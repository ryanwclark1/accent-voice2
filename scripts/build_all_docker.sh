#!/bin/bash

# Get the directory where the current script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source the list of services
source "$SCRIPT_DIR/docker_services.sh"

# Root of the entire service
SERVICE_ROOT="$SCRIPT_DIR/.."

# Loop through each service
for SERVICE in "${SERVICES[@]}"; do
    # Construct full path to service directory
    DIR="$SCRIPT_DIR/../service/$SERVICE"

    echo "Processing service: $DIR"

    # Check if the directory has build-docker.sh
    if [ -f "$DIR/build-docker.sh" ]; then
        echo "Using build-docker.sh in $DIR"
        (cd "$DIR" && bash build-docker.sh)
    else
        # Use the provided script content to build Docker image
        echo "Using default build process for $DIR"

        # Get the base name of the service directory
        BASE_DIR_NAME="$(basename "$DIR")"

        # Building the Docker image with the root of the service as the build context
        docker build --platform linux/amd64 --pull --no-cache --rm -f "Dockerfile" -t "accentcommunications/${BASE_DIR_NAME}:latest" "$BUILD_CONTEXT"
        # docker build --platform linux/amd64 --pull --rm -f "$DIR/Dockerfile" -t "${BASE_DIR_NAME}:latest" "$SERVICE_ROOT"
        # docker tag "${BASE_DIR_NAME}:latest" accentcommunications/"${BASE_DIR_NAME}:latest"
        docker push accentcommunications/"${BASE_DIR_NAME}:latest"
    fi
done

