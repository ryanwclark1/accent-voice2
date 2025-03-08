#!/bin/bash

# Get the current directory name
current_dir=$(basename "$(pwd)")

# Navigate two directories up
build_context=$(realpath ../../)

# Build the Docker image using the current directory as the image name
DOCKER_BUILDKIT=1 docker build --secret id=github_token,src=$HOME/.gh/token --platform linux/amd64 --pull --rm -f "Dockerfile" -t "accentcommunications/accent-$current_dir:latest" "$build_context"
# docker tag "$current_dir":latest accentcommunications/"$current_dir":latest
docker push accentcommunications/accent-"$current_dir":latest