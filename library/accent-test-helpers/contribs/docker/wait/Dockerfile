FROM debian:bullseye-slim
LABEL maintainer="Accent Maintainers <help@accentservices.com>"

RUN apt-get -q update && apt-get install -yq netcat

ADD wait /wait

CMD ["/wait"]
