# Backup Layout

## Purpose

This document defines the backup and recovery baseline for the recovery-critical services on `rainier`.

Core services:

- AdGuard Home
- Caddy
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
- Caddyfile
- Home Assistant YAML config slices
- Mosquitto broker config
- durable operational docs

### Secrets

Secrets should be restored from secret storage, not Git.

Known secret-bearing paths:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- `/home/shumie/homeassistant/config/secrets.yaml`
- `/home/shumie/mosquitto/config/passwords`
- Caddy runtime volume contents used for TLS/account material
- SSH keys stored in 1Password

### Stateful runtime data

These paths require backup outside Git:

- `/home/shumie/adguard/work`
- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- Docker volume `caddy_caddy_data`
- Docker volume `caddy_caddy_config`
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

### Caddy

Required for recovery:

- Docker volume `caddy_caddy_data`
- Docker volume `caddy_caddy_config`

Tracked separately in Git:

- `/home/shumie/projects/rainier-infra/compose/caddy/compose.yaml`
- `/home/shumie/projects/rainier-infra/caddy/Caddyfile`

Recovery note:

- certificate/account state is not in Git and must be backed up from Docker-managed runtime state

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
- Docker volume `caddy_caddy_data`
- Docker volume `caddy_caddy_config`
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

## Retention recommendation

Minimum:

- daily local backup
- daily or weekly off-host replication
- retain multiple historical recovery points

Suggested bias:

- short retention for logs
- longer retention for Home Assistant and AdGuard state
- retain at least one known-good monthly recovery point off-host

## Restore dependency order

1. Restore secrets and state before starting services that require them.
2. Recreate Docker network `proxy`.
3. Restore AdGuard state.
4. Restore Mosquitto state.
5. Restore Home Assistant state.
6. Restore Caddy runtime volumes.
7. Start services in dependency-aware order.
8. Validate DNS, HTTPS, Home Assistant, and MQTT.

## Backup design gaps

Current gaps observed on `2026-04-11`:

- no verified backup target
- no verified backup schedule
- no verified restore test
- no documented capture method for Docker volumes
- mixed ownership on live paths complicates least-authority backup workflows

## Next implementation steps

1. Choose the backup destination and off-host replication target.
2. Decide which service state should be captured by file-level backup versus image or snapshot backup.
3. Add a repeatable backup script or job for the recovery-critical paths and volumes.
4. Add a restore verification checklist after the first successful backup run.
