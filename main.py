from io import BytesIO
from textwrap import indent
from traceback import format_exc

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse

from src.api import process_pdf
from src.utils.llm import console

app = FastAPI(title="PDF to Markdown API", version="dev")


@app.get("/", include_in_schema=False)
def _():
    return RedirectResponse("/docs")


@app.post("/convert", response_model=str, response_class=PlainTextResponse)
async def convert_pdf_to_markdown(pdf: bytes = Body(media_type="application/pdf")) -> str:
    try:
        return await process_pdf(BytesIO(pdf))
    except Exception as e:
        console.print("\n" + indent(format_exc().strip(), " ") + "\n", style="red")
        raise HTTPException(status_code=500, detail=str(e))
