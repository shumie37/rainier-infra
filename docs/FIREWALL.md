# Firewall Policy

## Purpose

This document defines the current and recommended host firewall policy for `rainier`.

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
- expose WAN-facing traffic only when intentionally published through the gateway

## Recommended allowlist

### SSH

Allow:

- `22/tcp` from trusted admin networks

### DNS

Allow:

- `53/tcp` and `53/udp` from trusted client networks

Reason:

- AdGuard is the LAN DNS server

### HTTP and HTTPS

Allow:

- `80/tcp` and `443/tcp` from trusted client networks

Optional, only if WAN publishing is intentional:

- `80/tcp` from anywhere
- `443/tcp` from anywhere

Reason:

- nginx reverse proxy ingress

### Home Assistant

Allow:

- `8123/tcp` from trusted LAN clients if direct access is still needed

### MQTT

Allow:

- `1883/tcp` from trusted LAN clients

### RADIUS

Allow:

- `1812/udp` and `1813/udp` from trusted UniFi infrastructure

### Step CA

Allow:

- `9000/tcp` from trusted admin clients only if remote CA administration is needed

## Recommended deny-by-omission

Do not allow broadly unless a specific use case is documented:

- `3000/tcp` AdGuard web UI
- `21064/tcp`
- `18555/tcp`
- `9000/tcp`

## Live Docker-aware exceptions

The following additional allows are currently required for correct host operation:

- `172.18.0.0/16 -> 3000/tcp` for nginx to reach AdGuard on the host
- `172.18.0.0/16 -> 8123/tcp` for nginx to reach Home Assistant on the host
- `172.17.0.0/16 -> 53/tcp` for Docker build containers to resolve DNS through AdGuard
- `172.17.0.0/16 -> 53/udp` for Docker build containers to resolve DNS through AdGuard

These are local container-network exceptions, not LAN exposure rules.
