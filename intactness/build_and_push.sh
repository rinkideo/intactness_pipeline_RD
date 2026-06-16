#!/usr/bin/env bash
set -euo pipefail

# Build and publish the multi-arch Intactness app image to GitHub Container Registry.
#
# Prerequisite (one time, until the token expires):
#   docker login ghcr.io -u <your-github-username>
#   (use a GitHub Personal Access Token with the "write:packages" scope as the password)
#
# Usage:
#   ./build_and_push.sh                 # pushes :latest for amd64 + arm64
#   TAG=2026-06-16 ./build_and_push.sh  # also override the tag
#   PLATFORMS=linux/amd64 ./build_and_push.sh   # single platform

IMAGE="${IMAGE:-ghcr.io/rinkideo/intactness-app}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
TAG="${TAG:-latest}"
BUILDER="${BUILDER:-intactness-builder}"

# Build from the repo root (parent of this script's folder) so Dockerfile.app
# can see both intactness/ and intactness/environment.docker.yml.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# A docker-container builder is required for multi-platform output.
if ! docker buildx inspect "${BUILDER}" >/dev/null 2>&1; then
  echo "Creating buildx builder: ${BUILDER}"
  docker buildx create --name "${BUILDER}" --driver docker-container --bootstrap
fi
docker buildx use "${BUILDER}"

echo "Building ${IMAGE}:${TAG} for ${PLATFORMS} and pushing to GHCR..."
docker buildx build \
  --platform "${PLATFORMS}" \
  -f intactness/Dockerfile.app \
  -t "${IMAGE}:${TAG}" \
  --push \
  .

echo "Done. Pushed ${IMAGE}:${TAG} (${PLATFORMS})."
echo "Lab members get it with: docker pull ${IMAGE}:${TAG}  (or just run run_app.sh)"
