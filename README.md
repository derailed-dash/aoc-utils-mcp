# The Aoc-Utils MCP Server

This repo contains an MCP server that exposes handy Advent of Code (AoC) utilities, e.g.

- The `get_puzzle_input(year: int, day: int)` retrieves your puzzle data for a given specific year and day.

It also acts as a useful example of how to implement a FastMCP server for Python functions, and explains how to integrate the MCP server into an AI tool like Gemini CLI.

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

## Installing the MCP Server into Gemini CLI

I struggled to install with either of these approaches:

```bash
# Using FastMCP CLI, which automatically calls the Gemini CLI MCP management system
# It runs gemini mcp add for you
fastmcp install gemini-cli server.py \
  --project /path/to/your/project \
  --env AOC_SESSION_COOKIE=$AOC_SESSION_COOKIE

# Using `gemini mcp add`
gemini mcp add aoc-utils-mcp \
  uv -- run --project /path/to/project --with fastmcp fastmcp run server.py \
  -e AOC_SESSION_COOKIE=$AOC_SESSION_COOKIE
```

So instead, I just create this entry in my `settings.json`, in my AoC project:

```json
{
  "mcpServers": {
    "aoc-utils-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/home/darren/localdev/python/aoc-utils-mcp/src/server.py"
      ],
      "env": {
        "AOC_SESSION_COOKIE": "${AOC_SESSION_COOKIE}"
      },
      "cwd": "/home/darren/localdev/python/aoc-utils-mcp/src"
    }
  }
}
```

Note: **You need to ensure your AOC_SESSION_COOKIE environment is set before launching Gemini CLI.**

## Appendix

### Deploying to FastMCP Cloud

We can optionally deploy the sever to FastMCP Cloud to make it publicly accessible.
Note that FastMCP Cloud automatically detects and uses `pyproject.toml`.

### Troubleshooting

#### Terminating the Background Process

If we're having trouble closing the background process...

```bash
pgrep -f "fastmcp"
kill <PID>
```