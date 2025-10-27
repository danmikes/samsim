from python:3.10-slim

workdir /app

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy . .

expose 10000

cmd ["gunicorn", "--bind", "0.0.0.0:10000", "wsgi:application"]
