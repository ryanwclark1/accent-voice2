#!/bin/bash

if [ $# -ne 1 ]; then
    echo "usage: $(basename "$0") filename"
    exit 1
fi

NAME=$(basename "$1")
SIZE=$(stat -c "%s" "$1")
SHA1SUM=$(sha1sum "$1" | cut -f1 -d' ')

echo "[$NAME]"
echo "url: "
echo "size: $SIZE"
echo "sha1sum: $SHA1SUM"
