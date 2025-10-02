#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Uso: $0 archivo_backup.tgz"
  exit 1
fi

tar -xzf $1 -C ./data
echo "✅ Restaurada BD de PROD en PREP (./data/tarkovpedia.db)"
