# Transport Layer Security (TLS 1.2+) Configuration

# BBMS-SR-001 (TC-Sec-01)
Owner: Rithish P M (PR #1)

## Overview
Per IEEE SRS Section 4.1 and SAD Section 3.6, all communication between clients and the Blood Bank Management System (BBMS) API must be encrypted using **TLS 1.2 or higher**. In development, HTTP is permitted on `127.0.0.1:8000` to allow offline testing without certificate installation, while production environments enforce TLS via environment configuration.

---

## Environment Variables

| Variable | Default (Dev) | Production Value | Purpose |
|---|---|---|---|
| `DJANGO_SECURE_SSL_REDIRECT` | `False` | `True` | Forces all non-HTTPS requests to redirect to HTTPS (HTTP 301). |
| `DJANGO_SECURE_HSTS_SECONDS` | `0` | `31536000` (1 year) | Instructs browsers via HTTP Strict Transport Security to only connect via HTTPS. |
| `DJANGO_BEHIND_PROXY` | `False` | `True` | Tells Django to inspect `X-Forwarded-Proto` header from reverse proxies (Nginx/Traefik/Cloudflare). |

---

## Production Deployment Architecture

In production, TLS termination is performed at the reverse proxy layer (e.g., Nginx, Caddy, or AWS ALB) using modern cipher suites (TLS 1.2 / TLS 1.3):

```
Client (Browser / Mobile)
        │
        ▼ HTTPS (Port 443, TLS 1.2 / TLS 1.3)
Reverse Proxy (Nginx / Caddy / Cloudflare)
        │
        ▼ HTTP (Internal network / Unix socket)
Gunicorn / Uvicorn WSGI Worker (Django App)
```

### Sample Nginx Configuration Snippet
```nginx
server {
    listen 80;
    server_name bbms.hospital.org;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name bbms.hospital.org;

    ssl_certificate /etc/letsencrypt/live/bbms.hospital.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bbms.hospital.org/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

---

## Verification & Testing
Verification of TLS enforcement is automated in `bloodrequests/tests/test_tls.py` (TC-Sec-01):
```bash
python manage.py test bloodrequests.tests.test_tls
```
The test suite overrides `SECURE_SSL_REDIRECT=True` and validates that HTTP requests receive an immediate 301 Permanent Redirect to HTTPS.
