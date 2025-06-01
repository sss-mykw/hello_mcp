from fastmcp import Client
import asyncio

from fastmcp.client import StreamableHttpTransport

# [Network Transports]
# Streamable HTTP
# The Client automatically uses StreamableHttpTransport for HTTP URLs
#client = Client("https://example.com/mcp")

# You can also explicitly instantiate the transport:
# デフォルトだと末尾にmcpが必要な点に注意
url = "http://127.0.0.1:8000/mcp"
# url = "http://127.0.0.1:8000/my-custom-path"
transport = StreamableHttpTransport(
    url=url,
    headers={"Authorization": "Bearer your-token-here"}
)
client = Client(transport)

async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


if __name__ == "__main__":
    asyncio.run(main())
