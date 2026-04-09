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
- Review DNS rewrite for claw.blackridge.shumie.net, current value appears typoed as 192.1.68.3.11 and likely should be 192.168.3.11.
