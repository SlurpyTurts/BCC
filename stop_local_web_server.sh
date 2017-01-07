#!/bin/bash
DOCKER_PID=$(docker ps -q --filter name=bcc-web-server)
docker stop $DOCKER_PID
docker rm $DOCKER_PID
