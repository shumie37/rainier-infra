#!/usr/bin/env bash
set -euo pipefail

REPO="${HOME}/projects/rainier-infra"

echo "Checking tracked files exist..."
test -f "${REPO}/compose/adguard/docker-compose.yml"
test -f "${REPO}/compose/nginx-proxy/compose.yaml"
test -f "${REPO}/compose/nginx-proxy/nginx/nginx.conf"
test -f "${REPO}/compose/nginx-proxy/nginx/templates/blackridge.conf.template"
test -f "${REPO}/docs/NGINX-CUTOVER.md"
test -f "${REPO}/compose/homeassistant/docker-compose.yml"
test -f "${REPO}/mosquitto/config/mosquitto.conf"
test -f "${REPO}/homeassistant/configuration.yaml"

echo "Checking ignored sensitive/runtime paths are not tracked..."
git -C "${REPO}" ls-files | grep -q '^adguard/conf/AdGuardHome.yaml$' && { echo "ERROR: AdGuardHome.yaml is tracked"; exit 1; } || true
git -C "${REPO}" ls-files | grep -q '^homeassistant/config/secrets.yaml$' && { echo "ERROR: secrets.yaml is tracked"; exit 1; } || true
git -C "${REPO}" ls-files | grep -q '^mosquitto/config/passwords$' && { echo "ERROR: mosquitto passwords file is tracked"; exit 1; } || true
git -C "${REPO}" ls-files | grep -q '^compose/nginx-proxy/.env.nginx-proxy$' && { echo "ERROR: nginx env file is tracked"; exit 1; } || true
git -C "${REPO}" ls-files | grep -q '^compose/nginx-proxy/auth/luna-admin.htpasswd$' && { echo "ERROR: nginx auth file is tracked"; exit 1; } || true

echo "Sanity checks passed."
