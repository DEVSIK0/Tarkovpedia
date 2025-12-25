#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.." || exit 1

PROJECT="tarkovpedia"

echo "[*] Starting containers for project: $PROJECT"
docker compose -p "$PROJECT" up -d

echo "[OK] Containers started."
