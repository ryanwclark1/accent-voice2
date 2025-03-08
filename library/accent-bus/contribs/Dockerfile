FROM python:3.10-slim-bullseye

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/accent-bus
COPY contribs/asyncapi-template.yml /app
COPY contribs/documentation.py /app

WORKDIR /app

RUN true \
    && pip install pyyaml \
    && pip install -r accent-bus/requirements.txt \
    && pip install -e accent-bus \
    && mkdir -p -m777 /app/output

ENTRYPOINT ["python", "documentation.py", "-o", "/app/output"]
