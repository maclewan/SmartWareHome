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
            raise RuntimeError("UpcDatabase api failed.")

        response_data = response.json()
        if response_data.get("success") is not True:
            # This is example of this kind of api, which always returns 200...
            return UpcDbResponse(code=response_data["error"]["code"])

        metadata = response_data.get("metadata")
        metadata = metadata if metadata is not None else dict()

        return UpcDbResponse(
            code=200,
            product=ProductData(
                title=response_data["title"],
                barcode=response_data["barcode"],
                description=response_data["description"],
                category=response_data["category"],
                quantity=metadata.get("quantity", ""),
            ),
        )

    @classmethod
    def post_product(cls, product_data: ProductData) -> bool:
        raise NotImplementedError(
            "UpcDatabase post endpoint is currently broken."
        )
        # For some reason all requests causes`MySQL has encountered an error.Unknown column 'mpn' in 'field list'` error
        # Possible solution might be to use some automation script and add products on upcdatabase.org website
        # which seems to be adding products properly
        cls._assure_credentials()
        payload = {
            "title": product_data.title,
            "description": product_data.description,
            "alias": "",
            "brand": "",
            "manufacturer": "",
            "asin": "",
            "msrp": "",
            "category": product_data.category,
            "metadata": (
                {
                    "quantity": product_data.quantity,
                }
                if product_data.quantity
                else None
            ),
        }
        response = requests.post(
            url=f"{cls.BASE_URL}/product/{product_data.barcode}",
            headers={"Authorization": f"Bearer {cls.API_KEY}"},
            data=payload,
        )

        if response.status_code != 200:
            raise RuntimeError("UpcDatabase api failed.")

        response_data = response.json()
        return bool(response_data.get("success"))
