#!/bin/bash

# If the line doesn't start with "; ", prefix it with "; "

find ../library/accent-asterisk-config/etc/asterisk -type f -name "sample.conf" | while read -r file; do
    awk '
        {
            if ($0 && !/^; /) {
                print "; " $0
            } else {
                print $0
            }
        }
        ' "$file" > "${file}.tmp"
        mv "${file}.tmp" "$file"
    done