import asyncio
from pathlib import Path
import sys
from dotenv import load_dotenv
import subprocess

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from utils.aoc_client import AocClient

# Load environment variables from project root
load_dotenv(project_root / '.env')

# Initialize AOC client
client = AocClient()

server = Server("aoc")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Supports:
    - Reading puzzle text
    - Submitting answers
    - Running Python scripts
    """
    return [
        types.Tool(
            name="get-puzzle",
            description="Get the puzzle text for a specific day",
            inputSchema={
                "type": "object",
                "properties": {
                    "day": {"type": "integer", "minimum": 1, "maximum": 25},
                },
                "required": ["day"],
            },
        ),
        types.Tool(
            name="submit-answer",
            description="Submit an answer for an AOC puzzle",
            inputSchema={
                "type": "object",
                "properties": {
                    "day": {"type": "integer", "minimum": 1, "maximum": 25},
                    "part": {"type": "integer", "enum": [1, 2]},
                    "answer": {"type": "string"},
                },
                "required": ["day", "part", "answer"],
            },
        ),
        types.Tool(
            name="run-script",
            description="Run a Python script in the AOC directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the Python script, relative to /Users/rictic/open/aoc2024/",
                    },
                },
                "required": ["path"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Supports getting puzzle text, submitting answers, and running Python scripts.
    """
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "get-puzzle":
        day = arguments.get("day")
        if not day:
            raise ValueError("Missing day")

        puzzle_text = client.get_puzzle_text(day)
        return [
            types.TextContent(
                type="text",
                text=puzzle_text,
            )
        ]

    elif name == "submit-answer":
        day = arguments.get("day")
        part = arguments.get("part")
        answer = arguments.get("answer")

        if not all([day, part, answer]):
            raise ValueError("Missing day, part, or answer")

        response = client.submit_answer(day, part, answer)
        return [
            types.TextContent(
                type="text",
                text=response,
            )
        ]

    elif name == "run-script":
        script_path = arguments.get("path")
        if not script_path:
            raise ValueError("Missing path")

        # Resolve and validate the path
        aoc_root = Path("/Users/rictic/open/aoc2024")
        full_path = (aoc_root / script_path).resolve()

        # Ensure the path is within the AOC directory
        if not str(full_path).startswith(str(aoc_root)):
            raise ValueError(f"Script path must be within {aoc_root}")

        # Ensure it's a .py file
        if full_path.suffix != '.py':
            raise ValueError("Script must be a Python file")

        # Run the script using uv with full path
        try:
            result = subprocess.run(
                ["/Users/rictic/.cargo/bin/uv",
                 "--directory",
                 str(aoc_root / "mcp_server"),
                 "run",
                 str(full_path)],
                capture_output=True,
                text=True,
                check=True
            )
            return [
                types.TextContent(
                    type="text",
                    text=f"Output:\n{result.stdout}\n\nErrors:\n{result.stderr}"
                )
            ]
        except subprocess.CalledProcessError as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error running script:\nOutput:\n{e.stdout}\n\nErrors:\n{e.stderr}"
                )
            ]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="aoc",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
