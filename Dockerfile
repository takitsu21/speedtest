# Install uv
FROM python:3.14-slim@sha256:2751cbe93751f0147bc1584be957c6dd4c5f977c3d4e0396b56456a9fd4ed137

WORKDIR /app

COPY scripts/entrypoint.sh /app/entrypoint.sh

RUN pip install speedtest-cloudflare-cli

ENTRYPOINT ["/app/entrypoint.sh"]
