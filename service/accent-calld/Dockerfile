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
    PYSETUP_PATH="/usr/src/accent-calld" \
    VENV_PATH="/usr/src/accent-calld/.venv"

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

COPY ./service/accent-calld/pyproject.toml ./service/accent-calld/poetry.lock ./
COPY ./service/accent-calld/accent_calld ./accent_calld

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-calld/etc /etc
COPY ./service/accent-calld/bin/accent-pdf2fax /usr/bin/accent-pdf2fax

RUN true \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
    ghostscript \
    && adduser --quiet --system --group --home /var/lib/accent-calld accent-calld \
    && mkdir -p /etc/accent-calld/conf.d \
    && mkdir -p /var/spool/asterisk/voicemail \
    && install -o www-data -g www-data /dev/null /var/log/accent-calld.log \
    && chown root:www-data /usr/bin/accent-pdf2fax \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9500

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-calld"]