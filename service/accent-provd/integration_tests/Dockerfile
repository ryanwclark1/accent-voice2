FROM accentcommunications/accent-provd

ENV PYTHONDONTWRITEBYTECODE='true'

COPY . /usr/src/accent-provd
WORKDIR /usr/src/accent-provd

RUN pip install -e . --config-settings editable_mode=compat
