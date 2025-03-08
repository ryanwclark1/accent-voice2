#!/usr/bin/env bash

set -e  # Exit immediately on errors (can be relaxed if needed)
set -o pipefail

# Default values
MAJOR_PYTHON_VERSION=${1:-3.12}  # Use the specified version or default to Python 3.12
DIRS_FILE=${2:-"directories.sh"}  # Default directories file
LOG_FILE="install_log.txt"

# Initialize logs
echo "Logging to $LOG_FILE"
echo "Poetry Dependency Install Log - $(date)" > "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"

# Function to check if pyproject.toml is valid
validate_pyproject() {
    local dir=$1
    if [[ ! -f "$dir/pyproject.toml" ]]; then
        return 1  # Not valid if pyproject.toml doesn't exist
    fi
    # Check with poetry if the pyproject.toml is valid
    poetry check --directory "$dir" >/dev/null 2>&1
}

# Function to clear virtual environments
clear_poetry_env() {
    local dir=$1
    poetry env remove --all --directory "$dir" >/dev/null 2>&1 || true
}

# Function to install dependencies
install_dependencies() {
    local dir=$1
    poetry install --directory "$dir" || return 1
}

# Load and parse services
if [[ -f "$SERVICES_FILE" ]]; then
    echo "Using services file: $SERVICES_FILE"
    source "$SERVICES_FILE"  # Source the file to use its functions
    DIRS_TO_PROCESS=($(get_service_with_paths))
else
    echo "Error: Services file not found at $SERVICES_FILE"
    exit 1
fi

# Process each directory
for dir in "${DIRS_TO_PROCESS[@]}"; do
    echo "Processing directory: $dir"

    # Ensure directory exists
    if [[ ! -d "$dir" ]]; then
        echo "Directory $dir does not exist. Skipping." | tee -a "$LOG_FILE"
        continue
    fi

    # Check if pyproject.toml is valid
    if ! validate_pyproject "$dir"; then
        echo "Invalid pyproject.toml in $dir. Skipping." | tee -a "$LOG_FILE"
        continue
    fi

    # Clear virtual environment
    clear_poetry_env "$dir"

    # Try installing dependencies
    if install_dependencies "$dir"; then
        echo "Successful install for $dir" | tee -a "$LOG_FILE"
    else
        echo "Unsuccessful install for $dir" | tee -a "$LOG_FILE"
        echo "Check poetry logs in $dir for more details." | tee -a "$LOG_FILE"
    fi
done

echo "Processing complete. Check $LOG_FILE for details."