from asyncio import run

from src.api import process_pdf

run(process_pdf("example.pdf"))
