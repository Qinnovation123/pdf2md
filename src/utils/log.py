from __future__ import annotations

from traceback import format_exception_only
from typing import TYPE_CHECKING

from promplate.prompt.chat import ensure
from promptools.openai.tokenize import cached_get_encoding, count_token
from rich.console import Console

if TYPE_CHECKING:
    from ..utils.vision.types import ExtendedMessage, Message

console = Console()

enc = cached_get_encoding("o200k_base")


def simplify_messages(messages: list[ExtendedMessage]) -> list[Message]:
    return [{"role": m["role"], "content": m["content"] if isinstance(m["content"], str) else "".join(part["text"] for part in m["content"] if part["type"] == "text")} for m in messages]


def print_token_usage(prompt, completion):
    a = count_token(simplify_messages(ensure(prompt)), enc)  # type: ignore
    b = count_token(completion, enc)
    c = a + b
    console.print(
        f"\n [r] usages [/r] {a} + {b} = {c} [green]$ {(a * 0.15 + b * 0.6) / 1_000} / 1k rounds",
        style="bright_red",
    )


def print_exception_only(exc: Exception):
    console.log(format_exception_only(exc), style="bright_red")


def print_label(label: str):
    console.print(f"\n [r] {label} [/r] ", end="", style="bright_magenta")


def print_results(content, highlight=False):
    console.print(content, style="bright_magenta", highlight=highlight)
