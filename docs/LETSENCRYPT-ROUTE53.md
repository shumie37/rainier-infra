# Let's Encrypt via Route 53

## Purpose

This document defines the clean path to make `dns.blackridge.shumie.net` use a publicly trusted certificate for local DNS-over-HTTPS without requiring WAN port forwarding.

## Goal

Target outcome:

- `dns.blackridge.shumie.net` serves a publicly trusted certificate
- `https://dns.blackridge.shumie.net/dns-query` is usable by normal clients without trusting the Caddy internal CA
- certificate issuance uses DNS-01 through AWS Route 53
- no WAN `80/443` forwarding is required

## Current state

- `dns.blackridge.shumie.net` now presents a publicly trusted Let's Encrypt certificate
- local DoH is wired at `/dns-query`
- Caddy runs from a custom build that includes the Route 53 DNS provider module
- AWS credentials remain local-only and are injected through `.env.route53`

## Recommended architecture

### Certificate strategy

Use Let's Encrypt with DNS challenge against Route 53.

Do not use:

- `tls internal` for client-facing DoH long term
- HTTP-01 with WAN port forwards unless public ingress is intentionally desired

### Caddy runtime strategy

Switch from the stock `caddy:2` image to a Caddy image that includes:

- `dns.providers.route53`

Two viable paths:

1. build and pin a custom Caddy image locally
2. use a prebuilt custom image you control and trust

Preferred bias:

- build and pin the image deliberately
- track the build recipe in Git

## AWS requirements

### Secrets

Do not commit these:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- optional `AWS_SESSION_TOKEN`
- optional `AWS_PROFILE`

Prefer:

- a narrowly scoped IAM user or role
- credentials injected into the Caddy container through an env file or secret mechanism

### Minimum IAM permissions

The Route 53 plugin needs permission to:

- list hosted zones
- list record sets
- change record sets
- get Route 53 change status

Scope it to the specific hosted zone where possible.

## Required hosted zone facts

Need to know:

- the public hosted zone ID for `shumie.net`
- whether `blackridge.shumie.net` is inside the same public hosted zone

## Required compose changes

The Caddy service will need:

- a Route 53-capable image
- AWS credentials injected at runtime

Recommended env names:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION=us-east-1`

## Required Caddyfile change

Replace `tls internal` for `dns.blackridge.shumie.net` with a DNS-challenge ACME block.

Example shape:

```caddy
dns.blackridge.shumie.net {
    tls {
        dns route53 {
            hosted_zone_id {$ROUTE53_HOSTED_ZONE_ID}
        }
    }
    reverse_proxy host.docker.internal:3000
}
```

Notes:

- credentials can come from container environment variables
- `hosted_zone_id` is optional if discovery is reliable, but explicit is safer

## Caddy image build example

One clean approach is a custom Dockerfile based on `xcaddy`:

```dockerfile
FROM caddy:builder AS builder
RUN xcaddy build \
  --with github.com/caddy-dns/route53@latest

FROM caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```

## Rollout order

1. Confirm the public Route 53 hosted zone and AWS credential strategy.
2. Build or obtain the Route 53-capable Caddy image.
3. Inject AWS credentials into the Caddy runtime without committing them.
4. Update the `dns.blackridge.shumie.net` site to use `tls { dns route53 ... }`.
5. Restart Caddy.
6. Verify certificate issuance.
7. Verify `dig +https @dns.blackridge.shumie.net ...` succeeds without TLS errors.

## Verification commands

After rollout:

```bash
echo | openssl s_client -connect dns.blackridge.shumie.net:443 -servername dns.blackridge.shumie.net 2>/dev/null | openssl x509 -noout -subject -issuer
dig +https @dns.blackridge.shumie.net cloudflare.com A +short
dig +https @dns.blackridge.shumie.net mask.icloud.com A +short
curl -skI https://dns.blackridge.shumie.net/dns-query
```

Expected:

- issuer is a public CA chain, not the Caddy local CA
- DoH queries succeed without TLS trust errors

## Session result on 2026-04-11

What succeeded:

- Route 53 DNS-01 issuance through Let's Encrypt
- publicly trusted certificate for `dns.blackridge.shumie.net`
- Caddy custom build and Route 53 plugin deployment

What still needs client validation:

- end-to-end DoH client behavior from Apple and other real client devices
- whether host-local `dig +https` failures are client-specific or indicate remaining protocol nuance

## Non-goals

- exposing WAN `80/443` purely for ACME
- making all LAN clients use DoH automatically
- changing the UniFi gateway DNS role in this step

## Next implementation inputs needed

- Route 53 hosted zone ID
- preferred AWS credential delivery method
- whether to build the custom Caddy image locally on `rainier` or elsewhere
