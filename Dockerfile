from python:3.9-alpine

workdir /app

RUN apk add --no-cache tzdata
ENV TZ=Europe/Amsterdam

copy pack.txt .

run apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev && \
  pip install --no-cache-dir -r pack.txt && \
  apk del gcc musl-dev linux-headers libffi-dev

copy app.py config.py .
copy templates/ ./templates/
copy static/ ./static/

cmd ["python", "app.py"]
