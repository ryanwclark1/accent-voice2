# Copyright 2023 Accent Communications

import pycountry
from accent.mallow import fields
from marshmallow import validates
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema


class LocalizationSchema(BaseSchema):
    country = fields.String(allow_none=True, default=None, validate=Length(equal=2))

    @validates('country')
    def _validate_country(self, country, **kwargs):
        if not country:
            return

        try:
            country_iso = pycountry.countries.get(alpha_2=country)
        except LookupError:  # invalid country format raises this error
            country_iso = None

        if not country_iso:
            raise ValidationError(f'Invalid country code: {country}')
