import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

load_dotenv()

SERVER_SCRIPT = Path(__file__).resolve().parent / "server.py"


def mcp_tool_to_openai(tool):
    """Convert an MCP tool definition to OpenAI function-calling format."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema,
        },
    }


async def call_mcp_tool(session: ClientSession, name: str, arguments: dict) -> str:
    result = await session.call_tool(name, arguments)
    return "\n".join(chunk.text for chunk in result.content if chunk.type == "text")


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=[str(SERVER_SCRIPT)],
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_response = await session.list_tools()
            openai_tools = [mcp_tool_to_openai(tool) for tool in tools_response.tools]

            messages = [{"role": "user", "content": "What is the sum of 1 and 2?"}]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=openai_tools,
            )

            message = response.choices[0].message
            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    arguments = json.loads(tool_call.function.arguments)
                    tool_result = await call_mcp_tool(
                        session,
                        tool_call.function.name,
                        arguments,
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result,
                        }
                    )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=openai_tools,
                )

            print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
