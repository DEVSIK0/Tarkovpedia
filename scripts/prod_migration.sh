#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Uso: $0 archivo_migracion.sql"
  exit 1
fi

docker cp $1 tarkovpedia_web:/tmp/migracion.sql
docker compose -p tarkovpedia exec -T web \
  sqlite3 /app/data/tarkovpedia.db < /tmp/migracion.sql
echo "✅ Migración aplicada en PROD: $1"
