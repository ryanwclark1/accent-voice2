FROM python:3.12-slim-bookworm
LABEL maintainer="Ryan Clark <ryanc@accentservices.com>"

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    BUILD_PACKAGES="libpq-dev gcc libc6-dev" \
    PYTHON_PACKAGES="alembic==1.13.0 psycopg2-binary==2.8.6 sqlalchemy==1.3.22 sqlalchemy-utils==0.37.2 ../../library/accent-lib-python" \
    PG_PACKAGES="postgresql-15 postgresql-contrib-15 postgresql-client-15"
    # PYSETUP_PATH="/usr/src/accent-base-db"

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

#Locales must be configured before installing postgres, otherwise the database encoding defaults to SQL_ASCII
RUN true \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
        sudo \
        locales \
        python3-poetry-core \
    && dpkg-reconfigure locales \
    && locale-gen C.UTF-8  \
    && /usr/sbin/update-locale LANG=C.UTF-8 \
    && apt-get -yq install --no-install-recommends $PG_PACKAGES \
    && echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/15/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/15/main/postgresql.conf \
    && mkdir -p /run/postgresql/15-main.pg_stat_tmp \
    && chown -R postgres:postgres /run/postgresql \
    && apt-get -yq install --no-install-recommends $BUILD_PACKAGES \
    && pip install $PYTHON_PACKAGES \
    && rm -rf ../../library \
    && rm -rf /var/lib/apt/lists/* \
    && true

COPY ./service/accent-manage-db/contribs/docker/accent-base-db/pg_start ./service/accent-manage-db/contribs/docker/accent-base-db/pg_stop /usr/local/bin/

EXPOSE 5432
CMD ["/usr/lib/postgresql/15/bin/postgres", "-D", "/var/lib/postgresql/15/main", "--config-file=/etc/postgresql/15/main/postgresql.conf"]
