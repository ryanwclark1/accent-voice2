FROM debian:bookworm-slim

LABEL maintainer="Ryan Clark <ryanc@accentservices.com>"

ENV ASTERISK_VERSION="20.5.0"
ENV OPUS_CODEC="asterisk-20.0/x86-64/codec_opus-20.0_current-x86_64"

COPY ./deploy/asterisk/build-asterisk.sh /
COPY ./deploy/asterisk/docker-entrypoint.sh /
COPY ./service/accent-res-stasis-amqp /usr/src/accent-res-stasis-amqp
COPY ./service/accent-res-amqp /usr/src/accent-res-amqp
COPY ./library/accent-asterisk-config/etc/asterisk /etc/accent-asterisk-config

RUN --mount=type=secret,id=github_token \
    export GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    ./build-asterisk.sh

VOLUME /var/lib/asterisk/sounds /var/lib/asterisk/keys /var/lib/asterisk/phoneprov /var/spool/asterisk /var/log/asterisk

# EXPOSE 2000 5038 5060/udp
EXPOSE 2000 5060/udp 5060/tcp 5061/tcp 5038/tcp 5039/tcp
ENV PATH="/usr/sbin:$PATH"
ENTRYPOINT ["/docker-entrypoint.sh"]
