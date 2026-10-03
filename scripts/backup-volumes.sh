#!/usr/bin/env bash
set -euo pipefail

# Archive Docker volume into a compressed tarball
BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/backups"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
VOLUME_NAME="${1:-local-ai_open-webui-data}"

mkdir -p "${BACKUP_DIR}"

docker run --rm \
  -v "${VOLUME_NAME}:/volume-data:ro" \
  -v "${BACKUP_DIR}:/backup" \
  alpine tar -czf "/backup/${VOLUME_NAME}_${TIMESTAMP}.tar.gz" -C /volume-data .

echo "Snapshot created: ${BACKUP_DIR}/${VOLUME_NAME}_${TIMESTAMP}.tar.gz"
