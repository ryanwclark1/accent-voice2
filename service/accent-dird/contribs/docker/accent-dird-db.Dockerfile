FROM accentcommunications/accent-base-db
LABEL maintainer="Accent Maintainers <help@accentservices.com>"

COPY . /usr/src/accent-dird
WORKDIR /usr/src/accent-dird
ENV ALEMBIC_DB_URI=postgresql://accent-dird:password123@localhost/accent-dird

RUN true \
    && python3 setup.py install \
    && pg_start \
    && su postgres -c "psql -c \"CREATE ROLE \\"'"'"accent-dird\\"'"'" LOGIN PASSWORD 'password123';\"" \
    && su postgres -c "psql -c 'CREATE DATABASE \"accent-dird\" WITH OWNER \"accent-dird\";'" \
    && su postgres -c "psql \"accent-dird\" -c 'CREATE EXTENSION \"uuid-ossp\";'" \
    && su postgres -c "psql \"accent-dird\" -c 'CREATE EXTENSION \"unaccent\";'" \
    && su postgres -c "psql \"accent-dird\" -c 'CREATE EXTENSION \"hstore\";'" \
    && (cd /usr/src/accent-dird && python3 -m alembic.config -c alembic.ini upgrade head) \
    && pg_stop \
    && true
USER postgres
