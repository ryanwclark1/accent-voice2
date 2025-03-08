## Launching

```shell
accent_auth [-d] [--user <user>] --config <path/to/config/file>
```

* `-d`: Starts accent-auth in debug mode
* `--user`: Specify the OS user to use
* `--config`: Path to the configuration file

## Docker

The accentcommunications/accent-auth image can be built using the following command:

    % docker build -t accentcommunications/accent-auth .

To run accent-auth in docker, use the following commands:

    % docker run -p 9497:9497 -v /conf/accent-auth:/etc/accent-auth/conf.d/ -it accentcommunications/accent-auth bash
    % accent-auth [-df] [-u <user>] [-c <path/to/config/file>]

The accentcommunications/accent-auth-db image can be built using the following command:

    % docker build -f contribs/docker/Dockerfile-db -t accentcommunications/accent-auth-db .

## Bootstrapping

In order to be able to create users, groups and policies you have to be authenticated. The bootstrap
process allows the administrator to create a first user with the necessary rights to be able to add
other users.

### Preparing accent-auth to be bootstrapped

To be able to bootstrap accent-auth, you will have to enable the init plugin and create a key file in
accent-auth's HOME directory. This can be done using the `accent-auth-bootstrap` command.

```shell
accent-auth-bootstrap setup && systemctl restart accent-auth
```

### Bootstrapping accent-auth

Once accent-auth is ready to be bootstrapped, calling the init resource with a username, password and
the content of the key file will create a new user. The username and password can then be used to create
a token with the `auth.#` acl. This can be done using the `accent-auth-bootstrap` command.

```shell
accent-auth-bootstrap complete
```

This script will create a configuration file named `/root/.config/accent-auth-cli/050-credentials.yml`
containing all necessary information to be used from the `accent-auth-cli`.

## Load testing

To test accent-auth with ab

Dependencies

* ab

```shell
apt update && apt install apache2-utils
```

Running the tests

```shell
ab -n1000 -c25 -A 'alice:alice' -T 'application/json' "https://localhost:9497/0.1/token"
```

This line will start 25 process creating 1000 tokens with the username and password alice alice

## Configuration

The default config is /etc/accent-auth/config.yml, you could override in /etc/accent-auth/conf.d/

### Enabling the users registration API

To enable the users registration (/users/register) API endpoint, add a file containing the following lines to the /etc/accent-auth/conf.d directory and restart accent-auth

```yaml
enabled_http_plugins:
  user_registration: true
```
