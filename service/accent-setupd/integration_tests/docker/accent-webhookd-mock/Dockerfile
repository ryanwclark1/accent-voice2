FROM python:3.9-slim-bullseye

MAINTAINER Accent Maintainers <help@accentservices.com>

COPY requirements.txt /tmp/requirements.txt
RUN true && \
    pip3 install --no-cache-dir flask -r /tmp/requirements.txt && \
    mkdir -p /etc/accent-webhookd/conf.d && \
    true

EXPOSE 9300
COPY accent-webhookd-mock.py /usr/local/bin/accent-webhookd-mock.py
CMD ["/usr/local/bin/accent-webhookd-mock.py", "9300"]
