from asyncio import to_thread
from collections.abc import AsyncIterable
from io import BytesIO
from typing import Literal, TypedDict, assert_never, overload

from promplate import parse_chat_markup
from pydantic import TypeAdapter

from .templates import extract, pdf2md
from .utils.llm import complete, generate

type Engine = Literal["pdfminer", "pymupdf", "auto"]


def extract_text(pdf_path: BytesIO, /, max_pages: int | None = None, engine: Engine = "auto"):
    match engine:
        case "pdfminer":
            from pdfminer.high_level import extract_text as extract

            return extract(pdf_path, maxpages=max_pages or 0)
        case "pymupdf":
            from pymupdf import Document

            doc = Document(stream=pdf_path, filetype="pdf")
            return "\n\n".join(page.get_textpage().extractText() for page in doc[:max_pages])
        case "auto":
            try:
                return extract_text(pdf_path, max_pages, "pymupdf")
            except Exception:
                return extract_text(pdf_path, max_pages, "pdfminer")
        case _ as never:
            assert_never(never)


@overload
async def pdf_to_markdown(pdf_path) -> str: ...
@overload
async def pdf_to_markdown(pdf_path, stream: Literal[False]) -> str: ...
@overload
async def pdf_to_markdown(pdf_path, stream: Literal[True]) -> AsyncIterable[str]: ...


async def pdf_to_markdown(pdf_path, stream=False):
    text = await to_thread(extract_text, pdf_path)

    messages = parse_chat_markup(pdf2md.render({"content": text}))

    return generate(messages) if stream else await complete(messages)


Metadata = TypedDict("Metadata", {"title": str, "abstract": str, "keywords": list[str], "success": Literal[True]}) | TypedDict("Error", {"success": Literal[False]})
validator = TypeAdapter(Metadata)


async def parse_pdf_metadata(pdf_path, max_pages=None, max_tokens=None):
    text = await to_thread(extract_text, pdf_path, max_pages)

    if max_tokens:
        from .utils.token_limit import limit_tokens

        text = limit_tokens(text, max_tokens)

    messages = parse_chat_markup(extract.render({"content": text}))

    res = await complete(messages, response_format={"type": "json_object"})
    return validator.validate_json(res)
