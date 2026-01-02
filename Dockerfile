# Install uv
FROM python:3.13-slim@sha256:1f3781f578e17958f55ada96c0a827bf279a11e10d6a458ecb8bde667afbb669

WORKDIR /app

COPY scripts/entrypoint.sh /app/entrypoint.sh

RUN pip install speedtest-cloudflare-cli

ENTRYPOINT ["/app/entrypoint.sh"]
