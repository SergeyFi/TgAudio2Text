#!/bin/bash

CONTAINER_NAME="tg-audio2text"
SESSION_FILE="TgAudio2Text.session"

echo "Build image $CONTAINER_NAME"
docker build -t "$CONTAINER_NAME" .

if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
  echo "Remove old container $CONTAINER_NAME"
  docker stop "$CONTAINER_NAME" && docker rm "$CONTAINER_NAME"
fi

echo "start container $CONTAINER_NAME"
docker run -d \
  --name "$CONTAINER_NAME" \
  --env-file .env \
  -v "$(pwd)/$SESSION_FILE:/app/$SESSION_FILE" \
  "$CONTAINER_NAME"

docker image prune -f

