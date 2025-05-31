import asyncio
import os

from fastmcp import Client

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', '..', 'my_server.py')
client = Client(file_path)

# Connection Lifecycle
async def main():
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        target_tool_name = "greet"
        if any(tool.name == target_tool_name for tool in tools):
            result = await client.call_tool(target_tool_name, {"name": "World"})
            print(f"Greet result: {result}")

    # Connection is closed automatically here
    print(f"Client connected: {client.is_connected()}")

if __name__ == "__main__":
    asyncio.run(main())
