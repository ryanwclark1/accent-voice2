#!/usr/bin/env bash

set -e  # Exit immediately on errors (can be relaxed if needed)
set -o pipefail

# Default values
MAJOR_PYTHON_VERSION=${1:-3.12}  # Use the specified version or default to Python 3.12
LIBRARIES_FILE=${2:-"./libraries.sh"}  # Default to libraries.sh if not provided
SERVICES_FILE=${3:-"./services.sh"}  # Default to services.sh if not provided
LOG_FILE="install_log.txt"

# Initialize logs
echo "Logging to $LOG_FILE"
echo "Poetry Dependency Install Log - $(date)" > "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"

# Initialize counters
LIBRARY_COUNT=0
SERVICE_COUNT=0
SUCCESSFUL_COUNT=0
FAILED_COUNT=0

# Function to check if pyproject.toml is valid
validate_pyproject() {
    local dir=$1
    if [[ ! -f "$dir/pyproject.toml" ]]; then
        return 1  # Not valid if pyproject.toml doesn't exist
    fi
    # Check with poetry if the pyproject.toml is valid
    poetry check --directory "$dir" >/dev/null 2>&1 || {
        # Try to fix with poetry lock --no-update
        echo "Attempting to fix pyproject.toml in $dir with 'poetry lock --no-update'"
        if poetry lock --no-update --directory "$dir" >/dev/null 2>&1; then
            echo "Fixed pyproject.toml in $dir"
            return 0
        else
            echo "Failed to fix pyproject.toml in $dir"
            return 1
        fi
    }
}

# Function to clear virtual environments
# clear_poetry_env() {
#     local dir=$1
#     poetry env remove --all --directory "$dir" >/dev/null 2>&1 || true
# }

# Function to install dependencies
install_dependencies() {
    local dir=$1
    poetry update --directory "$dir" || return 1
    poetry install --directory "$dir" || return 1
}

# Load and parse libraries
if [[ -f "$LIBRARIES_FILE" ]]; then
    echo "Using library file: $LIBRARIES_FILE"
    source "$LIBRARIES_FILE"  # Source the file to use its functions
    LIBRARIES=($(get_library_with_paths))
    LIBRARY_COUNT=${#LIBRARIES[@]}
else
    echo "Error: Libraries file not found at $LIBRARIES_FILE"
    exit 1
fi

# Load and parse services
if [[ -f "$SERVICES_FILE" ]]; then
    echo "Using services file: $SERVICES_FILE"
    source "$SERVICES_FILE"  # Source the file to use its functions
    SERVICES=($(get_service_with_paths))
    SERVICE_COUNT=${#SERVICES[@]}
else
    echo "Error: Services file not found at $SERVICES_FILE"
    exit 1
fi

# Combine libraries and services into a single list
DIRS_TO_PROCESS=("${LIBRARIES[@]}" "${SERVICES[@]}")
TOTAL_COUNT=$((LIBRARY_COUNT + SERVICE_COUNT))

# Process each directory
for dir in "${DIRS_TO_PROCESS[@]}"; do
    echo
    echo "Processing directory: $dir"

    # Ensure directory exists
    if [[ ! -d "$dir" ]]; then
        echo "Directory $dir does not exist. Skipping." | tee -a "$LOG_FILE"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        continue
    fi

    # Check if pyproject.toml is valid
    if ! validate_pyproject "$dir"; then
        echo "Invalid pyproject.toml in $dir. Skipping." | tee -a "$LOG_FILE"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        continue
    fi

    # Clear virtual environment
    # clear_poetry_env "$dir"

    # Try installing dependencies
    if install_dependencies "$dir"; then
        echo "Successful install for $dir" | tee -a "$LOG_FILE"
        SUCCESSFUL_COUNT=$((SUCCESSFUL_COUNT + 1))
    else
        echo "Unsuccessful install for $dir" | tee -a "$LOG_FILE"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        echo "Check poetry logs in $dir for more details." | tee -a "$LOG_FILE"
    fi

    echo "------------------------------------------"  # Add spacing for readability
done

# Summary
echo
echo "Processing complete. Summary:"
echo "======================================="
echo "Libraries processed: $LIBRARY_COUNT"
echo "Services processed: $SERVICE_COUNT"
echo "Total directories processed: $TOTAL_COUNT"
echo "Successful installs: $SUCCESSFUL_COUNT"
echo "Failed installs: $FAILED_COUNT"
echo "=======================================" | tee -a "$LOG_FILE"

echo "Check $LOG_FILE for detailed logs."