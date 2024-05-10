from unittest.mock import Mock

import pytest
from django.utils import timezone as tz

from ware_home.common.utils import check_expiration_date, get_expiration_days


@pytest.mark.parametrize(
    "obj, days",
    [
        (Mock(expiration_date=tz.now().date()), 0),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=2)),
            2,
        ),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=-3)),
            -3,
        ),
    ],
)
def test_expiration_days(obj, days):
    assert get_expiration_days(obj) == days


@pytest.mark.parametrize(
    "obj, expired",
    [
        (Mock(expiration_date=tz.now().date()), True),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=1)),
            False,
        ),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=2)),
            False,
        ),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=-1)),
            True,
        ),
        (
            Mock(expiration_date=tz.now().date() + tz.timedelta(days=-5)),
            True,
        ),
    ],
)
def test_expiration_date(obj, expired):
    assert check_expiration_date(obj) is expired
