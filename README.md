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
