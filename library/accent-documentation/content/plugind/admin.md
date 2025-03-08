## Docker

The official docker image for this service is `accentcommunications/accent-plugind`.

### Getting the image

To download the latest image from the docker hub

```shell
docker pull accentcommunications/accent-plugind
```

### Running accent-plugind

```shell
docker run -e"ACCENT_UUID=<the accent UUID>" accentcommunications/accent-plugind
```

### Building the image

Building the docker image:

```shell
docker build -t accentcommunications/accent-plugind .
```
