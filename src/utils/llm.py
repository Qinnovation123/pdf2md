from promplate.llm.openai import AsyncChatGenerate
from promplate.prompt.chat import ensure
from promplate_trace.auto import patch
from rich.console import Console

from .log import print_token_usage
from .vision.print import show_prompt

generate = AsyncChatGenerate()


console = Console(markup=False)


@patch.chat.acomplete
async def complete(prompt, /, **kwargs):
    show_prompt(ensure(prompt))  # type: ignore

    res = ""
    async for i in generate(prompt, **kwargs):
        if i:
            res += i
            console.print(i, end="")

    print()

    print_token_usage(prompt, res)

    return res
