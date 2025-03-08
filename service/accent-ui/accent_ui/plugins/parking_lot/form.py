# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_
from wtforms.fields import FieldList, FormField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp

from accent_ui.helpers.destination import DestinationHiddenField
from accent_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = StringField(l_('Extension'), validators=[InputRequired()])
    context = SelectField(l_('Context'), validators=[InputRequired()])


class ParkingLotForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    slots_start = StringField(
        l_('Slots Start'), [InputRequired(), Regexp(r'^[0-9]+$'), Length(max=40)]
    )
    slots_end = StringField(
        l_('Slots End'), [InputRequired(), Regexp(r'^[0-9]+$'), Length(max=40)]
    )
    music_on_hold = SelectField(l_('Music On Hold'), [Length(max=128)], choices=[])
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])
    submit = SubmitField(l_('Submit'))


class ParkingFuncKeyDestinationForm(BaseForm):
    set_value_template = '{parking_lot_name}'

    parking_lot_id = SelectField(l_('Parking Lot'), [InputRequired()], choices=[])
    parking_lot_name = DestinationHiddenField()


class ParkPositionFuncKeyDestinationForm(BaseForm):
    set_value_template = '{parking_lot_name}'

    parking_lot_id = SelectField(l_('Parking Lot'), [InputRequired()], choices=[])
    position = IntegerField(l_('Position'), [InputRequired()])
    parking_lot_name = DestinationHiddenField()
