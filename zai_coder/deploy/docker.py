def get_dockerfile_template() -> str:
    return """FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 8765
CMD ["zai-coder", "serve", "--host", "0.0.0.0", "--port", "8765"]
"""

def get_docker_compose_template() -> str:
    return """version: '3.8'

services:
  zai-coder:
    build: .
    ports:
      - "127.0.0.1:8765:8765"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
"""
