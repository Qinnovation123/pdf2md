from collections.abc import AsyncIterable
from typing import Literal, overload

from pdfminer.high_level import extract_text
from promplate import parse_chat_markup

from .templates import template
from .utils.llm import complete, generate


@overload
async def process_pdf(pdf_path) -> str: ...
@overload
async def process_pdf(pdf_path, stream: Literal[False]) -> str: ...
@overload
async def process_pdf(pdf_path, stream: Literal[True]) -> AsyncIterable[str]: ...


async def process_pdf(pdf_path, stream=False):  # type: ignore
    text = extract_text(pdf_path)

    messages = parse_chat_markup(template.render({"content": text}))

    if stream:
        return generate(messages, temperature=0, model="gpt-4o-mini")
    return await complete(messages, temperature=0, model="gpt-4o-mini")
