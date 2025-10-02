📖 DB Workflow (PROD / PREP)

We use two databases:

PROD (VPS): real data, untouchable.

PREP (local PC): copy of PROD, free to break/test.

🔄 Daily workflow

1. Refresh PREP from PROD
```bash
# On VPS
./scripts/prod-backup.sh
# Download file to PC
scp user@IP:prod_db_DATE.tgz .
# On PC
./scripts/prep-restore-from-prod.sh prod_db_DATE.tgz
```

2. Work on PREP

Modify/test data freely.

Change schema if needed (add tables/columns).

3. Check schema differences
```bash
./scripts/prep-dump-schema.sh   # PC
./scripts/prod-dump-schema.sh   # VPS
```

Compare prep_schema.sql vs prod_schema.sql.

4. Apply migration to PROD
```bash
./scripts/prod-backup.sh
./scripts/prod-apply-migration.sh migration_X.sql
```
🛡 Rules

Never touch PROD data.

Always backup before migrations.

PREP = playground. PROD = real users.