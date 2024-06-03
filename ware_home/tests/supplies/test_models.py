import pytest
from django.utils import timezone
from freezegun import freeze_time

from ware_home.supplies.models import Supply
from ware_home.tests.factories import SupplyFactory

pytestmark = pytest.mark.django_db


@freeze_time("2107-04-02")
@pytest.mark.parametrize(
    "days_delta, expected_expiration_state",
    [
        (-16, "expired"),
        (1, "expired"),
        (2, "soon_to_expire"),
        (15, "soon_to_expire"),
        (21, "good"),
        (370, "good"),
    ],
)
def test_supply_qs(days_delta, expected_expiration_state):
    SupplyFactory(
        expiration_date=timezone.now().date() + timezone.timedelta(days=days_delta)
    )
    qs = Supply.objects.annotate_expiration_state()
    assert qs.count() == 1
    assert qs.first().days_to_expiration == days_delta
    assert qs.first().expiration_state == expected_expiration_state
