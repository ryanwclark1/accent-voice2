###############################################
# Base Image
###############################################
FROM postgres:15-bookworm
LABEL maintainer="Ryan Clark <ryanc@accentservices.com>"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/usr/src/accent-manage-db" \
    VENV_PATH="/usr/src/accent-manage-db/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

COPY ./service/accent-manage-db/ ./

RUN true \
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    python-is-python3 \
    python3 \
    python3-dev \
    curl \
    build-essential \
    ca-certificates \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install --without=dev


# COPY ./service/accent-manage-db/pyproject.toml ./service/accent-manage-db/poetry.lock ./
# COPY ./service/accent-manage-db/accent_manage_db/ ./accent_manage_db/

# RUN alias python='python3' \
#     && poetry install --without=dev

###############################################
# Production Image
###############################################
# FROM postgres:15-bookworm AS production
FROM debian:bookworm AS production
COPY --from=builder-base /opt/pysetup/.venv/bin/ /usr/local/bin/

COPY ./service/accent-manage-db/populate/ /usr/share/accent-manage-db/populate/
COPY ./service/accent-manage-db/alembic/ /usr/share/accent-manage-db/alembic/
COPY ./service/accent-manage-db/alembic.ini /usr/share/accent-manage-db/alembic.ini
COPY ./service/accent-manage-db/bin/ /usr/local/bin/

ENV PATH="/usr/local/bin:$PATH"

RUN cp /usr/src/accent-manage-db/.venv/bin/ /usr/local/bin/
COPY ./service/accent-manage-db/ /usr/src/accent-manage-db
WORKDIR /usr/src/accent-manage-db

RUN true \
    && accent-configure-uuid \
    && mkdir /usr/share/accent-manage-db /usr/lib/accent-manage-db \
    && cp -a alembic alembic.ini populate /usr/share/accent-manage-db \
    && ln -s /usr/local/bin/pg-populate-db /usr/lib/accent-manage-db/pg-populate-db \
    && pg_start \
    && alembic -c alembic.ini branches \
    && alembic -c alembic.ini show head \
    && accent-init-db --init \
    && alembic -c alembic.ini branches \
    && alembic -c alembic.ini show head \
    && pg_stop \
    && rm -rf /usr/src/accent-manage-db /var/lib/apt/lists/*
# USER postgres


# EXPOSE 5432
# CMD ["/usr/lib/postgresql/15/bin/postgres", "-D", "/var/lib/postgresql/15/main", "--config-file=/etc/postgresql/15/main/postgresql.conf"]

# CMD ["bin/sh"]
ENTRYPOINT ["/bin/bash"]

