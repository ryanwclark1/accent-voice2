FROM accentcommunications/accent-confd

ENV PYTHONDONTWRITEBYTECODE='true'

COPY . /usr/src/accent-confd
WORKDIR /usr/src/accent-confd
RUN python3 -m pip install -e .
