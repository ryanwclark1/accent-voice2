## Running unit tests

```
apt-get install libpq-dev python3-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py3
```

## Docker

The official docker image for this service is `accentcommunications/accent-agentd`.

### Getting the image

To download the latest image from the docker hub

```shell
docker pull accentcommunications/accent-agentd
```

### Running accent-agentd

```shell
docker run accentcommunications/accent-agentd
```

### Building the image

Building the docker image:

```shell
docker build -t accentcommunications/accent-agentd .
```
