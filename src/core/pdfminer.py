from hashlib import md5
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
            sha = md5(image.stream.get_data()).hexdigest()
            filename = sha[:6] + ext
            path = Path(self.outdir, filename)
            while path.exists() and md5(path.read_bytes()).hexdigest() != sha:
                sha = md5(sha.encode()).hexdigest()
                filename = sha[:6] + ext
                path = Path(self.outdir, filename)

            out.write(f" ![](./{filename}) ")
            return filename, str(path.resolve())

    manager = PDFResourceManager()
    device = TextConverter(manager, out, imagewriter=OurImageWriter("."), laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, device)

    with Path(pdf_path).open("rb") as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)

    device.close()

    return out.getvalue()
