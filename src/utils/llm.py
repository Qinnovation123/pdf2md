from asyncio import Lock

from promplate.llm.openai import AsyncChatGenerate
from promplate.prompt.chat import ensure
from promplate_trace.auto import patch
from rich.console import Console

from .log import print_token_usage
from .vision.print import show_prompt

generate = patch.chat.agenerate(AsyncChatGenerate())


console = Console(markup=False)


def fix_json(json: str):
    from partial_json_parser import ensure_json

    return ensure_json(json)


lock = Lock()


async def _debug_complete(prompt, /, **kwargs):
    res = ""
    from rich.live import Live

    if is_json := kwargs.get("response_format", {}).get("type", "text") != "text":
        from rich.json import JSON as Render  # noqa: N811
    else:
        from .rich_markdown import Markdown as Render

    async with lock:
        with Live(vertical_overflow="visible") as live:
            async for i in generate(prompt, **kwargs):
                if i:
                    res += i
                    live.update(Render(fix_json(res) if is_json else res), refresh=True)

        print()
        print_token_usage(prompt, res)

    return res


async def complete(prompt, /, pretty=__debug__, **kwargs):
    show_prompt(ensure(prompt))  # type: ignore

    kwargs |= {"reasoning_effort": "low", "model": "grok-3-mini-beta", "temperature": 0}

    if pretty:
        return await _debug_complete(prompt, **kwargs)

    res = ""
    async for i in generate(prompt, **kwargs):
        if i:
            res += i
            console.print(i, end="")

    print()

    print_token_usage(prompt, res)

    return res
