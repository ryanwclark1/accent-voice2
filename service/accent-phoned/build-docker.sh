
# Get the absolute path of the script
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

echo "Script location: $SCRIPT_PATH"
echo "Script directory: $SCRIPT_DIR"

# Get the base name of the script directory
BASE_DIR_NAME="$(basename "$SCRIPT_DIR")"

echo "Base directory name: $BASE_DIR_NAME"

# Assuming the Dockerfile is in the same directory as the script
# Build context is two directories up
BUILD_CONTEXT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "Docker build context: $BUILD_CONTEXT"

# Building the Docker image
docker build --platform linux/amd64 --pull --rm -f "Dockerfile" -t "accentcommunications/${BASE_DIR_NAME}:latest" "$BUILD_CONTEXT"
# docker build --platform linux/amd64 --pull --rm -f "Dockerfile" -t "${BASE_DIR_NAME}:latest" "$BUILD_CONTEXT"
# docker tag "$BASE_DIR_NAME":latest accentcommunications/"$BASE_DIR_NAME":latest
docker push accentcommunications/"$BASE_DIR_NAME":latest