import pytest
from rest_framework.test import APIClient

from ware_home.users.models import User


@pytest.fixture(name="api_client")
def fixture_api_client() -> APIClient:
    return APIClient()


@pytest.fixture(name="admin_api_client")
def fixture_admin_api_client(api_client: APIClient) -> APIClient:
    user, _ = User.objects.get_or_create(is_staff=True)
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client
