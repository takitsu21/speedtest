# Install uv
FROM python:3.13-slim

WORKDIR /app

ADD scripts/entrypoint.sh /app/entrypoint.sh

RUN pip install speedtest-cloudflare-cli

ENTRYPOINT ["/app/entrypoint.sh"]
