from pdfminer.high_level import extract_text
from promplate import parse_chat_markup

from .templates import template
from .utils.llm import complete


async def process_pdf(pdf_path):
    text = extract_text(pdf_path)

    messages = parse_chat_markup(template.render({"content": text}))

    return await complete(messages, temperature=0, model="gpt-4o-mini")
