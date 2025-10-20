from python:3.10-slim

env PYTHONUNBUFFERED=1
env PYTHONDONTWRITEBYTECODE=1
env MPLBACKEND=Agg

workdir /app

run apt-get update && apt-get install -y \
    gcc \
    gfortran \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

copy requirements.txt .

run pip install --no-cache-dir -r requirements.txt

copy . .

expose 8080

cmd ["gunicorn", "--workers", "2", "--threads", "2", "--bind", "0.0.0.0:8080", "app:application"]
