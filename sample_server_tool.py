import asyncio

import aiohttp
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from pydantic import Field

# 名前を付けることでクライアント側やログからサーバーを特定するのに役立つ
# 引数instructionsではサーバーとのやり取り方法についての指示を指定出来る
mcp = FastMCP(
    name="My MCP Server",
    on_duplicate_tools="error" # 同じ命名のtoolが登録された場合にValueErrorに倒す
)


# [Tools]
# 関数名、docや引数の型情報からLLMがどういう道具かを認識する
# 型情報などを記載することで不正チェックを実施出来る
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b


# Pydanticを用いると、より詳細な引数の制約を指示することが出来る
@mcp.tool()
def search_database(
    query: str = Field(description="Search query string"),
    limit: int = Field(10, description="Maximum number of results", ge=1, le=100)
) -> list:
    """Search the database with the provided query."""
    # Implementation...


# @mcp.toolを用いて関数のメタデータを指示するパターン
# 関数のシグネチャーからの推論を上書きする（@mcp.toolが優先される）
@mcp.tool(
    name="find_products",           # Custom tool name for the LLM
    description="Search the product catalog with optional category filtering.", # Custom description
    tags={"catalog", "search"}      # Optional tags for organization/filtering
)
def search_products_implementation(query: str, category: str | None = None) -> list[dict]:
    """Internal function description (ignored if description is provided above)."""
    # Implementation...
    print(f"Searching for '{query}' in category '{category}'")
    return [{"id": 2, "name": "Another Product"}]


# Synchronous tool (suitable for CPU-bound or quick tasks)
@mcp.tool()
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the distance between two coordinates."""
    # Implementation...
    return 42.5

# Asynchronous tool (ideal for I/O-bound operations)
@mcp.tool()
async def fetch_weather(city: str) -> dict:
    """Retrieve current weather conditions for a city."""
    # Use 'async def' for operations involving network calls, file I/O, etc.
    # This prevents blocking the server while waiting for external operations.
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/weather/{city}") as response:
            # Check response status before returning
            response.raise_for_status()
            return await response.json()


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""

    if b == 0:
        # Error messages from ToolError are always sent to clients,
        # regardless of mask_error_details setting
        raise ToolError("Division by zero is not allowed.")

    # If mask_error_details=True, this message would be masked
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers.")

    return a / b


# Annotations
# あくまで補助的なヒントであり、セキュリティの境界を強制するような機能ではないことに注意
@mcp.tool(
    annotations={
        "title": "Calculate Sum",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def calculate_sum(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


# [MCP Context]
# 詳しくは別の機会に
# 引数にContextを追加すれば使えるらしい
@mcp.tool()
async def process_data(data_uri: str, ctx: Context) -> dict:
    """Process data from a resource with progress reporting."""
    await ctx.info(f"Processing data from {data_uri}")

    # Read a resource
    resource = await ctx.read_resource(data_uri)
    data = resource[0].content if resource else ""

    # Report progress
    await ctx.report_progress(progress=50, total=100)

    # Example request to the client's LLM for help
    summary = await ctx.sample(f"Summarize this in 10 words: {data[:200]}")

    await ctx.report_progress(progress=100, total=100)
    return {
        "length": len(data),
        "summary": summary.text
    }


# [Server Behavior]
# Duplicate Tools
@mcp.tool()
def my_tool(): return "Version 1"

# @mcp.tool()
# def my_tool(): return "Version 2"

# Legacy JSON Parsing
# 2.2.10以降での挙動変更の話題であり、こちらのPJで使用しているのは2.5.X系のため関係なし

if __name__ == "__main__":
    mcp.run()
