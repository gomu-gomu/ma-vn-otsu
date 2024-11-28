#!/bin/bash

docker build -t eoussama/otsu-web -f docker/Dockerfile.web .
docker run --rm -v $(pwd)/assets:/app/assets -p 8501:8501 eoussama/otsu-web