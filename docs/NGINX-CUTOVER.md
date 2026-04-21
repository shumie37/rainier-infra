# Nginx Cutover

## Purpose

This document records the migration of `rainier` ingress from Caddy to nginx and the final post-cutover state.

## Current live ingress inventory

Validated live on `rainier` on 2026-04-20:

- runtime: Docker container `nginx-proxy`
- live compose: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/compose.yaml`
- live config: `/home/shumie/projects/rainier-infra/compose/nginx-proxy/nginx/conf.d/blackridge.conf`
- published ports: `80/tcp`, `443/tcp`
- TLS automation: Let's Encrypt DNS-01 via Route 53
- Caddy rollback stack: removed from the host and removed from this repo on 2026-04-19

Current live hostname map:

- `rainier.blackridge.shumie.net` -> `192.168.10.10`
- `blackcomb.blackridge.shumie.net` -> `192.168.10.30`
- `ha.blackridge.shumie.net` -> `192.168.10.10`, proxied to `host.docker.internal:8123`
- `dns.blackridge.shumie.net` -> `192.168.10.10`, proxied to `192.168.10.10:3000`
- `dsm.blackridge.shumie.net` -> `192.168.10.10`, proxied to `https://192.168.10.20:5001` with upstream TLS verification disabled
- `nas.blackridge.shumie.net` -> `192.168.10.20` directly
- `printer.blackridge.shumie.net` -> `192.168.10.10`, proxied to `https://192.168.40.10:443` with upstream TLS verification disabled and HTTP/1.1 forced

## Important operational notes

- `dsm.blackridge.shumie.net` must resolve to `192.168.10.10` for clients to use the nginx-managed Let's Encrypt certificate. If local DNS points `dsm.blackridge.shumie.net` directly to `192.168.10.20`, clients bypass nginx and see the NAS certificate instead.
- `nas.blackridge.shumie.net` should resolve directly to `192.168.10.20` for SMB and direct NAS access rather than the reverse proxy.
- `rainier.blackridge.shumie.net`, `dns.blackridge.shumie.net`, `ha.blackridge.shumie.net`, and `printer.blackridge.shumie.net` all resolve to `192.168.10.10` in the current authoritative DNS map.
- `printer.blackridge.shumie.net` uses a constrained upstream TLS policy and a local fallback for the missing `TheatreHome` bundle.
- The tracked nginx template and generated config should be kept aligned when ingress changes are made.

## Tracked nginx stack

Tracked ingress files live under:

- `compose/nginx-proxy/compose.yaml`
- `compose/nginx-proxy/nginx/nginx.conf`
- `compose/nginx-proxy/nginx/templates/blackridge.conf.template`
- `compose/nginx-proxy/scripts/renew.sh`

Local-only runtime files that must not be committed:

- `compose/nginx-proxy/.env.nginx-proxy`

## Validation commands

Run from `rainier` after config or certificate changes:

```bash
curl --resolve ha.blackridge.shumie.net:443:127.0.0.1 https://ha.blackridge.shumie.net/ -kI
curl --resolve dns.blackridge.shumie.net:443:127.0.0.1 https://dns.blackridge.shumie.net/dns-query -kI
curl --resolve dsm.blackridge.shumie.net:443:127.0.0.1 https://dsm.blackridge.shumie.net/ -kI
curl --resolve printer.blackridge.shumie.net:443:127.0.0.1 https://printer.blackridge.shumie.net/ -kI
```

Application-level checks:

- Home Assistant UI loads correctly through nginx
- AdGuard DoH endpoint returns expected application responses
- Synology DSM loads through nginx and presents the Rainier-managed certificate
- Printer root and the missing `TheatreHome` assets load correctly through nginx

## Cleanup status

As of 2026-04-19:

- nginx serves production ports `80/443`
- old Caddy host files were removed from `/home/shumie/caddy`
- old tracked Caddy files were removed from this repo
- old Caddy Docker images and volumes were removed from the host
