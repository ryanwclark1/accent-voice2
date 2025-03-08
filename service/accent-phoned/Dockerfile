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
    PYSETUP_PATH="/usr/src/accent-phoned" \
    VENV_PATH="/usr/src/accent-phoned/.venv"

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

COPY ./service/accent-phoned/pyproject.toml ./service/accent-phoned/poetry.lock ./
COPY ./service/accent-phoned/accent_phoned ./accent_phoned

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-phoned/etc/accent-phoned /etc/accent-phoned
COPY ./service/accent-phoned/contribs/docker/certs /usr/share/accent-certs

RUN true \
    && adduser --quiet --system --group --home /var/lib/accent-phoned accent-phoned \
    && mkdir -p /etc/accent-phoned/conf.d \
    && install -o www-data -g www-data /dev/null /var/log/accent-phoned.log

WORKDIR $PYSETUP_PATH

EXPOSE 9498 9499

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-phoned", "-d"]