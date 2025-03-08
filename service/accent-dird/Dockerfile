###############################################
# Base Image
###############################################
FROM python:3.12-slim-bookworm AS python-base
LABEL maintainer="Ryan Clark <ryanc@accentservices.com>"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=true \
    PYSETUP_PATH="/usr/src/accent-dird" \
    VENV_PATH="/usr/src/accent-dird/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base AS builder-base

RUN true \
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libc6-dev \
    libpq-dev \
    libldap-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

COPY ./service/accent-dird/pyproject.toml ./service/accent-dird/poetry.lock ./
COPY ./service/accent-dird/accent_dird/ ./accent_dird/
COPY ./service/accent-dird/alembic ./alembic
COPY ./service/accent-dird/alembic.ini ./
COPY ./service/accent-dird/bin ./bin

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY  ./service/accent-dird/etc /etc

RUN true \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
    libpq5 \
    libldap-2.5-0 \
    && mkdir -p /etc/accent-dird/conf.d \
    && mkdir -p /etc/accent-dird/templates.d \
    && install -o www-data -g www-data /dev/null /var/log/accent-dird.log \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9489

ENV PATH="$VENV_PATH/bin:$PYSETUP_PATH/bin:$PATH"
CMD ["accent-dird", "-d"]