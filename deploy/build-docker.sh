#!/bin/bash

# Get the absolute path of the script
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

echo "Script location: $SCRIPT_PATH"
echo "Script directory: $SCRIPT_DIR"

# Check if an argument was provided
if [[ $# -eq 1 ]]; then
    # Only use the provided Dockerfile
    DOCKERFILES=("$1")
else
    # Use all Dockerfiles in the directory
    DOCKERFILES=($(find "${SCRIPT_DIR}" -maxdepth 1 -name 'Dockerfile-*' -type f))
fi


# Loop over Dockerfiles in the directory
for dockerfile in "${DOCKERFILES[@]}"; do
    # Extract the name after "Dockerfile-"

    image_name_suffix=$(basename $dockerfile | cut -d'-' -f2)

    # Construct the full image name
    full_image_name="accent-${image_name_suffix}:deploy"

    # Assuming the Dockerfile is in the same directory as the script
    # Build context is two directories up
    BUILD_CONTEXT="$(dirname "$SCRIPT_DIR")"

    echo "Docker build context: $BUILD_CONTEXT"

    # Build the Docker image
    echo "Building image: ${full_image_name}"

    docker build --secret id=github_token,src=$HOME/.gh/token --platform linux/amd64 --pull --rm -f "$dockerfile" -t "accentcommunications/${full_image_name}" "$BUILD_CONTEXT"
    # Building the Docker image
    # docker tag "${full_image_name}" "accentcommunications/${full_image_name}"
    echo "Pushing image: ${full_image_name}"
    docker push accentcommunications/"$full_image_name"
done
