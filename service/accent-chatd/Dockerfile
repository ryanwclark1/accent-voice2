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
    PYSETUP_PATH="/usr/src/accent-chatd" \
    VENV_PATH="/usr/src/accent-chatd/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base AS builder-base

RUN true \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

COPY ./service/accent-chatd/pyproject.toml ./service/accent-chatd/poetry.lock ./
COPY ./service/accent-chatd/accent_chatd ./accent_chatd
COPY ./service/accent-chatd/alembic ./alembic
COPY ./service/accent-chatd/alembic.ini ./

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-chatd/etc /etc

RUN true \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
    libpq5 \
    && adduser --quiet --system --group --home /var/lib/accent-chatd accent-chatd \
    && mkdir -p /etc/accent-chatd/conf.d \
    && install -o accent-chatd -g accent-chatd /dev/null /var/log/accent-chatd.log \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9304

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-chatd"]