FROM accentcommunications/accent-confd-db
LABEL maintainer="Accent Maintainers <help@accentservices.com>"

USER root
ENV PG_CONF="/etc/postgresql/15/main/postgresql.conf"

#Insert data required for running integration tests
COPY contribs/docker/accent-confd-db-test/initdb.sql /usr/src/initdb.sql
COPY alembic /usr/share/accent-manage-db/alembic
COPY contribs/docker/accent-confd-db-test/bootstrap-pg.sh /bootstrap-pg.sh

ADD https://github.com/tianon/gosu/releases/download/1.16/gosu-amd64 /usr/local/bin/gosu

RUN true \
    && mkdir -p /pg-init-db \
    && sed -i 's/#fsync.*/fsync = off/g' $PG_CONF \
    && pg_start \
    && sudo -u postgres psql asterisk < /usr/src/initdb.sql \
    && cd /usr/share/accent-manage-db \
    && alembic -c alembic.ini branches \
    && alembic -c alembic.ini show head \
    && accent-update-db \
    && alembic -c alembic.ini branches \
    && alembic -c alembic.ini show head \
    && sudo -u postgres psql asterisk -c "CREATE DATABASE accenttemplate TEMPLATE asterisk;" \
    && pg_stop \
    && chmod +x /usr/local/bin/gosu

ENTRYPOINT ["/bootstrap-pg.sh"]
