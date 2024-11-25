from promplate import parse_chat_markup

from .core.pdfminer import extract_text
from .templates import template
from .utils.llm import complete
from .utils.vision.inject import patch_message


async def process_pdf(pdf_path: str):
    text = extract_text(pdf_path)

    messages = parse_chat_markup(template.render({"content": text}))
    patch_message(messages[1])  # the user message

    return await complete(messages, temperature=0, model="gpt-4o-mini")
