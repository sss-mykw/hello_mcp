import asyncio
import os

from fastmcp import Client

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', '..', 'my_server.py')
client = Client(file_path)

# Connection Lifecycle
# Tool Operations
# Resource OperationsやPrompt Operationsも似たような内容なのでスキップ
async def main():
    # Connection is established here
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        # Raw MCP Protocol Objects
        # デバッグ用途で使用するかもしれない
        raw_result = await client.list_tools_mcp()
        print(f"raw_result: {raw_result}")

        target_tool_name = "greet"
        if any(tool.name == target_tool_name for tool in tools):
            # タイムアウトを2秒に設定
            result = await client.call_tool(target_tool_name, arguments={"name": "World"}, timeout=2.0)
            print(f"Greet result: {result[0].text}")

    # Connection is closed automatically here
    print(f"Client connected: {client.is_connected()}")

if __name__ == "__main__":
    asyncio.run(main())
