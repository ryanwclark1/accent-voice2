# Copyright 2023 Accent Communications


from io import StringIO

from accent_dao import asterisk_conf_dao
from accent_dao.resources.asterisk_file import dao as asterisk_file_dao
from accent_dao.resources.pjsip_transport import dao as transport_dao

from accent_confgend.generators.util import AsteriskFileWriter

from ..helpers.asterisk import AsteriskFileGenerator


class PJSIPConfGenerator:
    def __init__(self, dependencies):
        pass

    def generate(self):
        asterisk_file_generator = AsteriskFileGenerator(asterisk_file_dao)
        output = StringIO()
        asterisk_file_generator.generate(
            'pjsip.conf', output, required_sections=['global', 'system']
        )
        self.generate_transports(output)
        output.write('\n')
        self.generate_lines(output)
        output.write('\n')
        self.generate_trunks(output)
        output.write('\n')
        self.generate_meeting_guests(output)
        return output.getvalue()

    def generate_transports(self, output):
        writer = AsteriskFileWriter(output)
        transports = transport_dao.search()
        for transport in transports.items:
            writer.write_section(transport.name)
            writer.write_option('type', 'transport')
            writer.write_options(transport.options)

    def generate_lines(self, output):
        writer = AsteriskFileWriter(output)
        endpoints = asterisk_conf_dao.find_sip_user_settings()
        for endpoint in endpoints:
            self._write_simple_endpoint(writer, endpoint)

    def generate_meeting_guests(self, output):
        writer = AsteriskFileWriter(output)
        endpoints = asterisk_conf_dao.find_sip_meeting_guests_settings()
        for endpoint in endpoints:
            self._write_simple_endpoint(writer, endpoint)

    def _write_simple_endpoint(self, writer, endpoint):
        name = endpoint['name']
        label = endpoint.get('label')
        endpoint_section_options = endpoint.get('endpoint_section_options', [])
        writer.write_section(name, comment=label)
        writer.write_options(endpoint_section_options)
        sections = {}
        for key, value in endpoint_section_options:
            if key == 'auth':
                sections['auth_section_options'] = value
            elif key == 'aors':
                sections['aor_section_options'] = value

        for key in sorted(sections):
            writer.write_section(sections[key])
            writer.write_options(endpoint.get(key, []))

    def generate_trunks(self, output):
        writer = AsteriskFileWriter(output)
        endpoints = asterisk_conf_dao.find_sip_trunk_settings()
        for endpoint in endpoints:
            name = endpoint['name']
            label = endpoint.get('label')
            endpoint_section_options = endpoint.get('endpoint_section_options', [])
            registration_section_options = endpoint.get(
                'registration_section_options', []
            )
            writer.write_section(name, comment=label)
            writer.write_options(endpoint_section_options)
            sections = {
                'identify_section_options': name,
                'registration_section_options': name,
            }
            for key, value in endpoint_section_options:
                if key == 'auth':
                    sections['auth_section_options'] = value
                elif key == 'aors':
                    sections['aor_section_options'] = value
                elif key == 'outbound_auth':
                    sections['outbound_auth_section_options'] = value
            for key, value in registration_section_options:
                if key == 'outbound_auth':
                    sections['registration_outbound_auth_section_options'] = value

            for key in sorted(sections):
                options = endpoint.get(key)
                if not options:
                    continue

                writer.write_section(sections[key])
                writer.write_options(options)
