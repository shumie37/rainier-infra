# rainier Architecture

## Purpose

`rainier` is a small Ubuntu host running home infrastructure services with Git-backed deployment definitions in `/home/shumie/projects/rainier-infra`.

Primary goals:

- keep deploy configuration in Git
- keep runtime state out of Git
- keep secrets out of Git
- preserve a rebuild path from documented host facts, tracked config, restored secrets, and separately backed-up state

## Layers

### Host configuration

- Hostname: `rainier`
- OS: Ubuntu 24.04.4 LTS
- Kernel: `6.8.0-107-generic`
- Core host services observed: `ssh`, `docker`, `containerd`, `systemd-networkd`, `systemd-resolved`, `rsyslog`, `cron`, `unattended-upgrades`

Host configuration is not currently represented in a dedicated host-config repo.

### Deploy configuration

Canonical Git-backed repo:

- `/home/shumie/projects/rainier-infra`

Tracked deploy/config artifacts currently include:

- compose definitions for AdGuard, Caddy, and Home Assistant
- Caddyfile
- Home Assistant YAML config slices
- Mosquitto broker config
- restore and service notes

### Runtime state

Live service roots currently observed:

- `/home/shumie/adguard`
- `/home/shumie/caddy`
- `/home/shumie/homeassistant`
- `/home/shumie/mosquitto`

Runtime/stateful paths currently observed:

- AdGuard: `/home/shumie/adguard/work`
- AdGuard secret-bearing config: `/home/shumie/adguard/conf/AdGuardHome.yaml`
- Caddy runtime: Docker volumes `caddy_data`, `caddy_config` (documented; not directly verified through Docker CLI)
- Home Assistant runtime: `/home/shumie/homeassistant/config`
- Mosquitto runtime: `/home/shumie/mosquitto/data`, `/home/shumie/mosquitto/log`

### Secrets

Secret-bearing locations observed or documented:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- `/home/shumie/homeassistant/config/secrets.yaml`
- `/home/shumie/mosquitto/config/passwords`
- Docker-managed Caddy ACME/internal CA state in runtime volumes

Secret values must remain out of Git. Only locations and variable names should be documented.

### Durable documentation

Durable ops/docs location:

- `/home/shumie/projects/rainier-infra`

This repo is the correct home for:

- deployment definitions
- restore procedures
- host/environment notes
- durable continuity docs

### Backups

A documented restore outline exists, but no verified backup target or automated backup job was observed from readable host state.

That means the current architecture has a documented rebuild path for config, but not yet a verified recovery path for stateful data.

## Services and topology

### AdGuard Home

- Live compose path: `/home/shumie/adguard/docker-compose.yml`
- Runtime mode: host networking
- Tracked compose copy: `compose/adguard/docker-compose.yml`
- Secret-bearing live config intentionally excluded from Git

### Caddy

- Live compose path: `/home/shumie/caddy/compose.yaml`
- Live config path: `/home/shumie/caddy/Caddyfile`
- Tracked compose copy: `compose/caddy/compose.yaml`
- Tracked config copy: `caddy/Caddyfile`
- Live deployment now uses a custom Caddy build with the Route 53 DNS provider module
- Uses Docker bridge network `proxy`
- Published ports observed from Docker: `80/tcp`, `443/tcp`
- Terminates HTTPS for:
  - `ha.blackridge.shumie.net`
  - `dns.blackridge.shumie.net`
- `dns.blackridge.shumie.net` now uses Let's Encrypt via Route 53 DNS-01
- `/dns-query` is served through Caddy to AdGuard for local DoH use

### Home Assistant

- Live compose path: `/home/shumie/homeassistant/docker-compose.yml`
- Runtime mode: host networking
- Container is configured `privileged: true`
- Live config root: `/home/shumie/homeassistant/config`
- Tracked YAML slices are copied from the live config root into the repo

### Mosquitto

- Live config root: `/home/shumie/mosquitto/config`
- Live data root: `/home/shumie/mosquitto/data`
- Live log root: `/home/shumie/mosquitto/log`
- Tracked config copy: `mosquitto/config/mosquitto.conf`
- Anonymous auth disabled; password file is external to Git

## Architectural assessment

What is good:

- deploy/config and secret/runtime state are at least partially separated
- tracked config checked during this session matched the inspected live files
- Git remote exists for off-host config durability
- the recovery-critical service baseline is now explicit: AdGuard, Caddy, Home Assistant, and Mosquitto

What is weak:

- host config is not captured as code
- host firewall requires Docker-aware allowances for bridge subnets that proxy to host services
- backup architecture is not verified
- runtime paths live beside the operator home directory with inconsistent ownership
- some services rely on root-owned live trees, which makes capture/sync workflows brittle
