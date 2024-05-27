import pytest
from django.urls import reverse
from rest_framework import status

from ware_home.tests.factories import CategoryFactory, ProductFactory
from ware_home.tests.typing import AnyInteger

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
