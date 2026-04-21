# AdGuard Home

Tracked:
- compose file location and restore documentation
Not tracked:
- live AdGuardHome.yaml
- runtime work directory

Live paths:
- /home/shumie/adguard/docker-compose.yml
- /home/shumie/adguard/conf/AdGuardHome.yaml
- /home/shumie/adguard/work

Notes:
- AdGuardHome.yaml is intentionally excluded from Git because it contains authentication material.
- Review DNS rewrite for `claw.blackridge.shumie.net` against the current authoritative DNS map before relying on it. The older note about `192.1.68.3.11` / `192.168.3.11` is stale and should not be used as current guidance.
