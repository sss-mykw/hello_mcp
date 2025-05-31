import asyncio
from fastmcp import FastMCP

mcp = FastMCP(
    # 名前を付けることでクライアント側やログからサーバーを特定するのに役立つ
    name="HelpfulAssistant",
    # 引数instructionsではサーバーとのやり取り方法についての指示を指定出来る
    instructions="""
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
        """
)

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"


# [Components]

# Resource Templates
@mcp.prompt()
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"

# Prompts
""""LLMに渡したいデータをクライアントから引数で受け取る"""
@mcp.prompt()
def analyze_data(data_points: list[float]) -> str:
    """Creates a prompt asking for analysis of numerical data."""
    formatted_data = ", ".join(str(point) for point in data_points)
    return f"Please analyze these data points: {formatted_data}"


# [Composing Servers]
# Composing Serversで勉強するのでスキップ


# [Proxying Servers]
# Proxying Serversで勉強するのでスキップ


if __name__ == "__main__":
    # トランスポートの選択はSTDIOまたはStreamable HTTPがおすすめ（SSEは非推奨らしい）
    # This runs the server, defaulting to STDIO transport
    mcp.run()

    # To use a different transport, e.g., HTTP:
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
