"""
A test client for calling the aoc-utils MCP server.
"""
import argparse
import asyncio

from fastmcp import Client


def main():
    """ The main function. """
    parser = argparse.ArgumentParser(description="A test client for calling the aoc-utils MCP server.")
    parser.add_argument("--port", type=int, default=8000, help="The port to connect to.")
    args = parser.parse_args()

    client = Client(f"http://localhost:{args.port}/mcp")

    async def call_tool(year: int, day: int):
        async with client:
            puzzle = await client.call_tool("get_puzzle", {"year": year, "day": day})
            print(f"Puzzle: {puzzle}")
            
            input_data = await client.call_tool("get_puzzle_input_data", {"year": year, "day": day})
            print(f"Input data: {input_data}")

    asyncio.run(call_tool(2024, 1))

if __name__ == "__main__":
    main()
