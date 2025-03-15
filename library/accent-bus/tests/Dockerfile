# Dockerfile
FROM python:3.12-slim-buster

WORKDIR /app

# Install uv
RUN pip install uv

COPY pyproject.toml ./
COPY ../accent_bus ./accent_bus/
#Copy all folders, and files in tests to tests directory
COPY ../tests ./tests/

# Install dependencies using uv.  This correctly handles dependencies
# specified in pyproject.toml.  The "--no-cache-dir" is good practice
# in Docker builds to keep image size down.
RUN uv pip install . --no-cache-dir

# No CMD needed for a library.
