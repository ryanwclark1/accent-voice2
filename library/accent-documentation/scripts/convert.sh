#!/bin/bash

# Find all .puml files and process them
for filename in $(find . -type f -name "*.puml"); do
    # Create a directory for the processed files if it doesn't exist
    mkdir -p processed

    # Process the file content (replace ```plantuml with @startuml and ``` with @enduml)
    result=$(cat "$filename" | sed "s/\`\`\`plantuml/@startuml/" | sed "s/\`\`\`/@enduml/")

    # Get the base name of the file without path
    basename=$(basename "$filename")

    # Write the processed content to a temporary file
    echo "$result" > "processed/$basename"

    # Convert to SVG using Docker
    docker run --rm \
        -v "$(pwd)/processed:/data" \
        plantuml/plantuml:latest \
        -tsvg "/data/$basename"

    # Move the generated SVG to the original directory
    mv "processed/${basename%.*}.svg" "$(dirname "$filename")/"

    # Clean up the temporary file
    rm "processed/$basename"
done

# Remove the temporary directory
rmdir processed