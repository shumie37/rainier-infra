# WPA3-Enterprise with EAP-TLS

## Purpose

This document defines the planned home-lab Wi-Fi authentication model for Apple devices on the `blackridge.shumie.net` network.

## Goal

Target outcome:

- Apple devices auto-join Wi-Fi without a typed password
- Wi-Fi uses `WPA3-Enterprise`
- authentication uses `802.1X` with `EAP-TLS`
- each device has its own client certificate
- RADIUS runs locally on `rainier`
- public web certificates and internal Wi-Fi certificates remain separate concerns

## Design summary

Recommended architecture:

- UniFi APs act as the `802.1X` authenticators
- FreeRADIUS on `rainier` acts as the authentication server
- an internal PKI issues the RADIUS server certificate and Apple client certificates
- Apple devices receive a Wi-Fi configuration profile that includes:
  - the SSID
  - `EAP-TLS`
  - the trusted CA certificate
  - the device client certificate
  - auto-join enabled

## Trust model

### Why an internal CA is required

`EAP-TLS` needs mutual certificate trust:

- Apple devices must trust the RADIUS server certificate
- FreeRADIUS must trust the client certificates presented by devices

This trust is private to the home lab and should not depend on a public CA.

### PKI layout

Recommended split:

1. offline root CA
2. online issuing CA on `rainier`

The issuing CA signs:

- the FreeRADIUS server certificate
- one client certificate per Apple device

### Certificate naming

Recommended names:

- root CA: `Blackridge Root CA`
- issuing CA: `Blackridge Issuing CA`
- RADIUS server: `radius.blackridge.shumie.net`

Recommended client naming bias:

- one certificate per device
- simple stable names such as `macbook-air`, `iphone`, `ipad-pro`

## Service placement

### `rainier`

Planned services on `rainier`:

- FreeRADIUS
- issuing CA

The root CA should not remain online on `rainier`.

### UniFi

UniFi is responsible for:

- SSID definition
- `WPA3-Enterprise` network mode
- forwarding `802.1X` authentication to FreeRADIUS

UniFi is not the source of truth for certificate identity.

## Runtime model

### FreeRADIUS

FreeRADIUS will be deployed in Docker on `rainier`.

Initial bias:

- use `network_mode: host`
- bind standard RADIUS ports on the host
- mount tracked config from the repo
- mount certificates and secrets from a local-only runtime directory outside Git

Expected ports:

- `1812/udp` authentication
- `1813/udp` accounting

### Secrets and state

Do not commit:

- CA private keys
- RADIUS private keys
- client `.p12` exports
- any shared secret values used between UniFi and RADIUS

Track in Git:

- compose definitions
- non-secret FreeRADIUS config
- operational docs

Keep local-only on `rainier`:

- CA state
- RADIUS certificates and keys
- UniFi shared secret env file

## Apple client model

Each Apple device should receive a configuration profile containing:

- trusted CA certificate
- client identity certificate
- Wi-Fi payload for the secure SSID
- expected RADIUS server name
- `Auto Join = true`

Preferred deployment order:

1. validate with one Mac
2. validate with one iPhone
3. roll out to remaining Apple devices

## UniFi configuration target

Recommended first rollout:

- create a separate test SSID such as `lab-secure`
- security mode: `WPA3-Enterprise`
- authentication backend: FreeRADIUS on `rainier`

Do not migrate the primary SSID until:

- one Apple device has joined successfully
- reconnect behavior is validated
- certificate revocation and renewal expectations are documented

## Implementation phases

### Phase 1: documentation and scaffold

- add repo docs for PKI and RADIUS design
- add Docker compose for FreeRADIUS
- add placeholder config layout and secret expectations

### Phase 2: PKI bootstrap

- create offline root CA
- create online issuing CA
- issue FreeRADIUS server certificate
- issue one test client certificate

### Phase 3: FreeRADIUS activation

- deploy FreeRADIUS on `rainier`
- enable `EAP-TLS`
- point UniFi test SSID at FreeRADIUS
- replace temporary image test certificates with CA-issued `Blackridge` server material

### Phase 4: Apple validation

- install one `.mobileconfig` on a Mac
- verify join, reconnect, and reboot behavior
- roll out remaining devices

## Open design decisions

- whether the issuing CA should be `step-ca` or another lightweight internal PKI tool
- whether revocation checking should be enforced immediately or deferred for the first rollout
- how client profiles should be packaged and archived

## Current implementation status

As of `2026-04-14`:

- design direction chosen: `WPA3-Enterprise` + `EAP-TLS`
- deployment target chosen: FreeRADIUS on `rainier`
- internal CA required and planned
- Docker-based FreeRADIUS scaffold is the first implementation step

As of the first live bootstrap on `rainier`:

- `step-ca` is the chosen live CA service
- FreeRADIUS is configured with `default_eap_type = tls`
- the server certificate is now issued by the local `Blackridge` CA

## Hardening status

Current hardening targets:

- `default_eap_type = tls`
- `tls_min_version = "1.3"`
- `tls_max_version = "1.3"`
- `require_message_authenticator = yes` for the UniFi RADIUS client definition

Deferred until a fuller PKI lifecycle exists:

- CRL or OCSP-backed revocation checking
- moving from the current single-host CA bootstrap to the preferred offline-root / online-issuing split
