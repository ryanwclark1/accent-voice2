FROM python:3.9-slim-bullseye

MAINTAINER Accent Maintainers <help@accentservices.com>

RUN pip3 install --no-cache-dir flask

COPY accent-deployd-mock.py /usr/local/bin/accent-deployd-mock.py
COPY server.crt /usr/local/share/ssl/deployd/server.crt
COPY server.key /usr/local/share/ssl/deployd/server.key

EXPOSE 9800

CMD ["/usr/local/bin/accent-deployd-mock.py", "9800"]
