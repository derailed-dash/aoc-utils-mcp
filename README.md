# The Aoc-Utils MCP Server

Exposes Advent of Code (AoC) utilities as an MCP server, e.g.

- The `get_puzzle_input(year: int, day: int)` retrieves your puzzle data for a given specific year and day.

This is a useful example of how to implement a FastMCP server for Python functions.

## Useful Links

- [Dazbo's Advent of Code Walkthroughs](https://aoc.just2good.co.uk/)
- [FastMCP Quickstart](https://gofastmcp.com/getting-started/quickstart)
- [FastMCP Cloud](https://gofastmcp.com/deployment/fastmcp-cloud)
- [Gemini CLI with FastMCP](https://developers.googleblog.com/en/gemini-cli-fastmcp-simplifying-mcp-server-development/)
- [FastMCP Gemini Integration](https://gofastmcp.com/integrations/gemini-cli)
- [Dazbo's Advent of Code Solutions Repo](https://github.com/derailed-dash/advent-of-code)

## Running the MCP Server

Pre-reqs for development and running locally:

```bash
# Create venv and activate
uv sync
source .venv/bin/activate
```

Then launch the server.

Note that the `fastmcp` CLI automatically integrates with `uv` to manage
environments and dependencies.

```bash
cd src

# PRE-REQ: Ensure AOC_SESSION_COOKIE is set as env var
export AOC_SESSION_COOKIE=<session key>

# To launch the server with default stdio transport
fastmcp run my_server.py

# Or to run with HTTP transport:
fastmcp run server.py --transport http --port 9000

# Or if we just configure using the `fastmcp.json`, we don't need any parameters:
fastmcp run # If fastmcp.json is in the cwd
fastmcp run path/to/fastmcp.json
fastmcp run prod.fastmcp.json # use a specific json
```

Note that command-line arguments override the `fastmcp.json` configuration.

## Testing

We can test two ways:

### Unit Testing

Use the `make test` shortcut.

### With the Sample Client

Run a separate terminal session, and from there:

```bash
# Activate the venv
source .venv/bin/activate

# Launch a client with Python - requires server to be HTTP
python3 tests/a_client.py 
```

## Deploying to FastMCP Cloud

We can optionally deploy the sever to FastMCP Cloud to make it publicly accessible.
Note that FastMCP Cloud automatically detects and uses `pyproject.toml`.

## Installing the MCP Server into Gemini CLI

```bash
# Using FastMCP CLI, which automatically calls the Gemini CLI MCP management system
# It runs gemini mcp add for you
fastmcp install gemini-cli server.py \
  --project /path/to/your/project \
  --env AOC_SESSION_COOKIE=$AOC_SESSION_COOKIE

# Dependency handling:
# Add --with uvicorn --with requests
# OR
# Add --with-requirements requirements.txt
# OR use fastmcp.json

# OR add it as an MCP server without the integration
gemini mcp add aoc-utils-mcp \
  uv -- run --project /path/to/project --with fastmcp fastmcp run server.py \
  -e AOC_SESSION_COOKIE=$AOC_SESSION_COOKIE
```