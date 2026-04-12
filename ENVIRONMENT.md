# rainier Environment

## Identity

- Hostname: `rainier`
- FQDN in existing docs: `rainier.blackridge.shumie.net`
- Local domain in existing docs: `blackridge.shumie.net`
- Observed LAN IP in existing docs and live listeners: `192.168.3.10`
- Hardware from `hostnamectl`: ZOTAC `ZBOX-CI323NANO`
- Older docs contain conflicting hardware references and should be treated as stale where they disagree with `hostnamectl`

## OS and runtime

- OS: Ubuntu 24.04.4 LTS
- Kernel: `6.8.0-107-generic`
- Architecture: `x86_64`
- Root filesystem: `98G` total, `14G` used, `80G` available at time of inspection

## Git-backed durable repo

- Repo: `/home/shumie/projects/rainier-infra`
- Branch: `main`
- Remote: `git@github.com:shumie37/rainier-infra.git`

## Live paths

### Deploy/config paths

- AdGuard compose: `/home/shumie/adguard/docker-compose.yml`
- Caddy compose: `/home/shumie/caddy/compose.yaml`
- Caddy config: `/home/shumie/caddy/Caddyfile`
- Home Assistant compose: `/home/shumie/homeassistant/docker-compose.yml`
- Mosquitto config: `/home/shumie/mosquitto/config/mosquitto.conf`

### Runtime/state paths

- AdGuard runtime: `/home/shumie/adguard/work`
- AdGuard secret-bearing config: `/home/shumie/adguard/conf/AdGuardHome.yaml`
- Home Assistant runtime/config root: `/home/shumie/homeassistant/config`
- Home Assistant DB/log artifacts present in the live config root
- Mosquitto data: `/home/shumie/mosquitto/data`
- Mosquitto log: `/home/shumie/mosquitto/log`

### Repo-tracked copies verified against live files

Verified equal during this inspection:

- `compose/adguard/docker-compose.yml`
- `compose/homeassistant/docker-compose.yml`
- `homeassistant/configuration.yaml`
- `homeassistant/automations.yaml`
- `homeassistant/scenes.yaml`
- `homeassistant/scripts.yaml`
- `mosquitto/config/mosquitto.conf`

## Exposure observed from socket inspection

Observed listeners:

- `22/tcp` SSH
- `53/tcp` and `53/udp` DNS on `192.168.3.10`
- `80/tcp` HTTP
- `443/tcp` HTTPS
- `8123/tcp` Home Assistant
- `1883/tcp` MQTT
- `3000/tcp` AdGuard web UI
- `21064/tcp`
- `18555/tcp`
- multicast and local service listeners on `1900/udp`, `5353/udp`, loopback DNS, and localhost editor/helper ports

Docker-confirmed published ports:

- Caddy: `80/tcp`, `443/tcp`, plus container listeners on `443/udp` and `2019/tcp`
- Mosquitto: `1883/tcp`
- AdGuard Home: no Docker port publishing because the service uses host networking
- Home Assistant: no Docker port publishing because the service uses host networking

Portainer note:

- Portainer was removed from the live host on `2026-04-11`

## Firewall

- `ufw` status: active
- Base LAN allows are in place for SSH, DNS, HTTP, HTTPS, Home Assistant, and MQTT
- Additional Docker-aware allows are required for current operation:
  - `172.18.0.0/16 -> 3000/tcp` for Caddy to reach AdGuard
  - `172.18.0.0/16 -> 8123/tcp` for Caddy to reach Home Assistant
  - `172.17.0.0/16 -> 53/tcp` and `53/udp` for Docker build containers to resolve DNS through AdGuard
- Recommended host policy is documented in `docs/FIREWALL.md`

## Running host services observed

- `docker.service`
- `containerd.service`
- `ssh.service`
- `cron.service`
- `systemd-networkd.service`
- `systemd-resolved.service`
- `rsyslog.service`
- `unattended-upgrades.service`

## Docker runtime verified

Running containers:

- `caddy` using a custom build with the Route 53 DNS provider module
- `adguardhome` using `adguard/adguardhome:latest`
- `mosquitto` using `eclipse-mosquitto`
- `homeassistant` using `ghcr.io/home-assistant/home-assistant:stable`

Observed Docker volumes:

- `caddy_caddy_config`
- `caddy_caddy_data`

Observed Docker networks:

- default `bridge`
- `host`
- `none`
- `proxy`

## Scheduling observed

- No user crontab for `shumie`
- No custom backup/sync timer was observed in `systemctl list-timers --all`
- Only standard OS maintenance timers were visible from the read-only inspection

## Ownership and permissions

Top-level path ownership observed:

- `/home/shumie`: `shumie:shumie`
- `/home/shumie/projects/rainier-infra`: `shumie:shumie`
- `/home/shumie/adguard`: `shumie:shumie`
- `/home/shumie/caddy`: `shumie:shumie`
- `/home/shumie/homeassistant`: `root:root`
- `/home/shumie/mosquitto`: UID/GID `1883`

Notable file ownership details:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`: `root:root`
- `/home/shumie/adguard/work/data`: `root:root`
- `/home/shumie/homeassistant/config/*`: mostly `root:root`
- `/home/shumie/mosquitto/config/passwords`: UID/GID `1883`, mode `600`

## Remaining unverified items

- Docker volume mount contents and backup status were not inspected
- router-level forwarding and any upstream firewalling were not inspected

## TLS and DoH status

- `dns.blackridge.shumie.net` now presents a publicly trusted Let's Encrypt certificate
- issuance uses Route 53 DNS-01 through a custom Caddy build
- `https://dns.blackridge.shumie.net/dns-query` now exists and returns application-level responses instead of proxy failure
- host-side `dig +https` validation remained inconsistent during this session, so Apple/client rollout should still be validated from an actual client device
