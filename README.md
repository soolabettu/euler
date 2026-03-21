# euler

Project Euler solutions.

## FastAPI endpoint

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the API:

```bash
uvicorn api:app --reload
```

Run it so other machines on your network can reach it:

```bash
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
```

Run it with local HTTPS on port `8443` after placing certificates in `~/.config/euler-api/tls/`:

```bash
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8443 \
  --ssl-keyfile ~/.config/euler-api/tls/euler-local-server.key \
  --ssl-certfile ~/.config/euler-api/tls/euler-local-server.crt
```

Fetch the code for a problem number:

```bash
curl http://127.0.0.1:8000/problems/8
```

Optionally filter by language when multiple implementations exist:

```bash
curl "http://127.0.0.1:8000/problems/204?language=python"
```

## systemd user service

Install the service:

```bash
mkdir -p ~/.config/systemd/user
cp euler-api.service ~/.config/systemd/user/euler-api.service
systemctl --user daemon-reload
systemctl --user enable --now euler-api.service
```

Check status:

```bash
systemctl --user status euler-api.service
```

From another machine on the same network, open:

```text
http://<headless-machine-ip>:8000/docs
```

## Local HTTPS on a LAN IP

Before starting the HTTPS service, place these files in `~/.config/euler-api/tls/`:

```text
euler-local-server.key
euler-local-server.crt
euler-local-ca.crt
```

Install and start the HTTPS service:

```bash
mkdir -p ~/.config/systemd/user
cp euler-api-https.service ~/.config/systemd/user/euler-api-https.service
systemctl --user daemon-reload
systemctl --user enable --now euler-api-https.service
```

The service will listen on:

```text
https://192.168.1.41:8443/
```

Trust the local CA on the GUI machine using this certificate:

```text
~/.config/euler-api/tls/euler-local-ca.crt
```

Without trusting that CA, the browser will show a certificate warning.
