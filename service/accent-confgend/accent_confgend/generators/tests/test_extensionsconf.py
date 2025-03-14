# Copyright 2023 Accent Communications


import os
import textwrap
import unittest
from io import StringIO
from unittest.mock import Mock, patch

from accent_dao.alchemy.ivr import IVR
from hamcrest import assert_that, contains_string
from jinja2.loaders import DictLoader

from accent_confgend.generators.extensionsconf import ExtensionsConf
from accent_confgend.generators.util import AsteriskFileWriter
from accent_confgend.hints.generator import HintGenerator
from accent_confgend.template import TemplateHelper


class TestExtensionsConf(unittest.TestCase):
    maxDiff = 10000

    def setUp(self):
        self.hint_generator = Mock(HintGenerator)
        self.tpl_mapping = {}
        self.tpl_helper = TemplateHelper(DictLoader(self.tpl_mapping))
        self.extensionsconf = ExtensionsConf(
            'etc/accent-confgend/templates/contexts.conf',
            self.hint_generator,
            self.tpl_helper,
        )
        self.output = StringIO()

    @patch('accent_dao.asterisk_conf_dao.find_exten_accentfeatures_setting')
    def test_extensions_features(self, mock_find_exten_accentfeatures_setting):
        mock_conf = Mock()
        mock_conf.items.return_value = [
            ('objtpl', '%%EXTEN%%,%%PRIORITY%%,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})'),
            ('objtpl', 'n,Set(__ACCENT_BASE_EXTEN=${EXTEN})'),
            ('objtpl', 'n,GoSub(contextlib,entry-exten-context,1)'),
            ('objtpl', 'n,%%ACTION%%'),
        ]
        xfeatures = {
            'fwdrna': {'exten': '_*22.', 'enabled': True},
            'fwdbusy': {'exten': '_*23.', 'enabled': True},
            'bsfilter': {'exten': '_*37.', 'enabled': True},
            'fwdunc': {'exten': '_*21.', 'enabled': True},
            'vmusermsg': {'exten': '*98', 'enabled': True},
            'phoneprogfunckey': {'exten': '_*735.', 'enabled': True},
        }
        mock_find_exten_accentfeatures_setting.return_value = [
            {
                'exten': '*10',
                'enabled': True,
                'feature': 'phonestatus',
                'uuid': '7a51dda0-34e9-482e-b3c1-301f615d99cf',
            },
            {
                'exten': '_*11.',
                'enabled': True,
                'feature': 'paging',
                'uuid': '1775aa6e-c9fb-4cbf-88bd-5c266834df79',
            },
            {
                'exten': '*20',
                'enabled': True,
                'feature': 'fwdundoall',
                'uuid': '9a742f20-d5ce-440e-a08c-840fa3f1e22d',
            },
        ]

        ast_writer = AsteriskFileWriter(self.output)
        self.extensionsconf._generate_extension_features(
            mock_conf, xfeatures, ast_writer
        )
        mock_conf.items.assert_called_once_with('accent-features')
        mock_find_exten_accentfeatures_setting.assert_called_once()
        self.assertEqual(
            self.output.getvalue(),
            textwrap.dedent(
                """\
            [accent-features]
            exten = *10,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            same  =     n,GoSub(contextlib,entry-exten-context,1)
            same  =     n,GoSub(phonestatus,s,1())

            exten = _*11.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            same  =     n,GoSub(contextlib,entry-exten-context,1)
            same  =     n,GoSub(paging,s,1(${EXTEN:3}))

            exten = *20,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            same  =     n,GoSub(contextlib,entry-exten-context,1)
            same  =     n,GoSub(fwdundoall,s,1())

            exten = *23,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            exten = *23,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            exten = *23,n,Gosub(feature_forward,s,1(busy))
            exten = *22,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            exten = *22,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            exten = *22,n,Gosub(feature_forward,s,1(rna))
            exten = *21,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
            exten = *21,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
            exten = *21,n,Gosub(feature_forward,s,1(unc))
        """
            ),
        )

    def test_generate_dialplan_from_template(self):
        template = ["%%EXTEN%%,%%PRIORITY%%,Set('__ACCENT_BASE_CONTEXT': ${CONTEXT})"]
        exten = {'exten': '*98', 'priority': 1}

        ast_writer = AsteriskFileWriter(self.output)
        self.extensionsconf.gen_dialplan_from_template(template, exten, ast_writer)

        self.assertEqual(
            self.output.getvalue(),
            "exten = *98,1,Set('__ACCENT_BASE_CONTEXT': ${CONTEXT})\n\n",
        )

    def test_generate_hints(self):
        hints = [
            'exten = 1000,hint,SIP/abcdef',
            'exten = 4000,hint,confbridge:1',
            'exten = *7351***223*1234,hint,Custom:*7351***223*1234',
        ]

        self.hint_generator.generate.return_value = hints

        self.extensionsconf._generate_hints('context', self.output)

        self.hint_generator.generate.assert_called_once_with('context')
        for hint in hints:
            self.assertTrue(hint in self.output.getvalue())

    @patch('accent_confgend.generators.extensionsconf.ivr_dao')
    def test_generate_ivrs(self, mock_ivr_dao):
        ivr = IVR(id=42, name='foo', menu_sound='héllo-world')
        mock_ivr_dao.find_all_by.return_value = [ivr]
        self.tpl_mapping['asterisk/extensions/ivr.jinja'] = textwrap.dedent(
            '''
            [accent-ivr-{{ ivr.id }}]
            same  =   n,Background({{ ivr.menu_sound }})
        '''
        )

        self.extensionsconf._generate_ivr(self.output)

        assert_that(self.output.getvalue(), contains_string('[accent-ivr-42]'))
        assert_that(
            self.output.getvalue(),
            contains_string('same  =   n,Background(héllo-world)'),
        )

    @patch('accent_confgend.generators.extensionsconf.ivr_dao')
    @patch('accent_confgend.generators.extensionsconf.asterisk_conf_dao')
    def test_generate(self, mock_asterisk_conf_dao, mock_ivr_dao):
        hints = [
            'exten = 1000,hint,SIP/abcdef',
            'exten = 4000,hint,confbridge:1',
            'exten = *7351***223*1234,hint,Custom:*7351***223*1234',
        ]
        self.hint_generator.generate_global_hints.side_effect = [hints, []]
        self.hint_generator.generate.return_value = hints

        mock_asterisk_conf_dao.find_extenfeatures_settings.return_value = [
            Mock(feature="fwdbusy", exten="foo", enabled=True),
            Mock(feature="fwdrna", exten="bar", enabled=False),
            Mock(feature="fwdunc", exten="bar", enabled=False),
        ]
        self.tpl_mapping['asterisk/extensions/ivr.jinja'] = "[accent-ivr-{{ ivr.id }}]"

        mock_ivr_dao.find_all_by.return_value = [
            IVR(id=42, name='foo', menu_sound='hello-world'),
            IVR(id=43, name='bar', menu_sound='youhou'),
        ]

        mock_asterisk_conf_dao.find_context_settings.return_value = [
            {"name": "ctx_name", "contexttype": "incall", "tenant_uuid": "tenant-uuid"},
            {
                "name": "ctx_internal",
                "contexttype": "internal",
                "tenant_uuid": "tenant-uuid",
            },
        ]
        mock_asterisk_conf_dao.find_contextincludes_settings.return_value = [
            {"include": "include-me.conf"}
        ]
        mock_asterisk_conf_dao.find_exten_settings.side_effect = [
            [
                {
                    "type": "incall",
                    "context": "default",
                    "exten": "foo@bar",
                    "typeval": "incallfilter",
                    "id": 1234,
                    "tenant_uuid": "2b853b5b-6c19-4123-90da-3ce05fe9aa74",
                }
            ],
            [
                {
                    "type": "user",
                    "context": "ctx_internal",
                    "exten": "user@ctx_internal",
                    "typeval": "user",
                    "id": 56,
                    "tenant_uuid": "5adadf7b-5a4c-4701-9486-a4e8f9d21db0",
                }
            ],
        ]

        self.extensionsconf.generate(self.output)

        lines = [line for line in self.output.getvalue().split("\n") if line]
        path = os.path.dirname(__file__)
        with open(os.path.join(path, "expected_generated_extension.conf")) as f:
            expected_lines = [line for line in f.read().split("\n") if line]
        self.assertEqual(expected_lines, lines)
