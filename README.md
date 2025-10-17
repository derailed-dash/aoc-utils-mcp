# The Aoc-Utils MCP Server and Gemini Extension

This repo contains an extension and MCP server that exposes handy Advent of Code (AoC) utilities, e.g.

- The `get_puzzle_input(year: int, day: int)` retrieves your puzzle data for a given specific year and day.

It also acts as a useful example of how to implement a FastMCP server for Python functions, and explains how to integrate the MCP server into an AI tool like Gemini CLI.

## Useful Links

- [Advent of Code](https://adventofcode.com/)
- [Dazbo's Advent of Code Walkthroughs](https://aoc.just2good.co.uk/)
- [FastMCP Quickstart](https://gofastmcp.com/getting-started/quickstart)
- [FastMCP Cloud](https://gofastmcp.com/deployment/fastmcp-cloud)
- [Gemini CLI with FastMCP](https://developers.googleblog.com/en/gemini-cli-fastmcp-simplifying-mcp-server-development/)
- [FastMCP Gemini Integration](https://gofastmcp.com/integrations/gemini-cli)
- [Dazbo's Advent of Code Solutions Repo](https://github.com/derailed-dash/advent-of-code)

## Demo from Gemini CLI

My prompt to Gemini CLI: 

_Fetch the input data for AoC 2022 day 1, and save to tmp/aoc_2022_day1_input.txt_

![Get AoC Input](/docs/media/get-aoc-input.png)

And it has saved the file!

![File Saved](/docs/media/file-saved.png)

## Development

### Running the MCP Server

#### Pre-Reqs for Local Development and Testing

Start by loading your dependencies into the virtual environment:

```bash
# Create venv and activate
uv sync
source .venv/bin/activate
```

Then retrieve your AoC session key:

This AoC MCP server is designed to retrieve your specific AoC input data. To do so, you'll need to supply your unique AoC session key. This is easy to get. Open the [Advent of Code](https://adventofcode.com/) website and ensure you are logged in. Then open developer tools in your browser (F12), open the `Application` tab, then expand Cookies and find the cookie called `session`. Copy the value against this cookie.

#### Running the Server

Now we can launch the server.

Note that the `fastmcp` CLI automatically integrates with `uv` to manage
environments and dependencies.

```bash
cd mcp-server/src

# PRE-REQ: Ensure AOC_SESSION_COOKIE is set as env var
export AOC_SESSION_COOKIE=<session key>

# View FastMCP CLI help
fastmcp 

# To launch the server with default stdio transport
fastmcp run server.py

# Or to run with HTTP transport:
fastmcp run server.py --transport http --port 9000

# Or if we just configure using the `fastmcp.json`, we don't need any parameters:
fastmcp run # If fastmcp.json is in the cwd
fastmcp run path/to/fastmcp.json
fastmcp run prod.fastmcp.json # use a specific json
```

Note that command-line arguments override the `fastmcp.json` configuration.

### Testing

We can test a few ways:

#### Unit Testing

Use the `make test` shortcut to run unit tests. These tests do not the actual MCP server.

#### Checking the Server is Healthy

If we've started the MCP server, we can check it's [healthy](http://127.0.0.1:8000/health).

#### With the Sample Client

If the MCP server is running, we can test from a separate terminal session:

```bash
# Activate the venv
uv sync
source .venv/bin/activate

# Launch a client with Python - requires server to be HTTP
python3 tests/a_client.py --port 8000
```

## Installing into Gemini CLI

### Installing as an Extension

```bash
# Install from the GitHub URL
gemini extensions install https://github.com/derailed-dash/aoc-utils-mcp
```

Note that you can enable and disable extensions at global (user) and workspace level. This is configured in `~/.gemini/extensions/extension-enablement.json`. For example, to enable this extension only in a specific workspace:

```json
{
  "adk-docs-ext": {
    "overrides": [
      "/home/darren/*"
    ]
  },
  "gcloud": {
    "overrides": [
      "/home/darren/*"
    ]
  },
  "aoc-utils": {
    "overrides": [
      "!/home/darren/*",
      "/home/darren/localdev/python/advent-of-code/*"
    ]
  }
}
```

We can see that the `aoc-utils` extension is disabled (`!`) at global level, but enabled in the `advent-of-code` workspace.

### Installing the MCP Server Only

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
        "/home/darren/localdev/python/aoc-utils-mcp/mcp-server/src/server.py"
      ],
      "env": {
        "AOC_SESSION_COOKIE": "${AOC_SESSION_COOKIE}"
      },
      "cwd": "/home/darren/localdev/python/aoc-utils-mcp/mcp-server/src"
    }
  }
}
```

Note: **You need to ensure your AOC_SESSION_COOKIE environment is set before launching Gemini CLI.**

We can check the MCP server is running in Gemini CLI:

![MCP server running](/docs/media/mcp-running-in-gemini.png)

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