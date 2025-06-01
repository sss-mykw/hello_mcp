from fastmcp import FastMCP, Client
import asyncio

# [In-Memory Transports]
# FastMCP Transport
# UTで使える
# 1. Create your FastMCP server instance
server = FastMCP(name="InMemoryServer")

@server.tool()
def ping():
    return "pong"

# 2. Create a client pointing directly to the server instance
client = Client(server)  # Transport is automatically inferred

async def main():
    async with client:
        result = await client.call_tool("ping")
        print(f"In-memory call result: {result}")

asyncio.run(main())
