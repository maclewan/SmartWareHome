from PIL import Image

from ware_home.common.qr import generate_qr_from_details
from ware_home.supplies.models import Supply


def _generate_qr_for_supply(supply: Supply) -> Image:
    bar_code = supply.product.bar_code
    supply_id = str(supply.id)
    product_name = supply.product.name
    description = f"[{supply_id}]: {bar_code}", product_name
    return generate_qr_from_details(bar_code, supply_id, description)


def bulk_generate_qrs_for_supplies(supply_id_list: list[int]) -> list[Image]:
    qs = Supply.objects.select_related("product").filter(id__in=supply_id_list)
    images_list = [_generate_qr_for_supply(supply) for supply in qs]
    return images_list
