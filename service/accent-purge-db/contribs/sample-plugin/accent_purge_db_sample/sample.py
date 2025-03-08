# Copyright 2023 Accent Communications

archive_file = '/tmp/accent_purge_db.archive'
purger_file = '/tmp/accent_purge_db.purge'


def archive_plugin(config):
    with open(archive_file, 'w') as output:
        output.write(f'Save tables before purge. {config["days_to_keep"]} days to keep!')


class PurgePlugin:
    @staticmethod
    def purge(days_to_keep, session):
        with open(purger_file, 'w') as output:
            output.write(f'Purged, {days_to_keep} days keeped!')
