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
    PYSETUP_PATH="/usr/src/accent-agid" \
    VENV_PATH="/usr/src/accent-agid/.venv"

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

COPY ./service/accent-agid/pyproject.toml ./service/accent-agid/poetry.lock ./
COPY ./service/accent-agid/accent_agid ./accent_agid
COPY ./service/accent-agid/bin/ ./bin

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-agid/etc /etc

RUN true \
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    && adduser --disabled-password --gecos '' asterisk \
    && adduser --quiet --system --group --home /var/lib/accent-agid accent-agid \
    && mkdir -p /etc/accent-agid/conf.d \
    && mkdir -p /etc/accent \
    && install -D -o root -g root /dev/null /var/log/accent-agid.log \
    && install -D -o root -g root /dev/null /etc/accent/asterisk/accent_ring.conf \
    && install -D -o root -g root /dev/null /etc/accent/asterisk/accent_fax.conf \
    && install -D -o root -g root /dev/null /etc/accent/asterisk/accent_in_callerid.conf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 4573

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-agid"]
