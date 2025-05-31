import asyncio
from fastmcp import Client, FastMCP

# FastMCPのアーキテクチャはトランスポートをプロトコルロジックから分離するようにしていいる

# [FastMCP Client]
# Transports
# Client automatically infers the transport type
client_in_memory = Client(FastMCP(name="TestServer"))
client_http = Client("https://example.com/mcp")
# サンプルコードとファイル名が異なる点に注意
client_stdio = Client("my_server.py")
config = {
    "mcpServers": {
        "local": {"command": "python", "args": ["local_server.py"]},
        "remote": {"url": "https://example.com/mcp"},
    }
}
client_config = Client(config)

print(client_in_memory.transport)
print(client_http.transport)
print(client_stdio.transport)
print(client_config.transport)
