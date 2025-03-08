FROM python:3.9-slim-bullseye
MAINTAINER Accent Maintainers <help@accentservices.com>

RUN python3 -m pip install --no-cache-dir flask
COPY accent-auth-mock.py /usr/local/bin/accent-auth-mock.py

EXPOSE 9497

CMD ["/usr/local/bin/accent-auth-mock.py", "9497"]
