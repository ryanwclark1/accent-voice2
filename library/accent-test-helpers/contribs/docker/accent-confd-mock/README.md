# accent-confd mock

This is the required files to build a docker image to be used as a accent-confd mock
for integration tests.

## Usage

This mock exposes an interface similar to the official accent-confd with a few exceptions.

1. New endpoints have been added to customize the responses:

* `POST /_set_response`
* `GET /_requests`
* `POST /_reset`
