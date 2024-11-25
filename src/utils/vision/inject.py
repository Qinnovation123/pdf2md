from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .encode import image_to_url

if TYPE_CHECKING:
    from .types import ImageChunk, Message, TextChunk


def inject_images(content: str) -> str | list[TextChunk | ImageChunk]:
    if re.search(r"!\[[^\]]*\]\([^\)]+\)", content) is None:
        return content

    results: list[TextChunk | ImageChunk] = []

    for chunk in re.split(r"(!\[[^\]]*\]\([^\)]+\))", content):
        results.append({"type": "text", "text": chunk})
        if re.match(r"!\[[^\]]*\]\([^\)]+\)", chunk):
            match = re.match(r"!\[([^\]]*)\]\(([^\)]+)\)", chunk)
            assert match is not None
            image_path = match.group(2)
            assert isinstance(image_path, str), image_path
            results.append({"type": "image_url", "image_url": {"url": image_to_url(image_path)}})

    return results


def patch_message(message: Message):
    message["content"] = inject_images(message["content"])  # type: ignore
