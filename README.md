# Flask-App

## Local

### File
- /app.py
- /pack.txt
- /Dockerfile
- /.github/workflows/docker-build.yml

### Script
- sh script/docker-copy.sh
- sh script/docker-install.sh
- sh script/docker-refresh.sh
- sh script/docker-update.sh

### Environment Variable
- .env.blank -> .env

## GitHub

### Repository Secret
- PI_HOST = <Raspi hostname>
- PI_USER = <Raspi username>
- PI_PASS = <Raspi password>

## Router

### Port
- 80 -> 192.168.178.199
- 443 -> 192.168.178.199

## GitHub-actions

### docker-build.yml
- `git push` triggers /.github/workflows/docker-build.yml
- Dockerfile makes Gunicorn-Flask Image
- Builds and pushes docker-image to GitHub Container-Service
- Updates docker-compose.yml

## Shell-script

### docker-compose.yml
- `sh update` triggers 
  - `docker compose pull`
  - `docker compose up` | +1 container
  - `docker compose up` | -1 container

## Log
```
docker volume ls
docker compose logs -f docker-traefik-1
docker compose logs -f docker-flask-1
```

## Docker
```
docker exect -it docker-flask-1 sh
docker exect -it docker-traefik-1 sh
```

# Update App

1. push changes to GitHub-repo
```
git push
```

2. verify build by GitHub-action
```
cd sh build
```

3. copy conf files to Raspi
```
sh copy
```

4. restart Flask-container
```
sh update
```
