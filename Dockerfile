# Install uv
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN uv tool install speedtest-cloudflare-cli

ENTRYPOINT [ "/app/scripts/entrypoint.sh"]
