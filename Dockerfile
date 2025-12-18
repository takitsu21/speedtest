# Install uv
FROM python:3.13-slim@sha256:baf66684c5fcafbda38a54b227ee30ec41e40af1e4073edee3a7110a417756ba

WORKDIR /app

COPY scripts/entrypoint.sh /app/entrypoint.sh

RUN pip install speedtest-cloudflare-cli

ENTRYPOINT ["/app/entrypoint.sh"]
