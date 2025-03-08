FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -q update && apt-get -q -y install \
    apt-utils \
    gnupg \
    wget

RUN apt-get -q update && apt-get -q -y install \
    accent-libsccp \
    git \
    make \
    gcc \
    g++ \
    asterisk \
    libedit-dev \
    jq \
    accent-res-amqp

RUN  apt-get install --assume-yes openssl libxml2-dev libncurses5-dev uuid-dev sqlite3 libsqlite3-dev pkg-config libjansson-dev

RUN apt-get install --assume-yes asterisk-dev accent-res-amqp-dev librabbitmq-dev

COPY . /usr/src/accent-res-stasis-amqp
WORKDIR /usr/src/accent-res-stasis-amqp
RUN make && \
    make install DOCDIR=/usr/share/asterisk/documentation/thirdparty
RUN cp amqp.json /usr/share/asterisk/rest-api
RUN bin/patch_ari_resources.sh

EXPOSE 2000 5038 5039 5060/udp

CMD ["asterisk", "-dvf"]
