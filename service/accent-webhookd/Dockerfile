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
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_NO_INTERACTION=true \
    PYSETUP_PATH="/usr/src/accent-webhookd" \
    VENV_PATH="/usr/src/accent-webhookd/.venv"

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
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

COPY ./service/accent-webhookd/pyproject.toml ./service/accent-webhookd/poetry.lock ./
COPY ./service/accent-webhookd/accent_webhookd ./accent_webhookd
COPY ./service/accent-webhookd/alembic ./alembic
COPY ./service/accent-webhookd/alembic.ini ./

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-webhookd/etc /etc

RUN true \
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    && adduser --quiet --system --group accent-webhookd \
    && mkdir -p /etc/accent-webhookd/conf.d \
    && install -o accent-webhookd -g accent-webhookd -d /run/accent-webhookd \
    && install -o accent-webhookd -g accent-webhookd /dev/null /var/log/accent-webhookd.log \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9300

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-webhookd"]
