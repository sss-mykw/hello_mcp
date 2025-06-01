from fastmcp import FastMCP, Client
import asyncio

# [Advanced Features]

server = FastMCP(name="InMemoryServer")

@server.tool()
def ping():
    return "pong"

#----------------Server–client boundary----------------

client = Client(server)

async def main():
    async with client:
        result = await client.call_tool("ping")
        print(f"In-memory call result: {result}")

asyncio.run(main())
