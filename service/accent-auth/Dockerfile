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
    PYSETUP_PATH="/usr/src/accent-auth" \
    VENV_PATH="/usr/src/accent-auth/.venv"

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

COPY ./service/accent-auth/pyproject.toml ./service/accent-auth/poetry.lock ./
COPY ./service/accent-auth/accent_auth/ ./accent_auth/

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-auth/etc /etc
COPY ./service/accent-auth/templates /var/lib/accent-auth/templates

RUN true \
    && adduser --quiet --system --group --home /var/lib/accent-auth accent-auth \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
    libpq5 \
    libldap-2.5-0 \
    libsasl2-2 \
    libssl3 \
    && mkdir -p /etc/accent-auth/conf.d \
    && mkdir -p /etc/accent-auth/templates.d \
    && install -o accent-auth -g accent-auth /dev/null /var/log/accent-auth.log \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9497

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-auth", "--db-upgrade-on-startup"]