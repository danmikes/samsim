# GitHub

## File
```
/app.py
/pack.txt
/Dockerfile
/.github/workflows/docker-build.yml
```

# Router

## Port
```
8080 -> 192.168.178.199
```

# Pi

## Docker
```
sudo apt update
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo apt install -y python3 python3-dev python3-env python3-pip
```

## Docker Compose V2
```
python -m venv .venv
source .venv/bin/activate
pip install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## File
```
/docker-compose.yml
/lib/systemd/system/containerd.service
```

## Start
```
docker compose up -d
```

## Stop
```
docker compose down
```

## Clean
```
docker system purge -a
```
