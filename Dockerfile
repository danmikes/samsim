from arm32v6/python:3.9-alpine

workdir /app

run apk add --no-cache \
    python3-dev \
    tzdata \
    gcc \
    gfortran \
    musl-dev \
    g++ \
    lapack-dev \
    libjpeg-turbo-dev \
    zlib-dev

env TZ=Europe/Amsterdam

run python -m pip install --upgrade pip

run python -m pip install --no-cache-dir --extra-index-url https://piwheels.org/simple \
    numpy==1.24.4 \
    scipy==1.10.1 \
    flask==2.3.3 \
    waitress==2.1.2 \
    ipython==8.15.0 \
    matplotlib==3.7.4 \
    pillow==10.0.0

copy . .

cmd ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--threads=4", "app:app"]
