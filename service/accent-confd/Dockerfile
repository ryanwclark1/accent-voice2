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
    PYSETUP_PATH="/usr/src/accent-confd" \
    VENV_PATH="/usr/src/accent-confd/.venv"

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

COPY ./service/accent-confd/pyproject.toml ./service/accent-confd/poetry.lock ./
COPY ./service/accent-confd/accent_confd ./accent_confd

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-confd/etc /etc

RUN true \
    && apt-get -q update \
    && apt-get -yq install --no-install-recommends \
    libpq5 \
    && mkdir -p /etc/accent-confd/conf.d \
    && install -o www-data -g www-data /dev/null /var/log/accent-confd.log \
    && install -d -o www-data -g www-data /var/lib/asterisk/moh \
    && install -dm775 -o www-data -g www-data /var/lib/accent/sounds/tenants \
    && install -dm777 /usr/share/asterisk/sounds \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 9486

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-confd", "-d"]