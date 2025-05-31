from typing import Literal, Optional

import aiohttp
from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent
from pydantic import Field

mcp = FastMCP(name="PromptServer")

# [Prompts]
# The @prompt Decorator

# よく使うプロンプトを再利用可能にしておく
# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt()
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"

# Prompt returning a specific message type
@mcp.prompt()
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

# promptでは*argsまたは**kwargsをサポートしていないことに注意

# Return Values
# list[PromptMessage | str]は会話型向き
@mcp.prompt()
def roleplay_scenario(character: str, situation: str) -> list[Message]:
    """Sets up a roleplaying scenario with initial messages."""
    return [
        Message(f"Let's roleplay. You are {character}. The situation is: {situation}"),
        Message("Okay, I understand. I am ready. What happens next?", role="assistant")
    ]

# Type annotations
# FastMCPに期待する型を教えてバリデーションさせる
@mcp.prompt()
def generate_content_request(
        topic: str = Field(description="The main subject to cover"),
        format: Literal["blog", "email", "social"] = "blog",
        tone: str = "professional",
        word_count: Optional[int] = None
) -> str:
    """Create a request for generating content in a specific format."""
    prompt = f"Please write a {format} post about {topic} in a {tone} tone."

    if word_count:
        prompt += f" It should be approximately {word_count} words long."

    return prompt

# Prompt Metadata
# tagsはクライアントがフィルターやグルーピングするのに使うかもしれない
@mcp.prompt(
    name="analyze_data_request",          # Custom prompt name
    description="Creates a request to analyze data with specific parameters",  # Custom description
    tags={"analysis", "data"}             # Optional categorization tags
)
def data_analysis_prompt(
    data_uri: str = Field(description="The URI of the resource containing the data."),
    analysis_type: str = Field(default="summary", description="Type of analysis.")
) -> str:
    """This docstring is ignored when description is provided."""
    return f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."

# Asynchronous Prompts
# promptは非同期関数に対しても使える
@mcp.prompt()
async def data_based_prompt(data_id: str) -> str:
    """Generates a prompt based on data that needs to be fetched."""
    # In a real scenario, you might fetch data from a database or API
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/data/{data_id}") as response:
            data = await response.json()
            return f"Analyze this data: {data['content']}"
