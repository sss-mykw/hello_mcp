import asyncio
import uuid
from enum import Enum
from pathlib import Path
from typing import Literal, Annotated

import aiohttp
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from pydantic import Field, BaseModel

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


# [Parameter Types]
# FastMCP generally supports all types that Pydantic supports as fields, including all Pydantic custom types.
# This means you can use any type that can be validated and parsed by Pydantic in your tool parameters.
# 引数に対して型の強制変換が働くので、intを期待してたのにstringで来た場合はintに変換してくれる。
# ただし、強制変換が出来ない場合はバリデーションエラーを返すことに注意

# コレクション
@mcp.tool()
def analyze_data(
    values: list[float],           # List of numbers
    properties: dict[str, str],    # Dictionary with string keys and values
    unique_ids: set[int],          # Set of unique integers
    coordinates: tuple[float, float],  # Tuple with fixed structure
    mixed_data: dict[str, list[int]] # Nested collections
):
    """Analyze collections of data."""
    # Implementation...

# Constrained Types
# Literals
# 選択肢以外の入力がされた場合はバリデーションエラーになる
@mcp.tool()
def sort_data(
    data: list[float],
    order: Literal["ascending", "descending"] = "ascending",
    algorithm: Literal["quicksort", "mergesort", "heapsort"] = "quicksort"
):
    """Sort data using specific options."""
    # Implementation...

# Enums
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# クライアントはEnumのvalueを指定しないといけないが、この際に大文字・小文字は正確に指定する必要がある。
# REDを指定する場合は、"red"が正しく、"RED"は間違いである
@mcp.tool()
def process_image(
    image_path: str,
    color_filter: Color = Color.RED
):
    """Process an image with a color filter."""
    # Implementation...
    # color_filter will be a Color enum member

# Paths
# When a client sends a string path, FastMCP automatically converts it to a Path object.
@mcp.tool()
def process_file(path: Path) -> str:
    """Process a file at the given path."""
    assert isinstance(path, Path)  # Path is properly converted
    return f"Processing file at {path}"

# UUIDs
# クライアントがString型でUUIDの文字列 (e.g., “123e4567-e89b-12d3-a456-426614174000”)を受け取った場合
# FastMCPは自動的にUUID型に変換してくれる。
@mcp.tool()
def process_item(
    item_id: uuid.UUID  # String UUID or UUID object
) -> str:
    """Process an item with the given UUID."""
    assert isinstance(item_id, uuid.UUID)  # Properly converted to UUID
    return f"Processing item {item_id}"

# Pydantic Models
class User(BaseModel):
    username: str
    email: str = Field(description="User's email address")
    age: int | None = None
    is_active: bool = True

"""
Pydanticを利用すると
・複雑な入力に対して明確で自己文書化された構造を提供
・データのバリデーション（検証）機能が標準で搭載されている
・LLM（大規模言語モデル）向けに詳細なJSONスキーマを自動生成できる
・dictやJSON入力から自動的にモデルへ変換される

またクライアントはPydanticモデルのパラメータに対して、以下の形式でデータを提供できます：
・JSONオブジェクト（文字列形式）
・適切な構造を持った辞書（dictionary）
"""
@mcp.tool()
def create_user(user: User):
    """Create a new user in the system."""
    # The input is automatically validated against the User model
    # Even if provided as a JSON string or dict
    # Implementation...

# Pydantic Fields
@mcp.tool()
def analyze_metrics(
    # Numbers with range constraints
    count: Annotated[int, Field(ge=0, le=100)],  # 0 <= count <= 100
    ratio: Annotated[float, Field(gt=0, lt=1.0)],  # 0 < ratio < 1.0
    # String with pattern and length constraints
    user_id: Annotated[str, Field(
        pattern=r"^[A-Z]{2}\d{4}$",  # Must match regex pattern
        description="User ID in format XX0000"
    )],
    # String with length constraints
    comment: Annotated[str, Field(min_length=3, max_length=500)] = "",
    # Numeric constraints
    factor: Annotated[int, Field(multiple_of=5)] = 10,  # Must be multiple of 5（5の倍数でなければならない）
):
    """Analyze metrics with validated parameters."""
    # Implementation...

@mcp.tool()
def validate_data(
    # Value constraints
    age: int = Field(ge=0, lt=120),  # 0 <= age < 120
    # String constraints
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"),  # Email pattern
    # Collection constraints
    tags: list[str] = Field(min_length=1, max_length=10)  # 1-10 tags
):
    """Process data with field validations."""
    # Implementation...


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
