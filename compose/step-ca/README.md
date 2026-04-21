# Step CA compose scaffold

This directory contains the tracked deploy scaffold for the planned internal certificate authority on `rainier`.

Tracked here:

- `compose.yaml`

Local-only on the live host:

- `certs/`
- `config/`
- `db/`
- `secrets/`

Expected live layout on `rainier`:

- `/home/shumie/step-ca/compose.yaml`
- `/home/shumie/step-ca/certs/`
- `/home/shumie/step-ca/config/`
- `/home/shumie/step-ca/db/`
- `/home/shumie/step-ca/secrets/`

Notes:

- The current bootstrap uses a single on-host Step CA instance for both root and issuing material.
- The preferred long-term model is still an offline root with a separate online issuing CA.
- The live compose adds an explicit healthcheck against `/health` because the image default probe does not fit this hostname layout.
- Keep all Step CA private keys and password files out of Git.
