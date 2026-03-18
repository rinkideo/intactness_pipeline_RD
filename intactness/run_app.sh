#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-ghcr.io/rinkideo/intactness-app:latest}"
COMPOSE_FILE="docker-compose.app.yml"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed or not on PATH."
  echo "Install Docker Desktop, then rerun this script."
  exit 1
fi

echo "Pulling app image: ${IMAGE_NAME}"
docker pull "${IMAGE_NAME}"

echo "Starting Intactness app"
docker compose -f "${COMPOSE_FILE}" up -d

sleep 4

if command -v open >/dev/null 2>&1; then
  open "http://localhost:8501"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://localhost:8501" >/dev/null 2>&1 || true
fi

echo
echo "App is opening at http://localhost:8501"
echo "To stop it later: docker compose -f ${COMPOSE_FILE} down"
