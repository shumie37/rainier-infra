#!/usr/bin/env bash
set -euo pipefail

REPO="${HOME}/projects/rainier-infra"

echo "Syncing approved files from live paths into repo..."
cp /home/shumie/adguard/docker-compose.yml "${REPO}/compose/adguard/docker-compose.yml"
cp /home/shumie/homeassistant/docker-compose.yml "${REPO}/compose/homeassistant/docker-compose.yml"
cp /home/shumie/mosquitto/config/mosquitto.conf "${REPO}/mosquitto/config/mosquitto.conf"
cp /home/shumie/homeassistant/config/configuration.yaml "${REPO}/homeassistant/configuration.yaml"
cp /home/shumie/homeassistant/config/automations.yaml "${REPO}/homeassistant/automations.yaml"
cp /home/shumie/homeassistant/config/scenes.yaml "${REPO}/homeassistant/scenes.yaml"
cp /home/shumie/homeassistant/config/scripts.yaml "${REPO}/homeassistant/scripts.yaml"

if [ -d /home/shumie/homeassistant/config/themes ]; then
  mkdir -p "${REPO}/homeassistant/themes"
  rm -rf "${REPO}/homeassistant/themes"
  mkdir -p "${REPO}/homeassistant/themes"
  cp -R /home/shumie/homeassistant/config/themes/. "${REPO}/homeassistant/themes/"
fi

echo
echo "Sync complete. Review changes with:"
echo "  cd ${REPO} && git status && git diff"
