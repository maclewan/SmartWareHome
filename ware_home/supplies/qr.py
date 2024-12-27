from PIL import Image

from ware_home.common.qr import generate_qr_from_details
from ware_home.supplies.models import Supply, SupplyQuerySet


def _generate_qr_for_supply(supply: Supply) -> Image:
    bar_code = supply.product.bar_code
    supply_id = str(supply.id)
    product_name = supply.product.name
    description = f"[{supply_id}]: {bar_code}", product_name
    return generate_qr_from_details(bar_code, supply_id, description)


def bulk_generate_qrs_for_supplies(supplies_qs: SupplyQuerySet) -> list[Image]:
    images_list = [_generate_qr_for_supply(supply) for supply in supplies_qs]
    return images_list
