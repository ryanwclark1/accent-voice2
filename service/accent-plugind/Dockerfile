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
    PYSETUP_PATH="/usr/src/plugind" \
    VENV_PATH="/usr/src/plugind/.venv"

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

COPY ./service/accent-plugind/pyproject.toml ./service/accent-plugind/poetry.lock ./
COPY ./service/accent-plugind/accent_plugind/ ./accent_plugind/
COPY ./service/accent-plugind/bin ./bin
# Copy bin file ensure PATH -> Entrypoint?

RUN true \
    && poetry add pyparsing \
    && poetry add appdirs \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-plugind/etc /etc
COPY ./service/accent-plugind/templates /usr/lib/accent-plugind/templates

RUN true \
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    apt-utils \
    fakeroot \
    gdebi-core \
    git \
    wget \
    gnupg \
    && adduser --quiet --system --group --home /var/lib/accent-plugind accent-plugind \
    && mkdir -p /etc/accent-plugind/conf.d \
    && install -m 755 -d -o accent-plugind -g accent-plugind /var/lib/accent-plugind/rules \
    && install -d -o accent-plugind -g accent-plugind /var/lib/accent-plugind/downloads \
    && install -o accent-plugind -g accent-plugind /dev/null /var/log/accent-plugind.log \
    && chown -R accent-plugind:accent-plugind /usr/lib/accent-plugind \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9503

ENV PATH="$VENV_PATH/bin:$PYSETUP_PATH/bin:$PATH"
CMD [ "accent-plugind" ]