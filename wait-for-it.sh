#!/usr/bin/env bash

# wait-for-it.sh - Wait for a service to become available.

TIMEOUT=15
HOST=$(echo $1 | cut -d':' -f1)
PORT=$(echo $1 | cut -d':' -f2)

for i in $(seq $TIMEOUT); do
  nc -z "$HOST" "$PORT" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Service $HOST:$PORT is available!"
    exec "${@:2}"
    exit 0
  fi
  echo "Waiting for $HOST:$PORT..."
  sleep 1
done

echo "Timeout reached: $HOST:$PORT not available after $TIMEOUT seconds."
exit 1
