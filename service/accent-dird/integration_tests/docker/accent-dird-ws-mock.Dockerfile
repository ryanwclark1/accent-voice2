FROM python:3.9-slim-bullseye AS compile-image
LABEL maintainer="Accent Maintainers <help@accentservices.com>"

RUN pip install flask
