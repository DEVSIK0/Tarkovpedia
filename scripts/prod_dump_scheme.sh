#!/bin/bash
set -e
docker compose -p tarkovpedia exec -T web \
  sqlite3 /app/data/tarkovpedia.db ".schema" > prod_schema.sql
echo "✅ Esquema de PROD guardado en prod_schema.sql"
