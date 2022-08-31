#!/bin/env bash

if ! command -v docker &> /dev/null
then
      echo "Docker not found in $PATH"
      exit
fi

CONTAINER_NAME="waycarbon_takehometest_backend"
EXISTING_CONTAINER_ID=$(docker ps -a -q -f name="$CONTAINER_NAME")

if [ -z "$EXISTING_CONTAINER_ID" ]
then
  echo "Container \"$CONTAINER_NAME\" is not running."
  echo "Use the run_server.sh script to launch the container."
else
  docker exec "$CONTAINER_NAME" \
    poetry run python \
      -m unittest discover\
      -v app.tests
fi

