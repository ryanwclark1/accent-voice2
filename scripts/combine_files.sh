#!/usr/bin/env bash
# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine the project directory (assuming the script is in a subdirectory of the project)
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Define the search directory and output file
SEARCH_DIR="$PROJECT_DIR/library/accent-lib-rest-client/accent_lib_rest_client/"
OUTPUT_FILE="$PROJECT_DIR/scripts/accent-lib-rest-client.txt"
GITIGNORE_FILE="$PROJECT_DIR/scripts/.gitignore"

# Check if the search directory exists
if [ ! -d "$SEARCH_DIR" ]; then
    echo "Directory '$SEARCH_DIR' does not exist. Exiting."
    exit 1
fi

# Check if the .gitignore file exists in the current directory
if [ ! -f "$GITIGNORE_FILE" ]; then
    echo "No .gitignore file found in the current directory. Exiting."
    exit 1
fi

# Clear or create the output file
> "$OUTPUT_FILE"

# Initialize counters
TOTAL_FILES=0
TOTAL_DIRECTORIES=0

# Count directories
TOTAL_DIRECTORIES=$(find "$SEARCH_DIR" -type d | wc -l)

# Use find and grep to respect .gitignore for both .html and .js files
find "$SEARCH_DIR" -type f \( -name "*.py" -o -name "*.html" \) | grep -v -Ff "$GITIGNORE_FILE" | while read -r file; do
    # Increment file counter
    ((TOTAL_FILES++))

    # Get the relative path of the file
    RELATIVE_PATH=$(realpath --relative-to="$SEARCH_DIR" "$file")

    # Append the relative path and custom text to the output file
    echo "File: $RELATIVE_PATH" >> "$OUTPUT_FILE"
    echo "Please review for update" >> "$OUTPUT_FILE"
    echo >> "$OUTPUT_FILE"

    # Append the file content to the output file
    cat "$file" >> "$OUTPUT_FILE"

    # Separate files with a newline
    echo >> "$OUTPUT_FILE"
    echo "----------------------------------------" >> "$OUTPUT_FILE"
    echo >> "$OUTPUT_FILE"
done

# Print summary to stdout
echo "Processing complete."
echo "Total files processed: $TOTAL_FILES"
echo "Total directories scanned: $TOTAL_DIRECTORIES"
echo "Results saved to: $OUTPUT_FILE"
