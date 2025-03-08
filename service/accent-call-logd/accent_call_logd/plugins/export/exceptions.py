# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class ExportFSNotFoundException(APIException):
    def __init__(self, export_uuid, export_path):
        super().__init__(
            status_code=500,
            message='Export: not found on filesystem',
            error_id='export-filesystem-not-found',
            details={
                'export_uuid': str(export_uuid),
                'export_path': export_path,
            },
        )


class ExportFSPermissionException(APIException):
    def __init__(self, export_uuid, export_path):
        super().__init__(
            status_code=500,
            message='Export: permission denied',
            error_id='export-permission-denied',
            details={
                'export_uuid': str(export_uuid),
                'export_path': export_path,
            },
        )


class ExportNotDoneYetException(APIException):
    def __init__(self, export_uuid):
        super().__init__(
            status_code=202,
            message='Export: not done yet',
            error_id='export-not-done-yet',
            details={
                'export_uuid': str(export_uuid),
            },
        )


class ExportErrorException(APIException):
    def __init__(self, export_uuid):
        super().__init__(
            status_code=500,
            message='Error while creating the export',
            error_id='export-error',
            details={
                'export_uuid': str(export_uuid),
            },
        )
