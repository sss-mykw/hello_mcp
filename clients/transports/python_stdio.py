import asyncio
import os

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

base_dir = os.path.dirname(os.path.abspath(__file__))
server_script = os.path.join(base_dir, '..', '..', 'my_server.py')

# Option 1: Inferred transport
# client = Client(server_script)

# Option 2: Explicit transport with custom configuration
transport = PythonStdioTransport(
    script_path=server_script,
    python_cmd=os.path.join(base_dir, '..', '..', '.venv/bin/python3.13'), # Optional: specify Python interpreter
    # args=["--some-server-arg"],      # Optional: pass arguments to the script
    # env={"MY_VAR": "value"},         # Optional: set environment variables
)
client = Client(transport)

async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Connected via Python Stdio, found tools: {tools}")

asyncio.run(main())
