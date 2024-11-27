from __future__ import annotations

from typing import TYPE_CHECKING

from promplate import parse_chat_markup

from .core.mupdf import construct_message
from .core.pdfminer import extract_text
from .templates import template
from .utils.llm import complete
from .utils.vision.inject import patch_message

if TYPE_CHECKING:
    from .utils.vision.types import ExtendedMessage


async def process_pdf(pdf_path: str):
    text = extract_text(pdf_path)

    messages: list[ExtendedMessage] = parse_chat_markup(template.render({"content": text}))  # type: ignore
    patch_message(messages[1])  # type: ignore
    messages[1]["content"].extend(construct_message(pdf_path)["content"])  # type: ignore

    return await complete(messages, temperature=0, model="gpt-4o-mini")
