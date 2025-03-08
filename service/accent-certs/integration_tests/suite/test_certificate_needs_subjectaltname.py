# Copyright 2023 Accent Communications

import subprocess

from hamcrest import (
    assert_that,
    equal_to,
)


def test_certificate_needs_subjectaltname_true():
    return_code = subprocess.call(
        [
            '../bin/certificate-needs-subjectaltname',
            'assets/certificate-without-subjectaltname.crt',
        ]
    )
    assert_that(return_code, equal_to(0))
    return_code = subprocess.call(
        [
            '../bin/certificate-needs-subjectaltname',
            'assets/certificate-not-generated-by-accent.crt',
        ]
    )
    assert_that(return_code, equal_to(1))
    return_code = subprocess.call(
        [
            '../bin/certificate-needs-subjectaltname',
            'assets/certificate-with-subjectaltname.crt',
        ]
    )
    assert_that(return_code, equal_to(1))
