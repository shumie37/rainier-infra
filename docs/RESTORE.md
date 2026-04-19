# Restore notes

See also:

- `docs/BACKUP.md` for the recovery baseline and what must exist before restore

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
- nginx expects a local-only `.env.nginx-proxy`
- Route 53 credentials for certificate issuance must remain local-only
- FreeRADIUS is planned to use a local-only `.env.radius` file plus local certificate material under `/home/shumie/freeradius/certs`
- Home Assistant DB/runtime state is not stored in Git
- Mosquitto passwords are not stored in Git
- the recovery-critical backup baseline is AdGuard, nginx reverse proxy, Home Assistant, and Mosquitto

## Docker network recreation

The reverse-proxy stack expects an external Docker network named `proxy`.

Create it before starting the stack if it does not already exist:

```bash
docker network create proxy
```

Check existing networks:

```bash
docker network ls
```

## Suggested service restore order

1. AdGuard Home
2. Mosquitto
3. Home Assistant
4. nginx reverse proxy
5. Optional staged services such as FreeRADIUS or Step CA
