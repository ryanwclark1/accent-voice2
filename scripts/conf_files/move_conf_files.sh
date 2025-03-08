#!/bin/bash

# The source and destination directories
src_dir="./"
dst_dir="../library/accent-asterisk-config/etc/asterisk"

# Iterate over *.conf files in the source directory
for file in "$src_dir"/*.conf; do
    # If no .conf files are found, continue
    [ -e "$file" ] || continue
    
    # Extract the filename without the path and extension
    base_name=$(basename "$file" .conf)
    
    # Create the destination subdirectory if it doesn't exist
    mkdir -p "$dst_dir/$base_name.d"
    
    # Destination file path
    dest_file="$dst_dir/$base_name.d/sample.conf"
    
    # If a file with the same name doesn't already exist at the destination, move the file
    if [ ! -e "$dest_file" ]; then
        mv "$file" "$dest_file"
    else
        echo "Warning: '$dest_file' already exists. Skipping '$file'."
    fi
done