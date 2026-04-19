# rainier Memory

## Durable truths

- `projects/rainier-infra` is the canonical Git-backed repo for durable deploy config and host docs for `rainier`.
- nginx is the only supported ingress stack on `rainier`; the previous Caddy stack was removed from the host and repo on 2026-04-19.
- Secrets and runtime state are intentionally excluded from Git in several important places, which is correct in principle.
- Recovery is only partially durable today: configuration is Git-backed, but stateful backup capture and restore validation are not yet evidenced by the inspected host state.
- Hardware should be recorded canonically as ZOTAC `ZBOX-CI323NANO` based on `hostnamectl`.
- Home Assistant currently runs with `network_mode: host` and `privileged: true`.
- `ufw` is active on the host, with additional Docker-subnet allowances required for nginx-to-host proxying and Docker-build DNS.
- The recovery-critical backup baseline is AdGuard, nginx reverse proxy, Home Assistant, and Mosquitto.
- `dsm.blackridge.shumie.net` must resolve to `192.168.10.10` so clients reach nginx and receive the Rainier-managed Let's Encrypt certificate, while `nas.blackridge.shumie.net` should resolve directly to `192.168.10.20` for SMB and NAS access.
- Planned Wi-Fi direction is `WPA3-Enterprise` with `EAP-TLS`, using FreeRADIUS on `rainier` plus an internal CA for Apple device certificates.
- Step CA is the chosen CA service for the first internal PKI implementation on `rainier`.

## Ongoing risks to remember

- The host firewall is active, but Docker networking still creates non-obvious trust paths that must be documented and maintained deliberately.
- Service state lives under `/home/shumie` with mixed ownership (`shumie`, `root`, UID `1883`), which complicates clean backup capture and operator workflows.
- No backup target or automated backup job was confirmed during inspection.
- `scripts/sync-from-live.sh` assumes direct readability of live files; that is already false for parts of the current host.
- AdGuard rewrites can silently bypass nginx if service hostnames are pointed directly at backend devices.

## Preferred direction

- Keep `rainier-infra` as the durable config/docs repo.
- Keep nginx config and operational notes as the only supported ingress path.
- Separate tracked deploy artifacts from live runtime trees more explicitly.
- Move toward a documented, repeatable backup flow for stateful paths and Docker-managed volumes.
- Keep Route 53 credentials, RADIUS shared secrets, CA private keys, and device identity bundles local-only and out of Git.
