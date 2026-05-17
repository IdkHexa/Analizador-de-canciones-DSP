# Stage 1: Build environment
FROM python:3.12-slim AS builder

RUN apt-get update -qq && apt-get install -y -qq \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

RUN apt-get update -qq && apt-get install -y -qq \
    libsndfile1 \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon0 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

ENTRYPOINT ["python", "main.py"]
