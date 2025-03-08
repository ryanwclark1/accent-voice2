#!/usr/bin/env bash

# Source the services.sh script to get access to its functions
source "$(dirname "${BASH_SOURCE[0]}")/services.sh"

# Get the services with paths from the original script
services_array=($(get_service_with_paths))

# Function to format and validate each service directory
format_service_directories() {
    local success=true

    for service_path in "${services_array[@]}"; do
        # Skip if empty
        [ -z "$service_path" ] && continue

        # Create directory if it doesn't exist
        if [ ! -d "$service_path" ]; then
            echo "Creating directory: $service_path"
            mkdir -p "$service_path"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to create directory $service_path" >&2
                success=false
                continue
            fi
        fi

        # Normalize path (remove any double slashes, etc.)
        normalized_path=$(realpath --relative-to="$BASE_PATH" "$service_path")

        # Verify the directory exists and is accessible
        if [ -d "$service_path" ] && [ -r "$service_path" ]; then
            echo "✓ Verified: $normalized_path"
        else
            echo "✗ Error: Cannot access $normalized_path" >&2
            success=false
        fi
    done

    if [ "$success" = true ]; then
        echo -e "\nAll service directories have been processed successfully."
        return 0
    else
        echo -e "\nSome errors occurred while processing directories." >&2
        return 1
    fi
}

# Main execution
echo "Starting directory format verification..."
echo "Base path: $BASE_PATH"
echo "Processing ${#services_array[@]} services..."
echo "-------------------------------------------"

format_service_directories
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "Directory structure is now properly formatted."
else
    echo "Some errors occurred during formatting. Please check the output above." >&2
fi

exit $exit_code