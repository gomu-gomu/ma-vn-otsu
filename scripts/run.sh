#!/bin/bash

docker build -t eoussama/otsu-web -f docker/Dockerfile.web .
docker run --rm -v $(pwd)/otsu:/app/assets -p 8501:8501 eoussama/otsu-web