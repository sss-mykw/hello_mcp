import time

import yaml
from fastmcp import FastMCP

# Define a custom serializer that formats dictionaries as YAML
def yaml_serializer(data):
    # もしシリアライザー関数内で例外が起きた場合、デフォルトのjson形式で返却される
    return yaml.dump(data, sort_keys=False)

# これらの設定はFASTMCP_SERVER_というプレフィクスが付いた環境変数や.envファイルから読み込む事も出来るらしい
mcp = FastMCP(
    # 名前を付けることでクライアント側やログからサーバーを特定するのに役立つ
    name="HelpfulAssistant",
    # 引数instructionsではサーバーとのやり取り方法についての指示を指定出来る
    instructions="""
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
        """,
    # String型以外の返り値に適用される。String型は適用されずにそのまま返却される。
    tool_serializer=yaml_serializer
)

@mcp.tool()
def greet(name: str, duration_time_second: float) -> str:
    time.sleep(duration_time_second)
    return f"Hello, {name}!"

@mcp.tool()
def divide(a:int, b:int) -> float:
    return a / b

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
    # ターミナルでの実行コマンド「fastmcp run my_server.py --transport streamable-http --port 8000」
    # pythonではなくfastmcp runを用いて動かすと__main__が実行されないことに注意
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/my-custom-path")

    # [Server Configuration]
    # Settings are accessible via mcp.settings
    print(mcp.settings.port)  # Output: 8080
    print(mcp.settings.on_duplicate_tools)  # Output: "error"
