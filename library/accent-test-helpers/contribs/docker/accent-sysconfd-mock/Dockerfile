FROM python:3.9-slim-bullseye
MAINTAINER Accent Maintainers <help@accentservices.com>

RUN python3 -m pip install --no-cache-dir flask
COPY accent-sysconfd-mock.py /usr/local/bin/accent-sysconfd-mock.py

EXPOSE 8668

CMD ["/usr/local/bin/accent-sysconfd-mock.py", "8668"]
