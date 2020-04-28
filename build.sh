#!/bin/bash

IMAGE_NAME=cc-app
CONTAINER_ID=$(docker ps -a | awk "/$IMAGE_NAME/"'{ print $1 }')
docker stop ${CONTAINER_ID}
docker rm ${CONTAINER_ID}
docker rmi ${IMAGE_NAME}
docker build -t ${IMAGE_NAME} .
docker run -d --rm --name cc-app ${IMAGE_NAME}
