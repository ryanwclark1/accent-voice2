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
    PYSETUP_PATH="/usr/src/accent-setupd" \
    VENV_PATH="/usr/src/accent-setupd/.venv"

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

COPY ./service/accent-setupd/pyproject.toml ./service/accent-setupd/poetry.lock ./
COPY ./service/accent-setupd/accent_setupd/ ./accent_setupd/

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-setupd/etc /etc

RUN true\
    && adduser --quiet --system --group --home /var/lib/accent-setupd accent-setupd \
    && mkdir -p /etc/accent-auth/conf.d \
    && mkdir -p /etc/accent-nestbox-plugin/conf.d \
    && mkdir -p /etc/accent-setupd/conf.d \
    && mkdir -p /etc/accent-webhookd/conf.d \
    && mkdir -p /usr/share/accent-setupd \
    && install -m 0640 -o accent-setupd -g root /dev/null /usr/share/accent-setupd/50-accent-plugin-nestbox.yml \
    && ln -s /usr/share/accent-setupd/50-accent-plugin-nestbox.yml /etc/accent-auth/conf.d/50-accent-plugin-nestbox.yml \
    && ln -s /usr/share/accent-setupd/50-accent-plugin-nestbox.yml /etc/accent-nestbox-plugin/conf.d/50-accent-plugin-nestbox.yml \
    && ln -s /usr/share/accent-setupd/50-accent-plugin-nestbox.yml /etc/accent-webhookd/conf.d/50-accent-plugin-nestbox.yml \
    && install -o accent-setupd -g accent-setupd /dev/null /var/log/accent-setupd.log

EXPOSE 9302

WORKDIR $PYSETUP_PATH

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["accent-setupd"]
