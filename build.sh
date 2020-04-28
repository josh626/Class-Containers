#!/bin/bash

IMAGE_NAME=cc-app-test
CONTAINER_ID=$(docker ps -a | awk "/$IMAGE_NAME/"'{ print $1 }')
docker stop ${CONTAINER_ID}
docker rm ${CONTAINER_ID}
docker rmi ${IMAGE_NAME}
docker build -t cc-app .
docker run -d --name cc-app-test -p 80:80 cc-app

