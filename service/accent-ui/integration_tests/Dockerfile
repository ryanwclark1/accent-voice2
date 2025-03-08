FROM accentcommunications/accent-ui

COPY . /usr/src/accent-ui
WORKDIR /usr/src/accent-ui

ENV PYTHONDONTWRITEBYTECODE='true'

RUN pybabel compile --directory=accent_ui/translations
RUN python3 -m pip install -e .
