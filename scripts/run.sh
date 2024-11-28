#!/bin/bash

set -e

if [ "$1" == "web" ]; then
  docker build -t eoussama/otsu-web -f docker/Dockerfile.web .
  docker run --rm -v $(pwd)/otsu:/app/assets -p 8501:8501 eoussama/otsu-web
elif [ "$1" == "cli" ]; then
  if [ -z "$2" ]; then
    echo "Error: Image page is required."
    echo "Usage: ./run.sh cli <image_path>"
    exit 1
  fi

  docker build -t eoussama/otsu-cli -f docker/Dockerfile.cli .
  docker run --rm -v $(pwd)/assets:/app/assets eoussama/otsu-cli "$2"
else
  echo "Usage: ./run.sh [web|cli]"
fi