from python:3.9-alpine
workdir /app
copy pack.txt .
run pip install --no-cache-dir -r pack.txt
copy . .
cmd ["python", "app.py"]
