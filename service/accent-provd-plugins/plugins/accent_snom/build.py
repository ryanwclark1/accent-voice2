"""
Copyright 2023 Accent Communications
SPDX-License-Identifier: GPL-3.0-or-later

Depends on the following external programs:
 - rsync
 - sed
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from subprocess import check_call
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    def target(
        target_id: str, plugin_id: str, std_dirs: bool = True
    ) -> Callable[[Callable[[str], None]], None]:
        """The `target` method is injected in `exec` call by the build script."""

        def wrapper(func: Callable[[str], None]) -> None:
            pass

        return wrapper


@target('8.7.5.35', 'accent-snom-8.7.5.35')
def build_8_7_5_35(path: str) -> None:
    MODELS = [
        ('300', 'f'),
        ('320', 'f'),
        ('370', 'f'),
        ('710', 'r'),
        ('715', 'r'),
        ('720', 'r'),
        ('725', 'r'),
        ('760', 'r'),
        ('D765', 'r'),
        ('820', 'r'),
        ('821', 'r'),
        ('870', 'r'),
        ('MP', 'r'),
        ('PA1', 'f'),
    ]
    check_call(
        ['rsync', '-rlp', '--exclude', '.*', '--exclude', '*.btpl', 'common/', path]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'

        sed_script = f's/#FW_FILENAME#/snom{model}-8.7.5.35-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )
    check_call(['rsync', '-rlp', '--exclude', '.*', 'v8_7_5_35/', path])


@target('8.9.3.40', 'accent-snom-8.9.3.40')
def build_8_9_3_40(path: str) -> None:
    MODELS = [('D745', 'r')]

    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D745.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-8.9.3.40-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v8_9_3_40/', path])


@target('8.9.3.60', 'accent-snom-8.9.3.60')
def build_8_9_3_60(path: str) -> None:
    MODELS = [
        ('D305', 'r'),
        ('D315', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
    ]

    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-8.9.3.60-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v8_9_3_60/', path])


@target('8.9.3.80', 'accent-snom-8.9.3.80')
def build_8_9_3_80(path):
    MODELS = [
        ('D305', 'r'),
        ('D315', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('710', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('720', 'r'),
        ('725', 'r'),
        ('D745', 'r'),
        ('760', 'r'),
        ('D765', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-8.9.3.80-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v8_9_3_80/', path])


@target('10.1.20.0', 'accent-snom-10.1.20.0')
def build_10_1_20_0(path):
    MODELS = [
        ('D785', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D785.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.20.0-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_20_0/', path])


@target('10.1.26.1', 'accent-snom-10.1.26.1')
def build_10_1_26_1(path):
    MODELS = [
        ('D735', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D735.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.26.1-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_26_1/', path])


@target('10.1.39.11', 'accent-snom-10.1.39.11')
def build_10_1_39_11(path):
    MODELS = [
        ('D375', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D375.tpl',
            '--include',
            '/templates/D717.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.39.11-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_39_11/', path])


@target('10.1.46.16', 'accent-snom-10.1.46.16')
def build_10_1_46_16(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]

    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D717.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = (
            Path(path) / 'templates' / 'common' / f'snom{model}-firmware.xml.tpl'
        )
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.46.16-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_46_16/', path])


@target('10.1.49.11', 'accent-snom-10.1.49.11')
def build_10_1_49_11(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]

    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D717.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.46.16-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_49_11/', path])


@target('10.1.51.12', 'accent-snom-10.1.51.12')
def build_10_1_51_12(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D717.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.51.12-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_51_12/', path])


@target('10.1.54.13', 'accent-snom-10.1.54.13')
def build_10_1_54_13(path):
    MODELS = [
        ('D120', 'r'),
        ('D305', 'r'),
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D375', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D745', 'r'),
        ('D765', 'r'),
        ('D785', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D717.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.54.13-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_54_13/', path])


@target('05.20.0001', 'accent-snom-dect-05.20.0001')
def build_05_20_0001(path):
    MODELS = [
        'M300',
        'M700',
        'M900',
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/M300.tpl',
            '--include',
            '/templates/M700.tpl',
            '--include',
            '/templates/M900.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common_dect/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/{model}_v0520_b0001.fwu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common_dect/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common_dect/templates/common/snom-model.htm.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common_dect/templates/common/snom-model.xml.tpl.btpl',
                ],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v05_20_0001/', path])


@target('10.1.101.11', 'accent-snom-10.1.101.11')
def build_10_1_101_11(path):
    MODELS = [
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D785', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D712.tpl',
            '--include',
            '/templates/D717.tpl',
            '--include',
            '/templates/7*5.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.101.11-SIP-{fw_suffix}.bin/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_101_11/', path])


@target('10.1.141.13', 'accent-snom-10.1.141.13')
def build_10_1_141_13(path):
    MODELS = [
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('D713', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D785', 'r'),
        ('D862', 'r'),
        ('D865', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D71*.tpl',
            '--include',
            '/templates/7*5.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D86*.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.141.13-SIP-{fw_suffix}.bin/'
        if model.startswith("D8"):
            sed_script = f's/#FW_FILENAME#/snom{model}-10.1.141.13-SIP-{fw_suffix}.swu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_141_13/', path])


@target('10.1.152.12', 'accent-snom-10.1.152.12')
def build_10_1_152_12(path):
    MODELS = [
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('D713', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D785', 'r'),
        ('D862', 'r'),
        ('D865', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D71*.tpl',
            '--include',
            '/templates/7*5.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D86*.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.152.12-SIP-{fw_suffix}.bin/'
        if model.startswith("D8"):
            sed_script = f's/#FW_FILENAME#/snom{model}-10.1.152.12-SIP-{fw_suffix}.swu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_152_12/', path])


@target('10.1.159.12', 'accent-snom-10.1.159.12')
def build_10_1_159_12(path):
    MODELS = [
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('D713', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D785', 'r'),
        ('D862', 'r'),
        ('D865', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D71*.tpl',
            '--include',
            '/templates/7*5.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D86*.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.159.12-SIP-{fw_suffix}.bin/'
        if model.startswith("D8"):
            sed_script = f's/#FW_FILENAME#/snom{model}-10.1.159.12-SIP-{fw_suffix}.swu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_159_12/', path])


@target('10.1.175.16', 'accent-snom-10.1.175.16')
def build_10_1_175_16(path):
    MODELS = [
        ('D315', 'r'),
        ('D335', 'r'),
        ('D345', 'r'),
        ('D385', 'r'),
        ('D712', 'r'),
        ('D713', 'r'),
        ('715', 'r'),
        ('D717', 'r'),
        ('725', 'r'),
        ('D735', 'r'),
        ('D785', 'r'),
        ('D862', 'r'),
        ('D865', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D3*5.tpl',
            '--include',
            '/templates/D71*.tpl',
            '--include',
            '/templates/7*5.tpl',
            '--include',
            '/templates/D7*5.tpl',
            '--include',
            '/templates/D86*.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.175.16-SIP-{fw_suffix}.bin/'
        if model.startswith("D8"):
            sed_script = f's/#FW_FILENAME#/snom{model}-10.1.175.16-SIP-{fw_suffix}.swu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_175_16/', path])


@target('10.1.184.15', 'accent-snom-10.1.184.15')
def build_10_1_184_15(path):
    MODELS = [
        ('D812', 'r'),
        ('D815', 'r'),
    ]
    check_call(
        [
            'rsync',
            '-rlp',
            '--exclude',
            '.*',
            '--include',
            '/templates/base.tpl',
            '--include',
            '/templates/D81*.tpl',
            '--exclude',
            '/templates/*.tpl',
            '--exclude',
            '*.btpl',
            'common/',
            path,
        ]
    )
    template_dir = Path(path) / 'templates' / 'common'

    for model, fw_suffix in MODELS:
        # generate snom<model>-firmware.xml.tpl from snom-model-firmware.xml.tpl.btpl
        model_tpl = template_dir / f'snom{model}-firmware.xml.tpl'
        sed_script = f's/#FW_FILENAME#/snom{model}-10.1.184.15-SIP-{fw_suffix}.bin/'
        if model.startswith("D8"):
            sed_script = f's/#FW_FILENAME#/snom{model}-10.1.184.15-SIP-{fw_suffix}.swu/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                [
                    'sed',
                    sed_script,
                    'common/templates/common/snom-model-firmware.xml.tpl.btpl',
                ],
                stdout=f,
            )

        # generate snom<model>.htm.tpl from snom-model.htm.tpl.mtpl
        model_tpl = template_dir / f'snom{model}.htm.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.htm.tpl.btpl'],
                stdout=f,
            )

        # generate snom<model>.xml.tpl from snom-model.xml.mtpl
        model_tpl = template_dir / f'snom{model}.xml.tpl'
        sed_script = f's/#MODEL#/{model}/'
        with model_tpl.open(mode='wb') as f:
            check_call(
                ['sed', sed_script, 'common/templates/common/snom-model.xml.tpl.btpl'],
                stdout=f,
            )

    check_call(['rsync', '-rlp', '--exclude', '.*', 'v10_1_184_15/', path])
