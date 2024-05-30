import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from ware_home.supplies.models import Supply
from ware_home.tests.factories import CategoryFactory, ProductFactory, SupplyFactory
from ware_home.tests.typing import AnyDateTime, AnyInteger

pytestmark = pytest.mark.django_db


def test_retrieve_product(admin_api_client):
    product = ProductFactory(
        bar_code="21378",
        description="Sok z buraka",
        name="Dawtona sok",
        volume="421ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Buraki"),
        ],
    )
    url = reverse("product-detail", kwargs={"bar_code": product.bar_code})
    response = admin_api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "bar_code": "21378",
        "categories": [
            {"id": AnyInteger(), "name": "Soki"},
            {"id": AnyInteger(), "name": "Buraki"},
        ],
        "description": "Sok z buraka",
        "id": product.id,
        "name": "Dawtona sok",
        "volume": "421ml",
    }


def test_filter_supply(admin_api_client):
    product_1 = ProductFactory(
        bar_code="213781",
        description="Sok z pomidora",
        name="Dawtona pomidora",
        volume="422ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Pomidor"),
        ],
    )
    product_2 = ProductFactory(
        bar_code="213782",
        description="Sok z ogórka",
        name="Dawtona ogórka",
        volume="423ml",
        categories=[
            CategoryFactory(name="Soki"),
        ],
    )
    supply_1 = SupplyFactory(
        product=product_1,
        expiration_date=timezone.now().date() - timezone.timedelta(days=30),
    )
    supply_2 = SupplyFactory(
        product=product_1,
        expiration_date=timezone.now().date() - timezone.timedelta(days=20),
    )
    _ = SupplyFactory(product=product_2)
    _ = SupplyFactory(product=product_2)

    url = reverse("supply-filter-list", kwargs={"bar_code": product_1.bar_code})
    response = admin_api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "amount": f"{supply_1.amount:.1f}",
            "created_at": AnyDateTime(),
            "expiration_date": supply_1.expiration_date.strftime("%Y-%m-%d"),
            "id": supply_1.id,
            "product": product_1.id,
            "updated_at": AnyDateTime(),
        },
        {
            "amount": f"{supply_2.amount:.1f}",
            "created_at": AnyDateTime(),
            "expiration_date": supply_2.expiration_date.strftime("%Y-%m-%d"),
            "id": supply_2.id,
            "product": product_1.id,
            "updated_at": AnyDateTime(),
        },
    ]


def test_pop_supply_lower_amount(admin_api_client):
    product = ProductFactory(
        bar_code="213782",
        description="Sok z papryki",
        name="Dawtona papryk",
        volume="423ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Papryki"),
        ],
    )
    supply = SupplyFactory(
        product=product, expiration_date=timezone.now().date(), amount=1
    )

    url = reverse("supply-pop-amount", kwargs={"id": supply.id})
    response = admin_api_client.post(url, data={"amount_to_pop": "0.5"})
    supply.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "amount": f"0.5",
        "created_at": AnyDateTime(),
        "expiration_date": supply.expiration_date.strftime("%Y-%m-%d"),
        "id": supply.id,
        "product": product.id,
        "updated_at": AnyDateTime(),
    }
    assert supply.amount == 0.5


def test_pop_supply_exceeding_amount(admin_api_client):
    product = ProductFactory(
        bar_code="213782",
        description="Sok z papryki",
        name="Dawtona papryk",
        volume="423ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Papryki"),
        ],
    )
    supply = SupplyFactory(
        product=product, expiration_date=timezone.now().date(), amount=2
    )

    url = reverse("supply-pop-amount", kwargs={"id": supply.id})
    response = admin_api_client.post(url, data={"amount_to_pop": "2.5"})
    supply.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "amount_to_pop": ["Cannot pop more amount that in stock."]
    }
    assert supply.amount == 2


def test_pop_supply_zero_amount(admin_api_client):
    product = ProductFactory(
        bar_code="213782",
        description="Sok z papryki",
        name="Dawtona papryk",
        volume="423ml",
        categories=[
            CategoryFactory(name="Soki"),
            CategoryFactory(name="Papryki"),
        ],
    )
    supply = SupplyFactory(
        product=product, expiration_date=timezone.now().date(), amount=1.5
    )

    url = reverse("supply-pop-amount", kwargs={"id": supply.id})
    response = admin_api_client.post(url, data={"amount_to_pop": "1.5"})

    with pytest.raises(ObjectDoesNotExist, match="matching query does not exist"):
        supply.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
