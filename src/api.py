from collections.abc import AsyncIterable
from io import BytesIO
from typing import Literal, TypedDict, assert_never, overload

from promplate import parse_chat_markup
from pydantic import TypeAdapter

from .templates import extract, pdf2md
from .utils.llm import complete, generate

type Engine = Literal["pdfminer", "pymupdf", "auto"]


def extract_text(pdf_path: BytesIO, /, engine: Engine = "auto"):
    match engine:
        case "pdfminer":
            from pdfminer.high_level import extract_text as extract

            return extract(pdf_path)
        case "pymupdf":
            from pymupdf import Document

            doc = Document(stream=pdf_path, filetype="pdf")
            return "\n\n".join(page.get_textpage().extractText() for page in doc)
        case "auto":
            try:
                return extract_text(pdf_path, "pymupdf")
            except Exception:
                return extract_text(pdf_path, "pdfminer")
        case _ as never:
            assert_never(never)


@overload
async def pdf_to_markdown(pdf_path) -> str: ...
@overload
async def pdf_to_markdown(pdf_path, stream: Literal[False]) -> str: ...
@overload
async def pdf_to_markdown(pdf_path, stream: Literal[True]) -> AsyncIterable[str]: ...


async def pdf_to_markdown(pdf_path, stream=False):
    text = extract_text(pdf_path)

    messages = parse_chat_markup(pdf2md.render({"content": text}))

    if stream:
        return generate(messages, temperature=0, model="grok-2-1212")
    return await complete(messages, temperature=0, model="grok-2-1212")


Metadata = TypedDict("Metadata", {"title": str, "abstract": str, "keywords": list[str], "success": Literal[True]}) | TypedDict("Error", {"success": Literal[False]})
validator = TypeAdapter(Metadata)


async def parse_pdf_metadata(pdf_path):
    text = extract_text(pdf_path)

    messages = parse_chat_markup(extract.render({"content": text}))

    res = await complete(messages, temperature=0, model="grok-2-1212", response_format={"type": "json_object"})
    return validator.validate_json(res)
