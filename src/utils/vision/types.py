from typing import Literal, NotRequired, TypedDict

from promplate import Message


class TextChunk(TypedDict):
    type: Literal["text"]
    text: str


class ImageURL(TypedDict):
    url: str
    detail: NotRequired[Literal["auto", "low", "high"]]


class ImageChunk(TypedDict):
    type: Literal["image_url"]
    image_url: ImageURL


class ExtendedMessage(Message):
    content: str | list[TextChunk | ImageChunk]  # type: ignore
