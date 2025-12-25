#!/usr/bin/env bash

cd "$(dirname "$0")/.." || exit 1

PROJECT="tarkovpedia"

echo "[*] Container status for project: $PROJECT"
docker compose -p "$PROJECT" ps

echo ""
echo "[*] Images for project: $PROJECT"
docker compose -p "$PROJECT" images