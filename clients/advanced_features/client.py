from fastmcp import FastMCP, Client
import asyncio

from fastmcp.client.logging import LogMessage

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


client = Client(
    server,
    log_handler=log_handler,
)

async def main():
    async with client:
        result = await client.call_tool("ping")
        print(f"In-memory call result: {result}")

asyncio.run(main())
