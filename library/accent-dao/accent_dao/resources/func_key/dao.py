# Copyright 2023 Accent Communications

from sqlalchemy import or_

from accent_dao.alchemy.feature_extension import FeatureExtension
from accent_dao.alchemy.func_key_dest_forward import FuncKeyDestForward
from accent_dao.alchemy.func_key_dest_user import FuncKeyDestUser
from accent_dao.alchemy.func_key_mapping import FuncKeyMapping
from accent_dao.alchemy.userfeatures import UserFeatures
from accent_dao.helpers.db_manager import daosession


@daosession
def find_all_forwards(session, user_id, fwd_type):
    type_converter = _ForwardTypeConverter()

    query = (
        session.query(FuncKeyDestForward.number.label('number'))
        .join(
            FeatureExtension,
            FuncKeyDestForward.feature_extension_uuid == FeatureExtension.uuid,
        )
        .join(
            FuncKeyMapping, FuncKeyMapping.func_key_id == FuncKeyDestForward.func_key_id
        )
        .join(
            UserFeatures,
            UserFeatures.func_key_private_template_id == FuncKeyMapping.template_id,
        )
        .filter(UserFeatures.id == user_id)
        .filter(FeatureExtension.feature == type_converter.model_to_db(fwd_type))
    )
    return query.all()


@daosession
def find_users_having_user_destination(session, destination_user):
    query = (
        session.query(UserFeatures)
        .join(
            FuncKeyMapping,
            or_(
                FuncKeyMapping.template_id == UserFeatures.func_key_private_template_id,
                FuncKeyMapping.template_id == UserFeatures.func_key_template_id,
            ),
        )
        .join(
            FuncKeyDestUser, FuncKeyMapping.func_key_id == FuncKeyDestUser.func_key_id
        )
        .filter(FuncKeyDestUser.user_id == str(destination_user.id))
    )
    return query.all()


class _ForwardTypeConverter:
    fwd_types = {
        'unconditional': 'fwdunc',
        'noanswer': 'fwdrna',
        'busy': 'fwdbusy',
    }

    reversed_types = {value: key for key, value in fwd_types.items()}

    def db_to_model(self, db_type):
        return self.reversed_types[db_type]

    def model_to_db(self, model_type):
        return self.fwd_types[model_type]