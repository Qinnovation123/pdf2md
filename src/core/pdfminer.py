from io import StringIO
from pathlib import Path

from pdfminer.converter import TextConverter
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams, LTImage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text(pdf_path: str):
    out = StringIO()

    class OurImageWriter(ImageWriter):
        def _create_unique_image_name(self, image: LTImage, ext: str):
            filename, path = super()._create_unique_image_name(image, ext)
            out.write(f" ![]({filename}) ")  # TODO: change this
            return filename, path

    manager = PDFResourceManager()
    device = TextConverter(manager, out, imagewriter=OurImageWriter("."), laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, device)

    with Path(pdf_path).open("rb") as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)

    device.close()

    return out.getvalue()
