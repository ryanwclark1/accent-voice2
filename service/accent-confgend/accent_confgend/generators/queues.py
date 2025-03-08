# Copyright 2023 Accent Communications

from accent_dao import asterisk_conf_dao

from accent_confgend.generators.util import AsteriskFileWriter


class QueuesConf:
    _ignored_keys = [
        'name',
        'label',
        'category',
        'commented',
    ]

    def generate(self, output):
        writer = AsteriskFileWriter(output)

        writer.write_section('general')
        for item in asterisk_conf_dao.find_queue_general_settings():
            writer.write_option(item['var_name'], item['var_val'])

        for q in asterisk_conf_dao.find_queue_settings():
            writer.write_section(q['name'], comment=q['label'])

            for k, v in q.items():
                if k in self._ignored_keys:
                    continue
                if v is None or (isinstance(v, str) and not v):
                    continue

                writer.write_option(k, v)

            queuemember_settings = asterisk_conf_dao.find_queue_members_settings(
                q['name']
            )
            for values in queuemember_settings:
                writer.write_option('member', ','.join(values))
