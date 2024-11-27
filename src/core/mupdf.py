from collections.abc import Iterable
from typing import TYPE_CHECKING

from fitz import Document
from fitz.utils import get_pixmap
from promplate import Message

from ..utils.vision.encode import bytes_to_url

if TYPE_CHECKING:
    from ..utils.vision.types import ImageChunk, TextChunk


def get_thumbnails(pdf_path: str) -> Iterable[bytes]:
    with Document(pdf_path) as pdf:
        for page in pdf:
            img = get_pixmap(page, dpi=36 * 5)
            yield img.tobytes()


def construct_message(pdf_path: str) -> Message:
    content: list[ImageChunk | TextChunk] = [
        {
            "type": "image_url",
            "image_url": {"url": bytes_to_url(i, "png"), "detail": "low"},
        }
        for i in get_thumbnails(pdf_path)
    ]

    content.insert(0, {"type": "text", "text": "Here are the thumbnails of this PDF."})
    content.append({"type": "text", "text": "These thumbnails are meant to guide you in arranging the illustrations. The images in the last message should be in the format ![]()."})

    return {"role": "user", "content": content}  # type: ignore
