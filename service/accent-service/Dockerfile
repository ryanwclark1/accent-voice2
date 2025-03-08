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
    PYSETUP_PATH="/usr/src/accent-service" \
    VENV_PATH="/usr/src/accent-service/.venv"

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

COPY ./service/accent-service/pyproject.toml ./service/accent-service/poetry.lock ./
COPY ./service/accent-service/accent_service ./accent_service

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-service/etc/accent-service /etc/accent-service
COPY ./service/accent-service/contribs/docker/certs /usr/share/accent-certs

RUN true \
    && adduser --quiet --system --group --home /var/lib/accent-service accent-service \
    && mkdir -p /etc/accent-service/conf.d \
    && install -o www-data -g www-data /dev/null /var/log/accent-service.log

WORKDIR $PYSETUP_PATH

EXPOSE 9498 9499

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-service", "-d"]