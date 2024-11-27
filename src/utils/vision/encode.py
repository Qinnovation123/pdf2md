from base64 import b64encode
from pathlib import Path


def bytes_to_url(data: bytes, ext: str):
    base64 = b64encode(data).decode()
    return f"data:image/{ext};base64,{base64}"


def image_to_url(path: str):
    file = Path(path)
    base64 = b64encode(file.read_bytes()).decode()
    return f"data:image/{file.suffix[1:]};base64,{base64}"
