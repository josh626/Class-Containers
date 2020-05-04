#!/bin/bash

NAME=students
DOMAIN=classcontainers.com
CONTAINER_NAME=${NAME}
IMAGE_NAME=${NAME}
CONTAINER_ID=$(docker ps -a | awk "/$IMAGE_NAME/"'{ print $1 }')
docker stop ${CONTAINER_ID}
docker rm ${CONTAINER_ID}
docker rmi ${IMAGE_NAME}
docker build -t ${IMAGE_NAME} .
docker run -d --rm --name ${CONTAINER_NAME} \
	--mount type=bind,source="$(pwd)"/app,target=/app \
	-e "VIRTUAL_HOST=${CONTAINER_NAME}.${DOMAIN}" \
	-e "LETSENCRYPT_HOST=${CONTAINER_NAME}.${DOMAIN}" \
	${IMAGE_NAME}
