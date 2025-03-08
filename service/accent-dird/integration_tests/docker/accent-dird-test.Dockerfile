FROM accentcommunications/accent-dird

ENV PYTHONDONTWRITEBYTECODE='true'

COPY . /usr/src/accent-dird

WORKDIR /usr/src/accent-dird
RUN python3 -m pip install -e . \
    && rm -f /etc/accent-dird/conf.d/050-accent-*.yml

WORKDIR /usr/src/accent-dird/integration_tests/docker/broken-plugins
RUN python3 -m pip install -e .
