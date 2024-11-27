from fastapi.responses import StreamingResponse
from starlette.responses import AsyncContentStream


async def make_streaming_response(stream: AsyncContentStream, media_type: str):
    it = aiter(stream)

    first_chunk = await anext(it)

    async def _():
        yield first_chunk
        async for i in it:
            yield i

    return StreamingResponse(_(), media_type=media_type)
