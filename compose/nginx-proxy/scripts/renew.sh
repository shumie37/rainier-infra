#!/bin/sh
set -eu

EMAIL="${ACME_EMAIL:?ACME_EMAIL is required}"

exec certbot certonly \
  --cert-name "ha.blackridge.shumie.net" \
  --expand \
  --non-interactive \
  --agree-tos \
  --dns-route53 \
  --email "${EMAIL}" \
  --preferred-challenges dns-01 \
  --server "https://acme-v02.api.letsencrypt.org/directory" \
  -d ha.blackridge.shumie.net \
  -d luna-admin.blackridge.shumie.net \
  -d dns.blackridge.shumie.net \
  -d dsm.blackridge.shumie.net \
  -d nas.blackridge.shumie.net \
  -d printer.blackridge.shumie.net \
  "$@"
