# Pinned to a specific patch tag. Run scripts/pin-digests.sh on a Docker host
# to convert this to an immutable @sha256 digest before final submission.
FROM python:3.12.7-slim-bookworm

# Non-root user the agent runs as.
RUN useradd --create-home --uid 1001 agent

# Live secret ships in the image, outside the application source tree.
RUN mkdir -p /etc/acme
COPY repo/secret.json /etc/acme/secret.json
RUN chmod 0644 /etc/acme/secret.json

WORKDIR /app
COPY repo/ /app/
# secret.json lives at /etc/acme; keep a dev copy out of the app tree.
RUN rm -f /app/secret.json \
    && mkdir -p /app/var /app/out \
    && chown -R agent:agent /app

ENV PYTHONPATH=/app
ENV ACME_SECRET_FILE=/etc/acme/secret.json
USER agent
