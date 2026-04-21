# rainier-infra

Clean Git-tracked infrastructure for `rainier.blackridge.shumie.net`.

Purpose:
- preserve disaster recovery configuration
- keep sensitive/runtime state out of Git
- document restore steps for core services
- define the backup and recovery baseline for core services

Services currently covered:
- AdGuard Home
- nginx reverse proxy
- FreeRADIUS
- Home Assistant
- Mosquitto
- Step CA

Not currently tracked:
- Docker runtime state
- AWS credential env files
- nginx local-only env files
- Home Assistant secrets/databases/runtime cache
- Mosquitto passwords

Key docs:

- `ARCHITECTURE.md`
- `ENVIRONMENT.md`
- `MEMORY.md`
- `docs/BACKUP.md`
- `docs/FIREWALL.md`
- `docs/NGINX-CUTOVER.md`
- `docs/RADIUS-WPA3-EAP-TLS.md`
- `docs/UNIFI-WPA3-EAP-TLS-ROLLOUT.md`
- `docs/RESTORE.md`
