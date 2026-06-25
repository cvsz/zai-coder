FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --no-cache-dir -U pip pytest

EXPOSE 8765

CMD ["python", "-m", "pytest", "-q"]
