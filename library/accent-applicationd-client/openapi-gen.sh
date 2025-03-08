#!/bin/bash

docker run --net=host --rm -v ${PWD}:/accent-applicationd-client openapitools/openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python --package-name accent_applicationd_client -o /accent-applicationd-client

sudo chown -R $UID:$UID $PWD
