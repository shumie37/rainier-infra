# Backup Layout

## Purpose

This document defines the backup and recovery baseline for the recovery-critical services on `rainier`.

Core services:

- AdGuard Home
- nginx reverse proxy
- Home Assistant
- Mosquitto

## Backup principles

- Keep deploy configuration in Git.
- Keep secrets out of Git.
- Keep mutable runtime state out of Git.
- Back up stateful data separately from the repo.
- Maintain at least one off-host backup copy.

## Layers

### Git-backed deploy config

Source of truth:

- `/home/shumie/projects/rainier-infra`

Tracked config includes:

- compose definitions
- nginx reverse-proxy config
- Home Assistant YAML config slices
- Mosquitto broker config
- durable operational docs

### Secrets

Secrets should be restored from secret storage, not Git.

Known secret-bearing paths:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- `/home/shumie/homeassistant/config/secrets.yaml`
- `/home/shumie/mosquitto/config/passwords`
- `compose/nginx-proxy/.env.nginx-proxy`
- SSH keys stored in 1Password

### Stateful runtime data

These paths require backup outside Git:

- `/home/shumie/adguard/work`
- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- Docker volume `nginx-proxy_letsencrypt`
- `/home/shumie/homeassistant/config`
- `/home/shumie/mosquitto/data`
- `/home/shumie/mosquitto/log` if log retention matters
- `/home/shumie/mosquitto/config/passwords`

## Service backup matrix

### AdGuard Home

Required for recovery:

- live config: `/home/shumie/adguard/conf/AdGuardHome.yaml`
- runtime/work data: `/home/shumie/adguard/work`

Tracked separately in Git:

- `/home/shumie/projects/rainier-infra/compose/adguard/docker-compose.yml`

Recovery note:

- DNS records, rewrites, auth material, and service settings depend on `AdGuardHome.yaml`

### nginx reverse proxy

Required for recovery:

- Docker volume `nginx-proxy_letsencrypt`
- local-only env file `compose/nginx-proxy/.env.nginx-proxy`

Tracked separately in Git:

- `/home/shumie/projects/rainier-infra/compose/nginx-proxy/compose.yaml`
- `/home/shumie/projects/rainier-infra/compose/nginx-proxy/nginx/nginx.conf`
- `/home/shumie/projects/rainier-infra/compose/nginx-proxy/nginx/templates/blackridge.conf.template`

Recovery note:

- certificate and account state is not fully in Git and should be backed up from the Let's Encrypt volume and restored AWS credentials

### Home Assistant

Required for recovery:

- `/home/shumie/homeassistant/config`

Especially important within that tree:

- `secrets.yaml`
- `.storage/`
- `home-assistant_v2.db*`
- custom integration or theme content if present

Tracked separately in Git:

- `/home/shumie/projects/rainier-infra/compose/homeassistant/docker-compose.yml`
- `/home/shumie/projects/rainier-infra/homeassistant/configuration.yaml`
- `/home/shumie/projects/rainier-infra/homeassistant/automations.yaml`
- `/home/shumie/projects/rainier-infra/homeassistant/scenes.yaml`
- `/home/shumie/projects/rainier-infra/homeassistant/scripts.yaml`

Recovery note:

- Git alone is not enough for Home Assistant recovery; database and `.storage` state matter

### Mosquitto

Required for recovery:

- `/home/shumie/mosquitto/config/passwords`
- `/home/shumie/mosquitto/data`

Optional:

- `/home/shumie/mosquitto/log`

Tracked separately in Git:

- `/home/shumie/projects/rainier-infra/mosquitto/config/mosquitto.conf`

Recovery note:

- without the password file and persistence DB, auth and retained state will not be fully restored

## Recommended backup sets

### Set A: Git-backed config

- push `rainier-infra` off-host
- verify branch and remote health

### Set B: Secrets and service state

Back up:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- `/home/shumie/adguard/work`
- Docker volume `nginx-proxy_letsencrypt`
- `/home/shumie/homeassistant/config`
- `/home/shumie/mosquitto/data`
- `/home/shumie/mosquitto/config/passwords`

Optional:

- `/home/shumie/mosquitto/log`

### Set C: Bootstrap facts

Record durably:

- host identity
- static IP
- DNS role
- Docker network `proxy`
- restore order
- secret sources

## Restore dependency order

1. Restore secrets and state before starting services that require them.
2. Recreate Docker network `proxy`.
3. Restore AdGuard state.
4. Restore Mosquitto state.
5. Restore Home Assistant state.
6. Restore nginx certificate state and local-only env.
7. Start services in dependency-aware order.
8. Validate DNS, HTTPS, Home Assistant, and MQTT.
