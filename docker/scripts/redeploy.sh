#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.." || exit 1

PROJECT="tarkovpedia"

echo "[*] Stopping containers..."
docker compose -p "$PROJECT" down

echo "[*] Building images without cache..."
docker compose -p "$PROJECT" build --no-cache

echo "[*] Starting fresh containers..."
docker compose -p "$PROJECT" up -d --force-recreate

echo "[OK] Rebuild complete."
