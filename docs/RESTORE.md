# Restore notes

High level restore plan:
1. Rebuild host OS and Docker
2. Clone this repository
3. Restore required secrets from 1Password
4. Recreate external Docker network(s) if needed
5. Restore compose files and config files to target live paths
6. Restore runtime/stateful data separately where required
7. Start services in dependency-aware order
8. Validate DNS, HTTPS, Home Assistant, and MQTT
Notes:
- Caddy runtime cert/account data is not stored in Git
- Portainer data is not stored in Git
- Home Assistant DB/runtime state is not stored in Git
- Mosquitto passwords are not stored in Git

## Docker network recreation

Caddy expects an external Docker network named `proxy`.

Create it before starting Caddy if it does not already exist:
bash
docker network create proxy
Check existing networks:
bash
docker network ls
## Suggested service restore order

1. AdGuard Home
2. Mosquitto
3. Home Assistant
4. Caddy
5. Portainer

## Notes on Portainer

Portainer is intentionally not fully backed up in Git.
Recreate it from compose/runtime instructions, then reconnect it to the Docker socket and reapply settings manually if needed.
