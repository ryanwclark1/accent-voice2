###############################################
# Base Image
###############################################
FROM python:3.9-slim-bookworm AS python-base
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
    PYSETUP_PATH="/usr/src/accent-websocketd" \
    VENV_PATH="/usr/src/accent-websocketd/.venv"

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
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

# TODO: Running Python 3.9.17 -> UVLOOP 0.15.3 doesn't run on 3.10+
COPY ./service/accent-websocketd/pyproject.toml ./service/accent-websocketd/poetry.lock ./
COPY ./service/accent-websocketd/accent_websocketd/ ./accent_websocketd/

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-websocketd/etc /etc

# Contribs?
RUN true \
    && adduser --quiet --system --group accent-websocketd \
    && mkdir -p /etc/accent-websocketd/conf.d \
    && install -o accent-websocketd -g accent-websocketd -d /run/accent-websocketd \
    && install -o accent-websocketd -g accent-websocketd /dev/null /var/log/accent-websocketd.log

WORKDIR $PYSETUP_PATH

EXPOSE 9502

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-websocketd"]
