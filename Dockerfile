from python:3.9-alpine

workdir /app

RUN apk add --no-cache tzdata
ENV TZ=Europe/Amsterdam

copy pack.txt .

run pip install --no-cache-dir -r pack.txt

copy app.py .
copy templates/ ./templates/
copy static/ ./static/

cmd ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
