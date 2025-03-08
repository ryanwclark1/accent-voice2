FROM golang:1.21 AS builder-base

WORKDIR /app
COPY . .

# BUILD the go binary
RUN go build -o ./bin/accent-prov-server .

FROM debian:bookworm-slim AS production
COPY --from=builder-base /app/bin/accent-prov-server usr/bin/accent-prov-server

EXPOSE 8080

VOLUME /files
ENTRYPOINT [ "accent-prov-server" ]
