from io import BytesIO
from textwrap import indent
from traceback import format_exc

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse

from src.api import Metadata, parse_pdf_metadata, pdf_to_markdown
from src.utils.llm import console
from src.utils.response import make_streaming_response

app = FastAPI(title="PDF to Markdown API", version="dev")


@app.get("/", include_in_schema=False)
def _():
    return RedirectResponse("/docs")


@app.post("/convert", response_model=str, response_class=PlainTextResponse)
async def convert_pdf_to_markdown(pdf: bytes = Body(media_type="application/pdf"), stream: bool = True):
    try:
        if stream:
            return await make_streaming_response(await pdf_to_markdown(BytesIO(pdf), stream=True), media_type="text/markdown")
        else:
            return PlainTextResponse(await pdf_to_markdown(BytesIO(pdf)), media_type="text/markdown")
    except Exception as e:
        console.print("\n" + indent(format_exc().strip(), " ") + "\n", style="red")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/extract", response_model=Metadata)
async def parse_metadata_from_pdf(pdf: bytes = Body(media_type="application/pdf"), max_pages: int = 6, max_tokens: int = 3500):
    try:
        return await parse_pdf_metadata(BytesIO(pdf), max_pages, max_tokens)
    except Exception as e:
        console.print("\n" + indent(format_exc().strip(), " ") + "\n", style="red")
        raise HTTPException(status_code=500, detail=str(e)) from e
