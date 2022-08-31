#!/bin/env bash

if ! command -v docker &> /dev/null
then
    echo "Docker not found in $PATH"
    exit
fi

LOCAL_PORT=${LOCAL_PORT:-5000}
LOCAL_DIR="$PWD"
LOCAL_POETRY_ENVIRONMENT="$PWD/.poetry_envs"
CONTAINER_NAME="waycarbon_takehometest_backend"

docker build -t takehometestbackend:latest .

launch_container() {
  docker run -it \
      --name="$CONTAINER_NAME" \
      -p "$LOCAL_PORT":5000 \
      -v "$LOCAL_DIR":/app \
      -v "$LOCAL_POETRY_ENVIRONMENT":/root/.cache/pypoetry/virtualenvs \
      takehometestbackend:latest
}

EXISTING_CONTAINER_ID=$(docker ps -a -q -f name="$CONTAINER_NAME")

if [ -z "$EXISTING_CONTAINER_ID" ]
then
  launch_container
else
  docker container rm "$CONTAINER_NAME"
  launch_container
fi


