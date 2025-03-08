FROM python:3.9-slim-bullseye
MAINTAINER Accent Maintainers <help@accentservices.com>

RUN python3 -m pip install --no-cache-dir flask
COPY mock-accent-amid.py /usr/local/bin/mock-accent-amid.py

EXPOSE 9491

CMD ["/usr/local/bin/mock-accent-amid.py", "9491"]
