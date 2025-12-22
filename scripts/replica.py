#!/usr/bin/env python3
# replica.py
# Safely clone a PROD SQLite database into PRE (no changes to PROD).
# Usage:
#   ./replica.py [PROD_DB] [PRE_DB]
# Defaults:
#   ./replica.py prod.db pre.db
#
# Recommended: SQLite >= 3.27 for VACUUM INTO (fallback uses backup API).

import argparse
import sqlite3
import sys
from pathlib import Path

def remove_side_files(path: Path) -> None:
    """Remove target file and possible WAL/SHM side files."""
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(path) + suffix)
        try:
            if p.exists():
                p.unlink()
        except Exception as e:
            print(f"Error: could not remove {p}: {e}", file=sys.stderr)
            sys.exit(1)

def vacuum_into(src: Path, dst: Path) -> bool:
    """
    Try to create a compact, consistent copy using VACUUM INTO.
    Returns True if it worked, False if not supported or failed.
    """
    try:
        # Open source in read-only mode; VACUUM INTO writes to 'dst'.
        uri = f"file:{src}?mode=ro"
        with sqlite3.connect(uri, uri=True) as conn:
            # Ensure connection is established; journal mode read is harmless
            conn.execute("PRAGMA journal_mode;")
            # VACUUM INTO does not accept parameters; escape single quotes
            dst_escaped = str(dst).replace("'", "''")
            conn.execute(f"VACUUM INTO '{dst_escaped}';")
        return True
    except sqlite3.OperationalError:
        # e.g., "near 'INTO': syntax error" if SQLite < 3.27
        return False

def backup_api(src: Path, dst: Path) -> None:
    """
    Fallback using sqlite3's backup API, then VACUUM/optimize the copy.
    """
    with sqlite3.connect(f"file:{src}?mode=ro", uri=True) as src_conn, \
         sqlite3.connect(str(dst)) as dst_conn:
        # Full backup in one shot (can accept pages & progress callback if needed)
        src_conn.backup(dst_conn)
        # Compact and optimize the new copy to mimic VACUUM INTO behavior
        dst_conn.execute("VACUUM;")
        dst_conn.execute("PRAGMA optimize;")
        dst_conn.commit()

def integrity_check(db_path: Path) -> bool:
    """Return True if PRAGMA integrity_check is 'ok'."""
    with sqlite3.connect(str(db_path)) as conn:
        row = conn.execute("PRAGMA integrity_check;").fetchone()
        return bool(row and row[0] == "ok")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely clone a PROD SQLite DB into PRE (no changes to PROD)."
    )
    parser.add_argument("prod", nargs="?", default="prod.db",
                        help="Path to the production DB (default: prod.db)")
    parser.add_argument("pre",  nargs="?", default="pre.db",
                        help="Path to the PRE DB (default: pre.db)")
    args = parser.parse_args()

    prod = Path(args.prod)
    pre  = Path(args.pre)

    if not prod.is_file():
        print(f"Error: PROD DB not found: {prod}", file=sys.stderr)
        sys.exit(1)

    # Remove previous PRE and side files (WAL/SHM)
    remove_side_files(pre)

    # Try VACUUM INTO first; if not supported, fallback to backup API
    used_vacuum = vacuum_into(prod, pre)
    if not used_vacuum:
        backup_api(prod, pre)

    # Quick integrity check
    if not integrity_check(pre):
        print("Warning: PRE integrity_check did not return 'ok'.", file=sys.stderr)
        sys.exit(1)

    method = "VACUUM INTO" if used_vacuum else "backup API"
    print(f"OK: PRE created/updated -> {pre} (from {prod}) using {method}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
