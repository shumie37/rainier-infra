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
