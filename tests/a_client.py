"""
A test client for calling the aoc-utils MCP server.
"""
import asyncio

from fastmcp import Client

client = Client("http://localhost:9000/mcp")

async def call_tool(year: int, day: int):
    async with client:
        result = await client.call_tool("get_puzzle_input", {"year": year, "day": day})
        print(result)

asyncio.run(call_tool(2024, 1))
