"""
This module implements a simple tool server using FastMCP.

The server exposes a single tool, `get_puzzle_input`, which allows a client
to fetch puzzle inputs from the Advent of Code website.

FastMCP is used to quickly and easily create a web server that conforms to
the MCP specification, allowing it to be discoverable and usable by other systems, 
such as Large Language Model-based agents.
"""
import logging
import os

import requests
from fastapi import HTTPException
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

mcp = FastMCP(name="aoc-utils",
              instructions="""
                  This MCP server provides utilities for working with Advent of Code.
                  Call get_puzzle_input(year, day) to fetch the puzzle input for a given year and day.
              """,
)

logging.basicConfig(level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool # registers this function as a tool
async def get_puzzle_input(year: int, day: int) -> dict:
    """ Fetches AoC puzzle input for a given year and day.

    Args:
        year: int
        day: int

    Returns:
        dict: {"result": str, "content": str}
    """
    logger.info(f"Fetching puzzle input for {year}-{day}")
    
    if not year or not day:
        raise ValueError("'year' and 'day' are required.")

    session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if not session_cookie:
        raise HTTPException(
            status_code=500, detail="AOC_SESSION_COOKIE secret is not set."
        )

    url = f"https://adventofcode.com/{int(year)}/day/{int(day)}/input"
    cookies = {"session": session_cookie}

    try:
        response = requests.get(url, cookies=cookies, timeout=5)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        
        # The tool's result must be JSON serializable.
        # We return the content to be used by another tool like write_file.
        logger.info(f"Response={response.text}")
        
        return {"result": "success", "content": response.text.strip()}

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Puzzle input for {year}-12-{day} not found. Is it released yet?"
            ) from e
        else:
            raise HTTPException(
                status_code=e.response.status_code, detail=f"HTTP Error: {e}"
            ) from e
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}") from e

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request | None = None):
    """ Check MCP server health.
    E.g. http://127.0.0.1:8000/health 
    """
    return JSONResponse({"status": "healthy", "service": "mcp-server"})

# To ensure the server only starts when the script is executed directly,
# and not when imported as a module
# When we launch using FastMCP CLI, this entrypoint is ignored, e.g.
# fastmcp run server.py:mcp --transport http --port 8000
if __name__ == "__main__":
    # mcp.run() # Run the server with STDIO transport - recommended for local dev
    mcp.run(transport="http", host="0.0.0.0", port=8000) # http://localhost:8000/mcp/
