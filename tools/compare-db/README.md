# Setup

## Prerequisites

```sh
apt-get install docker-ce
curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
pip install -r requirements.txt
```

## Usage

1. Start 2 PostgreSQL instances, e.g. with Docker

    ```sh
    docker compose up -d
    ```

2. Get PostgreSQL ports from Docker

    ```sh
    docker compose port postgresql-migrated 5432
    docker compose port postgresql-installed 5432
    ```

3. Copy `defaults.ini` to `local.ini` and edit it to set the correct values. If you
   used the provided `docker-compose.yml`, you only need to change the port numbers.

4. Run the diff tool

    ```sh
    python compare-db-migrations.py --config local.ini
    ```
