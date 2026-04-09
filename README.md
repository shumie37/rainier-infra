# rainier-infra

Clean Git-tracked infrastructure for rainier.blackridge.shumie.net.

Purpose:
- preserve disaster recovery configuration
- keep sensitive/runtime state out of Git
- document restore steps for core services

Services currently covered:
- AdGuard Home
- Caddy
- Home Assistant
- Mosquitto

Not currently tracked:
- Docker runtime state
- Portainer data
- Caddy runtime volumes
- Home Assistant secrets/databases/runtime cache
- Mosquitto passwords
