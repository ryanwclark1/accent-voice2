# Copyright 2023 Accent Communications

from accent_dao.alchemy.dialaction import Dialaction
from marshmallow import post_load

from accent_confd.helpers.destination import DestinationField
from accent_confd.helpers.mallow import BaseSchema


class UserFallbackSchema(BaseSchema):
    noanswer_destination = DestinationField(
        attribute='noanswer', default=None, allow_none=True
    )
    busy_destination = DestinationField(attribute='busy', default=None, allow_none=True)
    congestion_destination = DestinationField(
        attribute='congestion', default=None, allow_none=True
    )
    fail_destination = DestinationField(
        attribute='chanunavail', default=None, allow_none=True
    )

    @post_load
    def create_objects(self, data, **kwargs):
        for key, form in data.items():
            if form:
                data[key] = Dialaction(**form)
        return data
