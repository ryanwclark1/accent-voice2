FROM python:3.9-slim-bullseye
MAINTAINER Accent Maintainers <help@accentservices.com>

RUN python3 -m pip install --no-cache-dir flask
COPY mock-accent-confd.py /usr/local/bin/mock-accent-confd.py

EXPOSE 9486

CMD ["/usr/local/bin/mock-accent-confd.py", "9486"]
