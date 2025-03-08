# integration tests
tooling for integration testing workflows

## shell.sh
Wraps common tasks to work with integration tests by providing a prepared subshell
* activates a virtual environment and ensure the test python dependencies are installed
* source `denv` into the shell, and runs `denv enter $asset` to deploy the integration tests setup using docker compose
* automatically cleanup before exit by running `denv exit $asset`

Example usage:
```shell
cd $project/integration_tests
bash -x /path/to/shell.sh
$ docker ps # see that test containers are up and available
$ denv logs $container # denv is available
$ pytest suites/ # pytest and other python test dependencies are available
$ ... # work
$ exit # exit shell when done
$ docker ps # see that containers are no longer up
```

