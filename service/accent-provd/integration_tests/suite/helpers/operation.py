# Copyright 2023 Accent Communications

from accent_provd_client import operation
from hamcrest import assert_that, is_


def operation_successful(operation_resource: operation.OperationInProgress) -> None:
    operation_resource.update()
    assert_that(operation_resource.state, is_(operation.OIP_SUCCESS))


def operation_fail(operation_resource: operation.OperationInProgress) -> None:
    operation_resource.update()
    assert_that(operation_resource.state, is_(operation.OIP_FAIL))
