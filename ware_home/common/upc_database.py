from dataclasses import dataclass

import requests
from django.conf import settings


@dataclass
class ProductData:
    title: str
    barcode: str
    description: str
    category: str
    quantity: str


@dataclass
class UpcDbResponse:
    code: int
    product: ProductData | None = None


class UpcDbApi:
    BASE_URL = "https://api.upcdatabase.org"
    API_KEY = settings.UPC_DATABASE_API_KEY

    @classmethod
    def _assure_credentials(cls):
        if cls.API_KEY != "":
            return
        raise RuntimeError("UPC_DATABASE_API_KEY is missing!")

    @classmethod
    def get_product(cls, code: str) -> UpcDbResponse:
        cls._assure_credentials()
        response = requests.get(
            url=f"{cls.BASE_URL}/product/{code}",
            headers={"Authorization": f"Bearer {cls.API_KEY}"},
        )
        if response.status_code != 200:
            # This is example of this kind of api, which always returns 200...
            raise RuntimeError("UpcDatabase api failed.")
        response_data = response.json()
        print(response_data)
        if response_data.get("success") is not True:
            return UpcDbResponse(code=response_data["error"]["code"])
        return UpcDbResponse(
            code=200,
            product=ProductData(
                title=response_data["title"],
                barcode=response_data["barcode"],
                description=response_data["description"],
                category=response_data["category"],
                quantity=response_data.get("metadata", dict()).get(
                    "quantity", ""
                ),
            ),
        )
