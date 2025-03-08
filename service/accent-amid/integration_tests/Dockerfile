FROM accentcommunications/accent-amid

ENV PYTHONDONTWRITEBYTECODE='true'

ADD . /usr/src/accent-amid
WORKDIR /usr/src/accent-amid
RUN python3 -m pip install -e .
