# Copyright 2023 Accent Communications

import json
import os
import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase

from accent_test_helpers.asset_launching_test_case import (
    AbstractAssetLaunchingHelper,
    _run_cmd,
)

_DOCKER_RUN_COMMAND = ["run", "--rm"]


class DockerError(Exception):
    pass


class ValidationError(Exception):
    pass


class TestDocumentation(AbstractAssetLaunchingHelper, TestCase):
    asset = "documentation"
    assets_root = os.path.join(os.path.dirname(__file__), "..", "assets")
    service = "spec-generator"
    validator = "spec-validator"

    @classmethod
    def setUpClass(cls) -> None:
        cls.pull_containers()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._maybe_dump_docker_logs()

    @classmethod
    def _generate_specfiles(
        cls, output_directory: os.PathLike
    ) -> subprocess.CompletedProcess:
        program = ["docker", "compose"]
        options = cls._docker_compose_options()
        volumes = ["-v", f"{output_directory}:/app/output"]
        service = [cls.service]
        service_args = ["-p", "test-version"]

        args = _DOCKER_RUN_COMMAND + volumes + service + service_args
        return _run_cmd(program + options + args)

    @classmethod
    def _validate_specfile(
        cls, name: str, path: os.PathLike
    ) -> subprocess.CompletedProcess:
        program = ["docker", "compose"]
        options = cls._docker_compose_options()
        volumes = ["-v", f"{path}:/{name}.yml"]
        service = [cls.validator]
        service_args = [
            "validate",
            "--fail-severity",
            "error",
            "--diagnostics-format",
            "json",
            f"/{name}.yml",
        ]

        args = _DOCKER_RUN_COMMAND + volumes + service + service_args
        return _run_cmd(program + options + args)

    @classmethod
    def _parse_errors(cls, process: subprocess.CompletedProcess) -> list[str]:
        output = process.stdout.decode().split("\n")
        starting_json = output.index("[")
        issues = json.loads("".join(output[starting_json:]))
        return [issue["message"] for issue in issues if issue["severity"] == 0]

    def test_documentation_is_valid(self) -> None:
        with TemporaryDirectory() as basepath:
            result = self._generate_specfiles(basepath)
            if result.returncode != 0:
                msg = "An error occured while generating specification files"
                raise DockerError(
                    msg
                )

            for filename in os.listdir(basepath):
                path = os.path.join(basepath, filename)
                name, extension = os.path.splitext(filename)
                if extension.endswith("yml"):
                    result = self._validate_specfile(name, path)

                    if result.returncode != 0:
                        for _error in self._parse_errors(result):
                            pass
                        msg = f"Validation failed for {name} specification file"
                        raise ValidationError(
                            msg
                        )
