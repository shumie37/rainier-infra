# rainier Architecture

## Purpose

`rainier` is a small Ubuntu host running home infrastructure services with Git-backed deployment definitions in `/home/shumie/projects/rainier-infra`.

## Layers

### Host configuration

- Hostname: `rainier`
- Core host services observed: `ssh`, `docker`, `containerd`, `systemd-networkd`, `systemd-resolved`, `rsyslog`, `cron`, `unattended-upgrades`

### Authoritative DNS map

Current source-of-truth DNS records for the Blackridge environment:

- `blackcomb.blackridge.shumie.net` -> `192.168.10.30`
- `rainier.blackridge.shumie.net` -> `192.168.10.10`
- `dns.blackridge.shumie.net` -> `192.168.10.10`
- `ha.blackridge.shumie.net` -> `192.168.10.10`
- `dsm.blackridge.shumie.net` -> `192.168.10.10`
- `nas.blackridge.shumie.net` -> `192.168.10.20`
- `printer.blackridge.shumie.net` -> `192.168.10.10`

### Deploy configuration

Canonical Git-backed repo:

- `/home/shumie/projects/rainier-infra`

Tracked deploy/config artifacts currently include:

- compose definitions for AdGuard, nginx, Home Assistant, FreeRADIUS, and Step CA
- nginx reverse-proxy config and templates
- Home Assistant YAML config slices
- Mosquitto broker config
- restore and service notes

### Runtime state

Live service roots currently observed:

- `/home/shumie/adguard`
- `/home/shumie/homeassistant`
- `/home/shumie/mosquitto`
- `/home/shumie/step-ca`
- `/home/shumie/freeradius`

Runtime/stateful paths currently observed:

- AdGuard: `/home/shumie/adguard/work`
- AdGuard secret-bearing config: `/home/shumie/adguard/conf/AdGuardHome.yaml`
- nginx certificate state: Docker volume `nginx-proxy_letsencrypt`
- Home Assistant runtime: `/home/shumie/homeassistant/config`
- Mosquitto runtime: `/home/shumie/mosquitto/data`, `/home/shumie/mosquitto/log`
- Step CA state: `/home/shumie/step-ca/config`, `/home/shumie/step-ca/db`, `/home/shumie/step-ca/certs`, `/home/shumie/step-ca/secrets`

### Secrets

Secret-bearing locations observed or documented:

- `/home/shumie/adguard/conf/AdGuardHome.yaml`
- `/home/shumie/homeassistant/config/secrets.yaml`
- `/home/shumie/mosquitto/config/passwords`
- `compose/nginx-proxy/.env.nginx-proxy`
- `/home/shumie/step-ca/secrets`

## Services and topology

### AdGuard Home

- Live compose path: `/home/shumie/adguard/docker-compose.yml`
- Runtime mode: host networking
- Tracked compose copy verified in this repo: `compose/adguard/docker-compose.yml`

### nginx reverse proxy

- Live compose path: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/compose.yaml`
- Live config path: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/nginx/conf.d/blackridge.conf`
- Tracked template path: `compose/nginx-proxy/nginx/templates/blackridge.conf.template`
- Uses Docker bridge network `proxy`
- Published ports observed from Docker: `80/tcp`, `443/tcp`
- Terminates HTTPS for public service hostnames including `ha`, `dns`, `dsm`, and `printer`
- `dsm.blackridge.shumie.net` must resolve to `192.168.10.10` so clients hit nginx instead of the Synology directly
- `nas.blackridge.shumie.net` should resolve directly to `192.168.10.20` for SMB and direct NAS access

### Home Assistant

- Live compose path: `/home/shumie/homeassistant/docker-compose.yml`
- Runtime mode: host networking
- Live config root: `/home/shumie/homeassistant/config`

### Mosquitto

- Live config root: `/home/shumie/mosquitto/config`
- Live data root: `/home/shumie/mosquitto/data`
- Live log root: `/home/shumie/mosquitto/log`

### FreeRADIUS

- Live compose path: `/home/shumie/freeradius/compose.yaml`
- Local-only certificate root: `/home/shumie/freeradius/certs`

### Step CA

- Live compose path: `/home/shumie/step-ca/compose.yaml`
- Published port: `9000/tcp`
- Intended role: internal CA for FreeRADIUS server and Apple device certificates

## Architectural assessment

What is good:

- deploy/config and secret/runtime state are reasonably separated
- Git remote exists for off-host config durability
- nginx ingress is now tracked directly in the repo instead of through a parallel legacy stack

What is weak:

- host config is not captured as code
- firewall behavior still depends on Docker-aware allowances for bridge subnets that proxy to host services
- backup architecture is not yet verified end-to-end
- runtime paths live beside the operator home directory with mixed ownership
