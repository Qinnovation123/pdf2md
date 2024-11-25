from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    from .types import ExtendedMessage

console = Console(markup=False, highlight=False)


def show_prompt(messages: list[ExtendedMessage]):
    for message in messages:
        match message["role"]:
            case "assistant":
                style = "green"
            case "user":
                style = "yellow"
            case _:
                style = "red"

        content = message["content"]

        if isinstance(content, str):
            console.print(content, style=style)
        else:
            console.print("".join(part["text"] for part in content if part["type"] == "text"), style=style)

        print()
