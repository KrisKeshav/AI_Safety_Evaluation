# Pinned patch tag; run scripts/pin-digests.sh on a Docker host to convert to
# an immutable @sha256 digest before final submission.
FROM python:3.12.7-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1001 agent

WORKDIR /app
COPY repo/ /app/
RUN chown -R agent:agent /app

ENV PYTHONPATH=/app
ENV SMTP_HOST=smtp
ENV SMTP_PORT=1025
USER agent
