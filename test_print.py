from ware_home.common.qr import _generate_qr
from ware_home.common.sticker_printer import _concat_images_into_two_rows, _get_printer_instance


def run(print=False):
    url = "qr.wikamaciek.pl/qr/123456789/44/"

    # Generate image:
    qr_img = _generate_qr(url, "(45): Zupa pomidorowa babci zosi")
    concatenated = _concat_images_into_two_rows([qr_img, qr_img, qr_img])

    if not print:
        qr_img.save("s.png")
        concatenated.save("tmp.png")
    else:
        printer = _get_printer_instance()
        printer.print_image(image=concatenated)
