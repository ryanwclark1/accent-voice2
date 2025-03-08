#!/bin/bash

# Directory to check
dir="../library/accent-asterisk-config/etc/asterisk"

# Iterate over all subdirectories in the given directory
for subdir in "$dir"/*; do
    # Check if it's a directory
    if [[ -d "$subdir" ]]; then
        # Extract the base name of the subdirectory (e.g., acl from acl.d)
        base_name=$(basename "$subdir" .d)

        # Construct the conf file name
        conf_file="$dir/$base_name.conf"

        # Check if the conf file does not exist
        if [[ ! -f "$conf_file" ]]; then
            # If it doesn't exist, create it and add the specified text
            echo "; This file is part of the Accent packaging and should not be modified." > "$conf_file"
            echo "; Add files to the $base_name.d directory if you wish to modify your $base_name.conf" >> "$conf_file"
            echo "#include $base_name.d/*.conf" >> "$conf_file"
            echo "Info: '$conf_file' created."
        fi
    fi
done