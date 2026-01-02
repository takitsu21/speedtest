# Install uv
FROM python:3.14-slim@sha256:3955a7dd66ccf92b68d0232f7f86d892eaf75255511dc7e98961bdc990dc6c9b

WORKDIR /app

COPY scripts/entrypoint.sh /app/entrypoint.sh

RUN pip install speedtest-cloudflare-cli

ENTRYPOINT ["/app/entrypoint.sh"]
