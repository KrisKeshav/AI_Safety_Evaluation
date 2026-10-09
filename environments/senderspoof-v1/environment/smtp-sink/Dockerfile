FROM python:3.12.7-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY server.py /server.py
CMD ["python", "/server.py"]
