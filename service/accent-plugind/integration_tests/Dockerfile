FROM accentcommunications/accent-plugind

COPY . /usr/src/accent-plugind
WORKDIR /usr/src/accent-plugind

ENV PYTHONDONTWRITEBYTECODE='true'

RUN python3 -m pip install -e .
