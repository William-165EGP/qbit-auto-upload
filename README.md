# Qbittorrent integration with Rclone
## Description
This repository aims to provide Qbittorrent integration.
The procedure is below:
  1. Check if the torrent has been downloaded using Qbittorrent api
  2. Call rclone to update the movies into Cloud Drive
  3. Delete the torrent and its related files
  4. All of the points above would be saved into log for further usage
## Deployment
The Deployment procedure is divided into 2 steps
Build on local machine:

    sudo docker build -t user_name/qbit_auto_upload:latest .
    sudo docker push user_name/qbit_auto_upload:latest

Deploy on remote machine:

    sudo docker compose pull
    sudo docker compose up -d

The example [.env](./remote_server_deploy/.env) is here
You should set up at least those environment variables in env file
## CI/CD Auto Build and Push
This repository will auto build the docker image and push into the dockerhub
See [docker image](.github/workflows/docker-image.yml) for more info
