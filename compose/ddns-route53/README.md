# Route 53 DDNS

Purpose:

- keep `vpn.blackridge.shumie.net` pointed at the current public WAN IP of the Blackridge UniFi gateway

Implementation:

- container: `crazymax/ddns-route53:2.15.0`
- runtime host: `rainier`
- schedule: every 5 minutes
- hosted zone: `Z1XIAIXXJ9KA3O`
- record: `vpn.blackridge.shumie.net`

Credential model:

- reuses the local-only AWS Route 53 credentials already present in `../nginx-proxy/.env.nginx-proxy`
- credentials must remain out of Git

Validated live:

- updater detected WAN IP `23.252.53.58`
- Route 53 update succeeded
- public DNS resolved `vpn.blackridge.shumie.net` to `23.252.53.58`
