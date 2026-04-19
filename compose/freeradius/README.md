# FreeRADIUS compose scaffold

This directory contains the tracked deploy scaffold for the planned FreeRADIUS service on `rainier`.

Tracked here:

- `compose.yaml`
- `.env.radius.example`
- `raddb/` tracked configuration tree

Local-only on the live host:

- `.env.radius`
- `certs/` with server certificate, key, and trusted CA material mounted to `/etc/freeradius/certs`

Expected live layout on `rainier`:

- `/home/shumie/freeradius/compose.yaml`
- `/home/shumie/freeradius/raddb/`
- `/home/shumie/freeradius/.env.radius`
- `/home/shumie/freeradius/certs/`

Notes:

- The initial container runs with `network_mode: host` to keep RADIUS UDP port handling simple.
- The live deployment now mounts a full `raddb/` tree derived from the image defaults and edited for `EAP-TLS`.
- The image tag should be pinned deliberately before first production deployment.
- `EAP-TLS` is the intended authentication mode; password-based inner methods are not part of the target design.
