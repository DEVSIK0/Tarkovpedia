#!/usr/bin/env python3
# sync_auto.py
#
# Auto-generate and apply a data-preserving SCHEMA migration from PRE -> PROD.
# For each table:
#   - New in PRE           -> CREATE TABLE (+ indexes/triggers from PRE)
#   - Exists in PROD+PRE   -> if only ADD COLUMN (SQLite-safe) -> ALTER ADD COLUMN
#                           -> else rebuild with data copy (common columns)
# Tables in PROD but not in PRE are NOT dropped unless --allow-drop is given.
#
# Safety:
#   - Builds a single migration SQL
#   - Tests on a COPY of PROD
#   - Backs up PROD to /database/versions/
#   - Applies to PROD
#
# Usage:
#   ./sync_auto.py --prod /path/prod.db --pre /path/pre.db [--dry-run] [--allow-drop]
#
# Requires: Python 3.8+ (stdlib sqlite3) ; SQLite engine available to Python.

import argparse
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Optional


@dataclass
class ColumnInfo:
    cid: int
    name: str
    type: str
    notnull: int
    dflt_value: Optional[str]
    pk: int


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def fetch_all(conn: sqlite3.Connection, sql: str, params: Tuple = ()) -> List[tuple]:
    cur = conn.execute(sql, params)
    return cur.fetchall()


def list_tables(conn: sqlite3.Connection) -> List[str]:
    rows = fetch_all(
        conn,
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
    )
    return [r[0] for r in rows]


def table_create_sql(conn: sqlite3.Connection, table: str) -> str:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,)
    ).fetchone()
    return row[0] if row and row[0] else ""


def table_columns(conn: sqlite3.Connection, table: str) -> List[ColumnInfo]:
    rows = fetch_all(conn, f"PRAGMA table_info('{table}');")
    cols = [
        ColumnInfo(
            cid=int(r[0]),
            name=str(r[1]),
            type=str(r[2] or ""),
            notnull=int(r[3] or 0),
            dflt_value=(None if r[4] is None else str(r[4])),
            pk=int(r[5] or 0),
        )
        for r in rows
    ]
    # Ensure ordered by cid
    cols.sort(key=lambda c: c.cid)
    return cols


def indexes_for_table(conn: sqlite3.Connection, table: str) -> List[str]:
    rows = fetch_all(
        conn,
        "SELECT sql FROM sqlite_master "
        "WHERE type='index' AND tbl_name=? AND sql IS NOT NULL;",
        (table,),
    )
    return [r[0] for r in rows if r and r[0]]


def triggers_for_table(conn: sqlite3.Connection, table: str) -> List[str]:
    rows = fetch_all(
        conn,
        "SELECT sql FROM sqlite_master "
        "WHERE type='trigger' AND tbl_name=? AND sql IS NOT NULL;",
        (table,),
    )
    return [r[0] for r in rows if r and r[0]]


def quote_ident(name: str) -> str:
    # Minimal identifier quoting using double quotes
    return '"' + name.replace('"', '""') + '"'


def only_add_column_safe(prod_conn: sqlite3.Connection, pre_conn: sqlite3.Connection, table: str) -> bool:
    """
    Decide if PRE vs PROD differs only by ADD COLUMN that SQLite can perform safely.
    Rules for ADD COLUMN in SQLite:
      - Adds the column at the end
      - Column cannot have PRIMARY KEY, UNIQUE, or REFERENCES clause
      - NOT NULL requires a DEFAULT (so existing rows get a value)
      - CHECK allowed (we stay conservative and reject if we see UNIQUE/REFERENCES/PRIMARY KEY near col)
    """
    prod_cols = table_columns(prod_conn, table)
    pre_cols = table_columns(pre_conn, table)

    # PRE must not have fewer cols than PROD
    if len(pre_cols) < len(prod_cols):
        return False

    # First N columns (N = len(PROD)) must match exactly by name
    for i in range(len(prod_cols)):
        if prod_cols[i].name != pre_cols[i].name:
            return False

    # Extra columns in PRE must be safely ADDable
    create_sql = table_create_sql(pre_conn, table).lower()

    for i in range(len(prod_cols), len(pre_cols)):
        col = pre_cols[i]
        # Reject PK
        if col.pk != 0:
            return False
        # NOT NULL requires DEFAULT
        if col.notnull == 1 and (col.dflt_value is None or str(col.dflt_value).strip() == ""):
            return False
        # Conservative scan in CREATE TABLE for forbidden constraints on this column
        # (very rough, but good enough to be safe)
        # Look for patterns like: "<colname> ... unique|references|primary key"
        # We won't fully parse SQL; best-effort conservative check.
        needle = col.name.lower()
        # Split by commas to inspect column defs roughly
        for seg in create_sql.split(","):
            seg = seg.strip()
            if needle in seg:
                if ("unique" in seg) or ("references" in seg) or ("primary key" in seg):
                    return False

    return True


def emit_add_columns_sql(
    mig: List[str],
    prod_conn: sqlite3.Connection,
    pre_conn: sqlite3.Connection,
    table: str,
) -> None:
    """Emit ALTER TABLE ... ADD COLUMN statements for columns present in PRE but not in PROD."""
    prod_cols = table_columns(prod_conn, table)
    pre_cols = table_columns(pre_conn, table)

    existing = {c.name for c in prod_cols}

    for col in pre_cols:
        if col.name in existing:
            continue
        # Build limited column definition allowed by SQLite when adding a column
        parts = [quote_ident(col.name)]
        if col.type:
            parts.append(col.type)
        # Only add NOT NULL if DEFAULT exists (SQLite requirement)
        if col.notnull == 1 and col.dflt_value not in (None, ""):
            parts.append("NOT NULL")
        if col.dflt_value not in (None, ""):
            parts.append(f"DEFAULT {col.dflt_value}")

        coldef = " ".join(parts)
        mig.append(f"ALTER TABLE {quote_ident(table)} ADD COLUMN {coldef};")


def emit_rebuild_sql(
    mig: List[str],
    prod_conn: sqlite3.Connection,
    pre_conn: sqlite3.Connection,
    table: str,
) -> bool:
    """
    Emit a data-preserving rebuild for 'table'.
    Returns True if emitted; False if cannot determine any common columns.
    """
    create_sql = table_create_sql(pre_conn, table)
    if not create_sql:
        mig.append(f"-- WARN: no CREATE SQL in PRE for {table}")
        return False

    prod_cols = table_columns(prod_conn, table)
    pre_cols = table_columns(pre_conn, table)

    prod_names = [c.name for c in prod_cols]
    pre_names = [c.name for c in pre_cols]

    # Common columns in the order of PRE so INSERT matches new schema
    common = [c for c in pre_names if c in prod_names]
    if len(common) == 0:
        mig.append(f"-- ABORT: no common columns for {table}; manual migration required")
        return False

    idx_sqls = indexes_for_table(pre_conn, table)
    trg_sqls = triggers_for_table(pre_conn, table)

    mig.append("")
    mig.append(f"-- Rebuild table {table} (data-preserving)")
    mig.append(f"ALTER TABLE {quote_ident(table)} RENAME TO {quote_ident(table + '__old')};")
    mig.append(f"{create_sql};")

    qcols = ", ".join(quote_ident(c) for c in common)
    mig.append(
        f"INSERT INTO {quote_ident(table)} ({qcols}) "
        f"SELECT {qcols} FROM {quote_ident(table + '__old')};"
    )

    mig.append(f"DROP TABLE {quote_ident(table + '__old')};")

    for s in idx_sqls:
        if s:
            mig.append(f"{s};")
    for s in trg_sqls:
        if s:
            mig.append(f"{s};")

    return True


def integrity_check(conn: sqlite3.Connection) -> bool:
    row = conn.execute("PRAGMA integrity_check;").fetchone()
    return bool(row and row[0] == "ok")


def build_migration_sql(
    prod_conn: sqlite3.Connection,
    pre_conn: sqlite3.Connection,
    allow_drop: bool,
) -> List[str]:
    """
    Construct the migration statements list.
    """
    mig: List[str] = []
    mig.append("PRAGMA busy_timeout=5000;")
    mig.append("PRAGMA foreign_keys=OFF;")
    mig.append("BEGIN;")

    prod_tables = list_tables(prod_conn)
    pre_tables = list_tables(pre_conn)

    in_prod = set(prod_tables)
    in_pre = set(pre_tables)

    # 1) Create new tables (present in PRE but not in PROD)
    for t in pre_tables:
        if t not in in_prod:
            create_sql = table_create_sql(pre_conn, t)
            if create_sql:
                mig.append(f"{create_sql};")
            # indexes/triggers from PRE
            for s in indexes_for_table(pre_conn, t):
                if s:
                    mig.append(f"{s};")
            for s in triggers_for_table(pre_conn, t):
                if s:
                    mig.append(f"{s};")

    # 2) Existing tables: add-only or rebuild
    for t in pre_tables:
        if t not in in_prod:
            continue
        if only_add_column_safe(prod_conn, pre_conn, t):
            emit_add_columns_sql(mig, prod_conn, pre_conn, t)
        else:
            ok = emit_rebuild_sql(mig, prod_conn, pre_conn, t)
            if not ok:
                # Abort transaction if we cannot auto-migrate safely
                mig.append("ROLLBACK;")
                mig.append("PRAGMA foreign_keys=ON;")
                raise RuntimeError(
                    f"ABORT: could not auto-build rebuild SQL for table '{t}' (no common columns). "
                    f"Inspect PRE/PROD schemas and handle manually."
                )

    # 3) Optional: drop tables missing in PRE
    if allow_drop:
        for t in prod_tables:
            if t not in in_pre:
                mig.append(f"DROP TABLE {quote_ident(t)};")

    mig.append("COMMIT;")
    mig.append("PRAGMA foreign_keys=ON;")

    return mig


def apply_sql(conn: sqlite3.Connection, statements: List[str]) -> None:
    sql_text = "\n".join(statements)
    conn.executescript(sql_text)


def backup_sqlite(src_path: Path, dst_path: Path) -> None:
    with sqlite3.connect(f"file:{src_path}?mode=ro", uri=True) as src, \
         sqlite3.connect(str(dst_path)) as dst:
        src.backup(dst)


def write_temp_file(contents: str, suffix: str = ".sql") -> Path:
    tmp = tempfile.NamedTemporaryFile(delete=False, prefix="syncauto_", suffix=suffix)
    tmp.write(contents.encode("utf-8"))
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto-generate and apply a data-preserving SCHEMA migration from PRE -> PROD."
    )
    parser.add_argument("-p", "--prod", required=True, help="Path to PROD SQLite DB")
    parser.add_argument("-r", "--pre", required=True, help="Path to PRE SQLite DB")
    parser.add_argument("--dry-run", action="store_true", help="Generate & validate migration but do not apply to PROD")
    parser.add_argument("--allow-drop", action="store_true", help="Allow dropping tables missing in PRE")
    args = parser.parse_args()

    prod_db = Path(args.prod)
    pre_db = Path(args.pre)

    if not prod_db.is_file():
        die(f"Error: PROD DB not found: {prod_db}")
    if not pre_db.is_file():
        die(f"Error: PRE DB not found: {pre_db}")

    # Open read-only for PRE, read-write for PROD once we need to apply
    with sqlite3.connect(f"file:{prod_db}?mode=ro", uri=True) as prod_ro, \
         sqlite3.connect(f"file:{pre_db}?mode=ro", uri=True) as pre_ro:

        # Build migration list (may raise if unsafe)
        try:
            migration = build_migration_sql(prod_ro, pre_ro, allow_drop=args.allow_drop)
        except RuntimeError as e:
            # Persist partial SQL for inspection
            mig_tmp = write_temp_file("-- PARTIAL/ABORTED MIGRATION --\n" + str(e) + "\n")
            die(f"{e}\nSaved details to: {mig_tmp}")

    # If migration contains only BEGIN/COMMIT pragmas, treat as no-op.
    statements = [s.strip() for s in migration if s.strip()]
    # Heuristic: look for any real DDL keywords besides PRAGMA/BEGIN/COMMIT/ROLLBACK
    has_real_changes = any(
        s.upper().startswith(prefix)
        for s in statements
        for prefix in (
            "CREATE TABLE", "ALTER TABLE", "DROP TABLE", "CREATE INDEX",
            "CREATE TRIGGER", "INSERT INTO", "UPDATE ", "DELETE "
        )
    )
    if not has_real_changes:
        print("No schema changes detected. Nothing to apply.")
        return

    # Save migration SQL to a temp file for visibility
    mig_sql_text = "\n".join(migration) + "\n"
    mig_sql_path = write_temp_file(mig_sql_text, suffix=".sql")
    print(f"Generated migration SQL: {mig_sql_path}")

    # DRY-RUN: validate on a copy of PROD
    with tempfile.TemporaryDirectory(prefix="syncauto_", ignore_cleanup_errors=True) as workdir:
        test_db = Path(workdir) / "prod_test.db"
        backup_sqlite(prod_db, test_db)

        with sqlite3.connect(str(test_db)) as test_conn:
            try:
                apply_sql(test_conn, migration)
            except Exception as e:
                die(f"ABORT: Migration failed on test copy: {e}\nSee SQL: {mig_sql_path}")

            if not integrity_check(test_conn):
                die(f"ABORT: integrity_check on test copy failed.\nSee SQL: {mig_sql_path}")

        print("OK: migration validated on test copy.")

        if args.dry_run:
            print("DRY-RUN: not applying to PROD.")
            return

        # Prepare backup directory
        versions_dir = prod_db.parent / "versions"
        versions_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = versions_dir / f"prod_backup_{ts}.sqlitedb"

        print(f">> Creating PROD backup -> {backup_path}")
        backup_sqlite(prod_db, backup_path)

        # Apply to PROD
        print(">> Applying migration to PROD...")
        with sqlite3.connect(str(prod_db)) as prod_rw:
            try:
                apply_sql(prod_rw, migration)
            except Exception as e:
                die(f"ERROR applying migration to PROD: {e}\nBackup available: {backup_path}\nSQL: {mig_sql_path}")

            if not integrity_check(prod_rw):
                die(f"WARNING: integrity_check on PROD failed.\nBackup available: {backup_path}\nSQL: {mig_sql_path}")

    print("OK: migration applied to PROD.")
    print(f"Backup: {backup_path}")
    print(f"Migration SQL (temp): {mig_sql_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
