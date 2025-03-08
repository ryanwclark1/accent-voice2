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
    PYSETUP_PATH="/usr/src/accent-provd" \
    VENV_PATH="/usr/src/accent-provd/.venv"

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
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY ./library ../../library

COPY ./service/accent-provd/pyproject.toml ./service/accent-provd/poetry.lock ./
COPY ./service/accent-provd/accent_provd ./accent_provd
COPY ./service/accent-provd/provd ./provd
COPY ./service/accent-provd/tftp-bench ./tftp-bench
COPY ./service/accent-provd/twisted ./twisted
COPY ./service/accent-provd/usr ./usr

RUN true \
    && poetry install --only main \
    && rm -rf ../../library

###############################################
# Production Image
###############################################
FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./service/accent-provd/etc /etc

RUN true \
    && mkdir -p /var/cache/accent-provd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

EXPOSE 8667 8666 69/udp

ENV PATH="$VENV_PATH/bin:$PATH"
CMD ["twistd", "--nodaemon", "--no_save", "--pidfile=", "accent-provd", "--stderr", "--verbose"]
