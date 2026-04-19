# UniFi WPA3-Enterprise rollout

## Purpose

This document captures the exact first-pass UniFi configuration needed to point the `lab-secure` test SSID at FreeRADIUS on `rainier`.

## Backend target

- RADIUS server: `192.168.3.10`
- Authentication port: `1812`
- Accounting port: `1813`
- Shared secret source: `/home/shumie/freeradius/.env.radius`

Do not copy the shared secret into Git.

## UniFi settings

Recommended first-pass test network:

- SSID: `lab-secure`
- Security protocol: `WPA3-Enterprise`
- Authentication server: `192.168.3.10`
- Authentication port: `1812`
- Accounting enabled: optional
- Accounting server: `192.168.3.10`
- Accounting port: `1813`
- Shared secret: value from `/home/shumie/freeradius/.env.radius`

## Notes

- Use a dedicated test SSID first instead of changing the primary home SSID.
- FreeRADIUS is configured for `EAP-TLS`, so no username/password inner method is required.
- The RADIUS server certificate currently uses:
  - common name: `radius.blackridge.shumie.net`
  - SANs: `radius.blackridge.shumie.net`, `192.168.3.10`

## Apple profile expectations

The Apple Wi-Fi profile should:

- trust the `Blackridge` root CA
- contain the device identity certificate
- set `AcceptEAPTypes` to TLS only
- trust the RADIUS server name `radius.blackridge.shumie.net`
- enable auto-join for `lab-secure`

## Validation sequence

1. Create the `lab-secure` SSID in UniFi.
2. Install the generated Apple `.mobileconfig` on one test device.
3. Join `lab-secure`.
4. Confirm FreeRADIUS logs show a successful TLS-based authentication.
5. Only after success, issue additional client certificates for other devices.
