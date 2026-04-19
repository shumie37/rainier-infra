# rainier Environment

## Identity

- Hostname: `rainier`
- FQDN in existing docs: `rainier.blackridge.shumie.net`
- Local domain in existing docs: `blackridge.shumie.net`
- Observed primary LAN IP: `192.168.10.10`
- Hardware from `hostnamectl`: ZOTAC `ZBOX-CI323NANO`

## OS and runtime

- OS: Ubuntu 24.04.4 LTS
- Architecture: `x86_64`
- Git-backed durable repo: `/home/shumie/projects/rainier-infra`

## Live paths

### Deploy/config paths

- AdGuard compose: `/home/shumie/adguard/docker-compose.yml`
- nginx compose: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/compose.yaml`
- nginx config root: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/nginx`
- Home Assistant compose: `/home/shumie/homeassistant/docker-compose.yml`
- Mosquitto config: `/home/shumie/mosquitto/config/mosquitto.conf`

### Runtime/state paths

- AdGuard runtime: `/home/shumie/adguard/work`
- AdGuard secret-bearing config: `/home/shumie/adguard/conf/AdGuardHome.yaml`
- Home Assistant runtime/config root: `/home/shumie/homeassistant/config`
- Mosquitto data: `/home/shumie/mosquitto/data`
- Mosquitto log: `/home/shumie/mosquitto/log`

## Exposure observed

Observed listeners and published services include:

- `22/tcp` SSH
- `53/tcp` and `53/udp` DNS
- `80/tcp` HTTP
- `443/tcp` HTTPS
- `8123/tcp` Home Assistant
- `1883/tcp` MQTT
- `3000/tcp` AdGuard web UI
- `9000/tcp` Step CA

Docker-confirmed published ports:

- nginx-proxy: `80/tcp`, `443/tcp`
- mosquitto: `1883/tcp`

## Firewall

- `ufw` status: active
- Additional Docker-aware allows are required for current operation:
  - `172.18.0.0/16 -> 3000/tcp` for nginx to reach AdGuard
  - `172.18.0.0/16 -> 8123/tcp` for nginx to reach Home Assistant
  - `172.17.0.0/16 -> 53/tcp` and `53/udp` for Docker build containers to resolve DNS through AdGuard

## Docker runtime verified

Running containers:

- `nginx-proxy` using `nginx:1.27-alpine`
- `adguardhome` using `adguard/adguardhome:latest`
- `mosquitto` using `eclipse-mosquitto`
- `homeassistant` using `ghcr.io/home-assistant/home-assistant:stable`
- `freeradius` using `freeradius/freeradius-server:latest`
- `step-ca` using `smallstep/step-ca:latest`

Observed Docker volumes:

- `nginx-proxy_letsencrypt`
- `nginx-proxy_certbot-work`
- `nginx-proxy_certbot-log`

Observed Docker networks:

- default `bridge`
- `host`
- `none`
- `proxy`

## TLS and ingress notes

- nginx is the only supported ingress stack on `rainier`
- `dsm.blackridge.shumie.net` must resolve to `192.168.10.10` for clients to use the Rainier-managed Let's Encrypt certificate
- `nas.blackridge.shumie.net` should resolve directly to `192.168.10.20` for SMB and direct NAS access
- if local DNS points `dsm.blackridge.shumie.net` directly at `192.168.10.20`, clients bypass nginx and see the Synology certificate instead
