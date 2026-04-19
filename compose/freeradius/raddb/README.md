# Planned FreeRADIUS config overrides

This directory is reserved for tracked, non-secret FreeRADIUS configuration overrides once the service moves past the initial install scaffold.

Expected tracked items later:

- `clients.conf` or equivalent client definitions without embedded secrets
- `mods-enabled/eap` tuned for `EAP-TLS`
- `sites-enabled/default` and `sites-enabled/inner-tunnel` changes if needed

Keep local-only:

- server private keys
- CA private keys
- exported Apple client identity bundles
- any config file containing shared secrets

Initial deployment bias:

- start the container with the image defaults
- inspect the live default config tree on `rainier`
- copy back only the non-secret deltas that are worth tracking in Git
