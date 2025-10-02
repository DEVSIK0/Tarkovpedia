#!/bin/bash
set -e
DATE=$(date +%F)
docker run --rm -v tarkovpedia_tarkovpedia_data:/data alpine \
  tar -czf - -C / data > prod_db_$DATE.tgz
echo "✅ Backup de PROD creado: prod_db_$DATE.tgz"
