# rainier-infra

Clean Git-tracked infrastructure for rainier.blackridge.shumie.net.

Purpose:
- preserve disaster recovery configuration
- keep sensitive/runtime state out of Git
- document restore steps for core services
- define the backup and recovery baseline for core services

Services currently covered:
- AdGuard Home
- Caddy
- Home Assistant
- Mosquitto

Not currently tracked:
- Docker runtime state
- Caddy runtime volumes
- AWS credential env files
- Home Assistant secrets/databases/runtime cache
- Mosquitto passwords

Key docs:

- `ARCHITECTURE.md`
- `ENVIRONMENT.md`
- `MEMORY.md`
- `docs/BACKUP.md`
- `docs/FIREWALL.md`
- `docs/LETSENCRYPT-ROUTE53.md`
- `docs/RESTORE.md`
