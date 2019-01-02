# Traefik stack

## Authentication

Before deploying the stack:

1. Generate a bcrypt-hashed password using `inv generate-bcrypt-hash`
2. Fill `.env` with `TRAEFIK_AUTH_USERNAME` and `TRAEFIK_AUTH_PASSWORD`
