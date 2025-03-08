#!/bin/bash

# Function to clean up temporary files
cleanup() {
    echo -e "\nCleaning up..."
    [ -d "$SCRIPT_DIR/processed" ] && rm -rf "$SCRIPT_DIR/processed"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# If a path is provided use it, otherwise use the script's directory
SEARCH_PATH="${1:-$SCRIPT_DIR}"

# Ensure the path exists
if [ ! -d "$SEARCH_PATH" ]; then
    echo "Error: Directory '$SEARCH_PATH' does not exist"
    exit 1
fi

# Create a directory for the processed files if it doesn't exist
mkdir -p "$SCRIPT_DIR/processed"

echo "Searching for PUML files in: $SEARCH_PATH"

# Find all .puml files and process them
find "$SEARCH_PATH" -type f -name "*.puml" | while read filename; do
    echo "Processing: $filename"

    # Get the absolute path of the file
    abs_path=$(realpath "$filename")

    # Get the base name of the file without path
    basename=$(basename "$filename")

    # Process the file content:
    # - replace ```plantuml with @startuml
    # - replace ``` with @enduml
    # - remove !include C4_Container.puml
    cat "$abs_path" > "$SCRIPT_DIR/processed/$basename"

    # Convert to SVG using Docker
    # Note: PlantUML will automatically overwrite existing SVG files
    docker run --rm \
        -v "$SCRIPT_DIR/processed:/data" \
        plantuml/plantuml:latest \
        -tsvg "/data/$basename"

    # Force overwrite if SVG already exists
    mv -f "$SCRIPT_DIR/processed/${basename%.*}.svg" "$(dirname "$abs_path")/"

    # Clean up the temporary file
    rm "$SCRIPT_DIR/processed/$basename"
done

# Clean up the temporary directory
cleanup