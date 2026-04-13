# Firewall Policy

## Purpose

This document defines the current and recommended host firewall policy for `rainier`.

The base LAN-only policy has now been applied.

## Current state

- `ufw` is active
- LAN allows are in place for SSH, DNS, HTTP, HTTPS, Home Assistant, and MQTT
- additional Docker bridge allows are in place for reverse-proxy and build-time DNS flows

## Security goal

Recommended posture:

- default deny inbound
- default allow outbound
- allow only explicitly required ports
- keep admin and service-specific management ports LAN-only
- expose WAN-facing traffic only when intentionally published through the UCG

## Assumed network scope

- LAN subnet: `192.168.3.0/24`
- Gateway: `192.168.3.1`
- Host: `192.168.3.10`
- Teleport VPN subnet: `192.168.2.0/24`

## Recommended allowlist

### SSH

Allow:

- `22/tcp` from `192.168.3.0/24`
- `22/tcp` from `192.168.2.0/24` (Teleport)

Reason:

- remote administration from trusted LAN

### DNS

Allow:

- `53/tcp` from `192.168.3.0/24`
- `53/udp` from `192.168.3.0/24`
- `53/tcp` from `192.168.2.0/24` (Teleport)
- `53/udp` from `192.168.2.0/24` (Teleport)

Reason:

- AdGuard is the LAN DNS server

### HTTP and HTTPS

Allow:

- `80/tcp` from `192.168.3.0/24`
- `443/tcp` from `192.168.3.0/24`

Optional, only if WAN publishing is intentional:

- `80/tcp` from anywhere
- `443/tcp` from anywhere

Reason:

- Caddy reverse proxy ingress

### Home Assistant

Allow:

- `8123/tcp` from `192.168.3.0/24`

Reason:

- direct LAN access only

### MQTT

Allow:

- `1883/tcp` from `192.168.3.0/24`

Reason:

- Home Assistant and trusted LAN clients

## Recommended deny-by-omission

Do not allow broadly unless a specific use case is documented:

- `3000/tcp` AdGuard web UI
- `21064/tcp`
- `18555/tcp`

These should remain blocked by the default deny policy unless intentionally opened to a narrow source range.

## Live Docker-aware exceptions

The following additional allows are currently required for correct host operation:

- `172.18.0.0/16 -> 3000/tcp` for Caddy to reach AdGuard on the host
- `172.18.0.0/16 -> 8123/tcp` for Caddy to reach Home Assistant on the host
- `172.17.0.0/16 -> 53/tcp` for Docker build containers to resolve DNS through AdGuard
- `172.17.0.0/16 -> 53/udp` for Docker build containers to resolve DNS through AdGuard

These are local container-network exceptions, not LAN exposure rules.

## Base command set applied

### LAN-only baseline

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow from 192.168.3.0/24 to any port 22 proto tcp comment 'ssh-lan'
sudo ufw allow from 192.168.2.0/24 to any port 22 proto tcp comment 'ssh-teleport'
sudo ufw allow from 192.168.3.0/24 to any port 53 proto tcp comment 'dns-tcp-lan'
sudo ufw allow from 192.168.3.0/24 to any port 53 proto udp comment 'dns-udp-lan'
sudo ufw allow from 192.168.2.0/24 to any port 53 proto tcp comment 'dns-teleport-tcp'
sudo ufw allow from 192.168.2.0/24 to any port 53 proto udp comment 'dns-teleport-udp'
sudo ufw allow from 192.168.3.0/24 to any port 80 proto tcp comment 'http-lan'
sudo ufw allow from 192.168.3.0/24 to any port 443 proto tcp comment 'https-lan'
sudo ufw allow from 192.168.3.0/24 to any port 8123 proto tcp comment 'homeassistant-lan'
sudo ufw allow from 192.168.3.0/24 to any port 1883 proto tcp comment 'mqtt-lan'
```

### Optional WAN ingress for reverse proxy only

Only if intentionally published through the gateway:

```bash
sudo ufw allow 80/tcp comment 'http-wan'
sudo ufw allow 443/tcp comment 'https-wan'
```

### Verification before enable

```bash
sudo ufw status numbered
sudo ss -tulpn
```

## Post-enable checks

Test from another trusted LAN client:

- SSH to `rainier`
- DNS queries to `192.168.3.10`
- access to `http://dns.blackridge.shumie.net` or the AdGuard DNS role as intended
- access to `https://ha.blackridge.shumie.net`
- direct Home Assistant on `192.168.3.10:8123` if still needed
- MQTT client connectivity on `192.168.3.10:1883`

Confirm these are blocked unless later justified:

- `192.168.3.10:3000`
- `192.168.3.10:21064`
- `192.168.3.10:18555`

## Open questions

- Is WAN forwarding enabled on the UCG for `80/tcp` and `443/tcp`?
- Does any legitimate workflow require direct LAN access to AdGuard UI on `3000/tcp`?
- What are `21064/tcp` and `18555/tcp`, and should they remain reachable?

## Recommendation

Best immediate target:

- keep the LAN-only deny-by-default `ufw` policy
- open WAN `80/443` only if the gateway is intentionally forwarding them
- keep admin and convenience ports blocked by default
- keep Docker bridge allowances as narrow and well-documented as possible
