FROM accentcommunications/accent-purge-db

ENV PYTHONDONTWRITEBYTECODE='true'

COPY . /usr/src/accent-purge-db
WORKDIR /usr/src/accent-purge-db

RUN pip install -Ur requirements.txt
RUN pip install -Ur integration_tests/requirements.txt
RUN python3 -m pip install -e .

WORKDIR contribs/sample-plugin
RUN python3 -m pip install .

WORKDIR /usr/src/accent-purge-db
RUN cp -r etc/accent-purge-db /etc

CMD ["pytest", "-v", "-s", "-p", "no:cacheprovider", "integration_tests/suite"]
