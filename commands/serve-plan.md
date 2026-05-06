# Serve Plan as HTML

Check the persistent Claude Plans server and report URLs.

## Arguments

The user provided: $ARGUMENTS

## Instructions

1. Check if the server is running:

   ```
   curl -s http://localhost:8899/api/count
   ```

   If this fails, tell the user to start it with `just dev` in `~/projects/claude-code-plans/` or install the launchd service with `just launchd-install`.

2. Get the Tailscale hostname:

   ```
   tailscale status --self --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['Self']['DNSName'].rstrip('.'))"
   ```

   If Tailscale is not available, fall back to `localhost`.

3. Report to the user:
   - Tailscale URL: `http://<tailscale-hostname>:8899/`
   - Localhost URL: `http://localhost:8899/`
   - If arguments were provided, also link to the specific plan: `http://localhost:8899/plan/<filename>`

The server runs as a persistent launchd service with real-time SSE updates. Plans auto-refresh in the browser when files change.
