import os

from fastmcp import Client, FastMCP

# FastMCPのアーキテクチャはトランスポートをプロトコルロジックから分離するようにしていいる

# [FastMCP Client]
# Transports
# Client automatically infers the transport type
client_in_memory = Client(FastMCP(name="TestServer"))
client_http = Client("https://example.com/mcp")
# サンプルコードとファイル名が異なる点に注意
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', '..', 'my_server.py')
client_stdio = Client(file_path)
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
