import marvin
from fastmcp import FastMCP, Client
import asyncio

from fastmcp.client.logging import LogMessage
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)

# [Advanced Features]

server = FastMCP(name="InMemoryServer")

@server.tool()
def ping():
    return "pong"

#----------------Server–client boundary----------------

# Logging and Notifications
async def log_handler(message: LogMessage):
    level = message.level.upper()
    logger = message.logger or 'default'
    data = message.data
    print(f"[Server Log - {level}] {logger}: {data}")

# Progress Monitoring
async def my_progress_handler(
    progress: float,
    total: float | None,
    message: str | None
) -> None:
    print(f"Progress: {progress} / {total} ({message})")

# LLM Sampling
async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    return await marvin.say_async(
        message=[m.content.text for m in messages],
        instructions=params.systemPrompt,
    )


client = Client(
    server,
    log_handler=log_handler,
    progress_handler=my_progress_handler,
    sampling_handler=sampling_handler,
)

async def main():
    async with client:
        result = await client.call_tool("ping")
        print(f"In-memory call result: {result}")

asyncio.run(main())
