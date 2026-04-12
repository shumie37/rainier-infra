# rainier Memory

## Durable truths

- `projects/rainier-infra` is the canonical Git-backed repo for durable deploy config and host docs for `rainier`.
- The repo currently matches the inspected live files for AdGuard compose, Caddy compose/config, Home Assistant compose/YAML slices, and Mosquitto config.
- Secrets and runtime state are intentionally excluded from Git in several important places, which is correct in principle.
- Recovery is only partially durable today: configuration is Git-backed, but stateful backup capture and restore validation are not yet evidenced by the inspected host state.
- Hardware should be recorded canonically as ZOTAC `ZBOX-CI323NANO` based on `hostnamectl`.
- Home Assistant currently runs with `network_mode: host` and `privileged: true`.
- Portainer was removed from the live host on `2026-04-11` and is not part of the tracked recovery baseline.
- `ufw` is active on the host, with additional Docker-subnet allowances required for Caddy-to-host proxying and Docker-build DNS.
- Verified Docker runtime currently includes `caddy`, `adguardhome`, `mosquitto`, and `homeassistant`.
- Verified persistent Docker volumes currently include `caddy_caddy_config` and `caddy_caddy_data`.
- The recovery-critical backup baseline is AdGuard, Caddy, Home Assistant, and Mosquitto.
- `dns.blackridge.shumie.net` now uses Let's Encrypt via Route 53 DNS-01 on a custom Caddy build.

## Ongoing risks to remember

- The host firewall is active, but Docker networking still creates non-obvious trust paths that must be documented and maintained deliberately.
- Service state lives under `/home/shumie` with mixed ownership (`shumie`, `root`, UID `1883`), which complicates clean backup capture and operator workflows.
- No backup target or automated backup job was confirmed during this inspection.
- `scripts/sync-from-live.sh` assumes direct readability of live files; that is already false for parts of the current host.
- Older docs contain at least one stale hardware reference and should be updated or retired.
- AdGuard notes already document a likely DNS rewrite typo for `claw.blackridge.shumie.net` that should be validated before relying on it.

## Preferred direction

- Keep `rainier-infra` as the durable config/docs repo.
- Add first-class top-level docs for architecture, environment, and continuity.
- Separate tracked deploy artifacts from live runtime trees more explicitly.
- Move toward a documented, repeatable backup flow for stateful paths and Docker-managed volumes.
- Use `docs/BACKUP.md` as the backup-scope baseline until a real backup implementation exists.
- Use `docs/FIREWALL.md` as the live host firewall baseline and keep the Docker-subnet allowances documented there.
- Keep Route 53 credentials local-only and out of Git.

## Decision bias

- Prefer cleanup in place only if it improves separation and recoverability without hidden live drift.
- Prefer rebuild if undocumented state, root-owned drift, or ad hoc runtime layout continues to accumulate faster than it can be normalized.
