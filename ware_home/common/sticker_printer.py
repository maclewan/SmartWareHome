from typing import Optional

from django.conf import settings
from phomemo_printer.ESCPOS_constants import *
from phomemo_printer.ESCPOS_printer import Printer
from PIL import Image, ImageEnhance


class PhomemoT02Printer(Printer):
    def print_text(self, text):
        raise NotImplementedError(
            "This method requires some const changes in order to work properly."
        )

    def print_charset(self):
        raise NotImplementedError(
            "This method requires some const changes in order to work properly."
        )

    def print_image(
        self, image_path=None, image=None, brightness=None, normalize=False
    ):
        """
        Adjusted code from original library to fit into T-02 printing dimensions
        """
        if image is None and image_path is None:
            raise ValueError("Either image_path or image is required!")
        if image is None:
            image = Image.open(image_path)

        if normalize and (image.width > image.height):
            image = image.transpose(Image.ROTATE_90)

        # width 384 dots
        IMAGE_WIDTH_BYTES = 46  # t-02
        IMAGE_WIDTH_BITS = IMAGE_WIDTH_BYTES * 8
        image = image.resize(
            size=(IMAGE_WIDTH_BITS, int(image.height * IMAGE_WIDTH_BITS / image.width))
        )

        if brightness is not None:
            filter = ImageEnhance.Brightness(image)
            image = filter.enhance(brightness)

        # black&white printer: dithering
        image = image.convert(mode="1")

        self._print_bytes(HEADER)
        for start_index in range(0, image.height, 256):
            end_index = (
                start_index + 256 if image.height - 256 > start_index else image.height
            )
            line_height = end_index - start_index

            BLOCK_MARKER = (
                GSV0
                + bytes([IMAGE_WIDTH_BYTES])
                + b"\x00"
                + bytes([line_height - 1])
                + b"\x00"
            )
            self._print_bytes(BLOCK_MARKER)

            image_lines = []
            for image_line_index in range(line_height):
                image_line = b""
                for byte_start in range(int(image.width / 8)):
                    byte = 0
                    for bit in range(8):
                        if (
                            image.getpixel(
                                (byte_start * 8 + bit, image_line_index + start_index)
                            )
                            == 0
                        ):
                            byte |= 1 << (7 - bit)
                    # 0x0a breaks the rendering
                    # 0x0a alone is processed like LineFeed by the printe
                    if byte == 0x0A:
                        byte = 0x14
                    # self._print_bytes(byte.to_bytes(1, 'little'))
                    image_line += byte.to_bytes(1, "little")

                image_lines.append(image_line)

            for l in image_lines:
                self._print_bytes(l)

        self._print_bytes(PRINT_FEED)
        # self._print_bytes(PRINT_FEED)
        self._print_bytes(FOOTER)


def _get_printer_instance() -> PhomemoT02Printer:
    # Todo: make it cacheable (something singleton-ish)
    printer = PhomemoT02Printer(
        bluetooth_address=settings.STICKER_PRINTER_MAC,
        channel=settings.STICKER_PRINTER_CHANNEL,
    )
    return printer


def _concat_images_into_two_rows(image_list: list[Image]) -> Optional[Image]:
    img_height = settings.TARGET_QR_WIDTH + settings.QR_DESCR_HEIGHT
    img_width = settings.TARGET_QR_WIDTH
    column_gap = settings.COLUMN_GAP

    if len(image_list) == 0:
        return

    if len(image_list) % 2 == 1:
        # Adjust to print in 2 columns
        image_list += [Image.new("RGB", (img_width, img_height), color=(255, 255, 255))]

    rows = len(image_list) / 2

    final_width = int(2 * img_width) + column_gap
    final_height = int(rows * img_height)
    final_image = Image.new("RGB", (final_width, final_height), color=(255, 255, 255))

    for idx, img in enumerate(image_list):
        x = (idx % 2) * (img_width + column_gap)
        y = (idx // 2) * img_height
        final_image.paste(img, (x, y))

    return final_image


def batch_print_qr(images_list: list[Image]) -> bool:
    """
    :param images_list: List of images, all TARGET_QR_WIDTH px wide
    :returs True if printed, False if image was empty
    """
    concatenated_image = _concat_images_into_two_rows(images_list)
    if concatenated_image is None:
        return False
    printer = _get_printer_instance()
    printer.print_image(image=concatenated_image)
    return True
