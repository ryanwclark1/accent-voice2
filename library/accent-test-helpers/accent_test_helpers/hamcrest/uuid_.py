# Copyright 2023 Accent Communications

from functools import partial

from hamcrest import matches_regexp

uuid_ = partial(
    matches_regexp, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
)
