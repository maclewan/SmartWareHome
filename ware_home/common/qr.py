import qrcode
from django.conf import settings
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
from qrcode import QRCode
from qrcode.image.pil import PilImage


def _generate_qr(content: str, description: tuple[str, str]) -> Image:
    font_path = settings.QR_FONT_PATH
    target_dimensions = (settings.TARGET_QR_WIDTH, settings.TARGET_QR_WIDTH)
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=1,
    )
    qr.add_data(content)
    qr.make(fit=True)

    pil_image: PilImage = qr.make_image(fill_color="black", back_color="white")
    image = pil_image.get_image()
    image.thumbnail(target_dimensions)
    width, height = image.size

    new_image = Image.new(
        "RGB", (width, height + settings.QR_DESCR_HEIGHT), color=(255, 255, 255)
    )
    new_image.paste(image, (0, 0))

    draw = ImageDraw.Draw(new_image)

    descr_line_1, descr_line_2 = description

    # Line 1
    font = ImageFont.truetype(font_path, size=30)
    bbox = draw.textbbox((0, 0), descr_line_1, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = height - text_height + 25

    draw.text((text_x, text_y), descr_line_1, fill="black", font=font)

    # Line 2
    if len(descr_line_2) > 27:
        descr_line_2 = descr_line_2[:25] + "..."

    font = ImageFont.truetype(font_path, size=25)
    bbox = draw.textbbox((0, 0), descr_line_2, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = height - text_height + 50

    draw.text((text_x, text_y), descr_line_2, fill="black", font=font)

    return new_image


def _generate_pop_stock_url(bar_code: str, supply_id: str) -> str:
    # Short params name to create as compact qr as possible
    qr_url = settings.BASE_DOMAIN + reverse(
        "qr-redirect",
        kwargs={
            "bar_code": bar_code,
            "supply_id": supply_id,
        },
    )
    return qr_url


def generate_qr_from_details(
    bar_code: str, supply_id: str, description: tuple[str, str]
) -> Image:
    qr_url = _generate_pop_stock_url(bar_code, supply_id)
    return _generate_qr(qr_url, description)
