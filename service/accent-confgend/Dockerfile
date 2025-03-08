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
    PYSETUP_PATH="/usr/src/accent-confgend" \
    VENV_PATH="/usr/src/accent-confgend/.venv"

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

COPY ./service/accent-confgend/pyproject.toml ./service/accent-confgend/poetry.lock ./
COPY ./service/accent-confgend/accent_confgend ./accent_confgend
COPY ./service/accent-confgend/bin ./bin

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-confgend/etc /etc

RUN true\
    && apt-get update -qq  \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    && adduser --quiet --system --group --home /var/lib/accent-confgend accent-confgend \
    && mkdir -p /etc/accent-confgend/conf.d \
    && install -D -o accent-confgend -g accent-confgend /dev/null /var/log/accent-confgend.log \
    && install -d -o accent-confgend -g accent-confgend /var/cache/accent-confgend \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 8668

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-confgend"]
