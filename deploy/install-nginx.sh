#!/usr/bin/env bash
# Install NRMS AI nginx snippets on the server (run with sudo)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SNIPPET_DIR="/etc/nginx/snippets"

echo "Installing NRMS AI nginx snippets to ${SNIPPET_DIR}..."
sudo mkdir -p "$SNIPPET_DIR"
sudo cp "$PROJECT_DIR/nginx/nrms-ai-proxy.conf" "$SNIPPET_DIR/nrms-ai-proxy.conf"
sudo cp "$PROJECT_DIR/nginx/nrms-ai-locations.conf" "$SNIPPET_DIR/nrms-ai-locations.conf"
echo ""
echo "Next steps:"
echo "  1. Add this line inside your nrms.ati.gov.et server { } block:"
echo "       include /etc/nginx/snippets/nrms-ai-locations.conf;"
echo "     OR copy locations from: $PROJECT_DIR/nginx/nrms-ai-locations.conf"
echo "  2. sudo nginx -t && sudo systemctl reload nginx"
echo "  3. docker compose -f $PROJECT_DIR/docker-compose.yml up -d --build"
