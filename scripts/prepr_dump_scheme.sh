#!/bin/bash
set -e
sqlite3 ./data/tarkovpedia.db ".schema" > prep_schema.sql
echo "✅ Esquema de PREP guardado en prep_schema.sql"
