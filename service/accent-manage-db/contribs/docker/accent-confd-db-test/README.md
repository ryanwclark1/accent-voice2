# accent-confd-db-test

accentcommunications/accent-confd-db-test is a [Postgres](http://postgresql.org) image with a minimal database
already configured. It is mainly used for running automated tests. Please note that the database is
preconfigured as if the Accent wizard has already been run, with default values already set.

## Building the image

This image depends on accentcommunications/accent-confd-db. Build this image first from the root directory of
accent-manage-db:

    docker build -t accentcommunications/accent-confd-db .

Then you can build accent-confd-db-test:

    docker build -t accentcommunications/accent-confd-db-test -f contribs/docker/accent-confd-db-test/Dockerfile .

## Using the image

### Initializing the database

If you would like to execute SQL scripts before postgres starts, place them in ```/pg-init-db```.
For example:

    docker run -v /path/to/sql/scripts:/pg-init-db accentcommunications/accent-confd-db-test
