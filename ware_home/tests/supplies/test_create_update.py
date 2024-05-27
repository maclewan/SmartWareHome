import pytest
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status

from ware_home.tests.factories import CategoryFactory, ProductFactory
from ware_home.tests.typing import AnyInteger

pytestmark = pytest.mark.django_db


def test_update_product(admin_api_client):
    product = ProductFactory(
        bar_code="21379",
        description="Burak z soku",
        name="Dawtona sok",
        volume="423ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Buraki"),
        ],
    )
    url = reverse("product-detail", kwargs={"bar_code": product.bar_code})
    response = admin_api_client.patch(
        url,
        data={
            "name": "Sok dawtona",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "bar_code": "21379",
        "categories": [
            {"id": AnyInteger(), "name": "Soki"},
            {"id": AnyInteger(), "name": "Buraki"},
        ],
        "description": "Burak z soku",
        "id": product.id,
        "name": "Sok dawtona",
        "volume": "423ml",
    }


def test_create_product(admin_api_client):
    product_data = dict(
        bar_code="21380",
        description="Description to be created",
        name="Tymbark pomarancza",
        volume="424ml",
    )
    url = reverse("product-create")
    response = admin_api_client.post(
        url,
        data=product_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "bar_code": "21380",
        "categories": [],
        "description": "Description to be created",
        "id": AnyInteger(),
        "name": "Tymbark pomarancza",
        "volume": "424ml",
    }


@freeze_time("2107-04-02")
def test_create_supply(admin_api_client):
    product = ProductFactory()

    supply_data = dict(
        product=product.id,
        amount=5.5,
        expiration_date=timezone.now().date() + timezone.timedelta(days=5),
    )

    url = reverse("supply-create")
    response = admin_api_client.post(
        url,
        data=supply_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "created_at": "2107-04-02T02:00:00+02:00",
        "updated_at": "2107-04-02T02:00:00+02:00",
        "expiration_date": "2107-04-07",
        "id": 1,
        "product": product.id,
        "amount": "5.5",
    }
