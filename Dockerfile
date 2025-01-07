from python:3.9-alpine
workdir /app
run apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev
copy . .
run pip install --no-cache-dir -r pack.txt
