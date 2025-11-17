Toy MCP server implemented with the official MCP Python SDK.

## Overview

This project implements a **toy Model Context Protocol (MCP) server** using Anthropic's official Python SDK `mcp` ([PyPI](https://pypi.org/project/mcp/), [docs.claude.com](https://docs.claude.com/en/docs/mcp)).

It exposes two tools:

- **random_animal**: returns a random animal from a predefined list of 10 animals.
- **roll_d20**: returns a random integer simulating a roll of a 20-sided die (1–20).

The server is:

- **MCP-native** – built using `FastMCP` from the official SDK, implementing tools according to the MCP spec ([docs.claude.com](https://docs.claude.com/en/docs/mcp)).
- **Stateless and simple** – suitable as a toy reference server.
- **Flexible on transport** – can be run over stdio, streamable HTTP, or SSE using the `mcp` CLI.

## Installation

From the project root:

```bash
uv sync
```

If you are not using `uv`, you can install dependencies with:

```bash
pip install -e .
```

This will install the `mcp[cli]` SDK, which provides the MCP runtime and developer tooling.

You should also have **Claude Desktop** installed if you want to register this server as a Claude MCP connector, as described in the MCP docs ([docs.claude.com](https://docs.claude.com/en/docs/mcp)).

## Running the MCP server

The recommended way to run this server is via the `mcp` CLI, which understands MCP transports and discovers the `FastMCP` instance defined in `main.py`.

### Dev mode (MCP Inspector / stdio)

From the project root:

```bash
uv run mcp dev main.py
```

This runs the server in **development mode** (stdio transport) and opens the MCP Inspector, where you can:

- Inspect the server’s declared tools.
- Manually invoke `random_animal` and `roll_d20`.

Under the hood:

- `uv run` ensures the `mcp` CLI runs inside this project’s environment (with the right `mcp` version from [PyPI](https://pypi.org/project/mcp/)).
- `mcp dev main.py` starts your server as a subprocess over **stdio** and connects an MCP Inspector client to it.

### Direct execution

You can also run the server directly (for example, to integrate with a custom MCP client over stdio or another supported transport):

```bash
python main.py
```

This calls `mcp.run()` on the `FastMCP` instance defined in `main.py`, starting an MCP server loop using the SDK’s defaults.

This is useful for:

- Custom MCP clients that you write yourself.
- Simple testing of the server process and logging without the inspector.

Note that **direct execution does not automatically register** the server with Claude Desktop; it just runs the MCP server.

## Registering the server with Claude Desktop

Once Claude Desktop is installed, you can register this MCP server so Claude can discover and launch it automatically.

From the project root, run:

```bash
uv run mcp install main.py
```

What this does conceptually:

- Inspects `main.py` to find the `FastMCP` server.
- Prompts you (if needed) for details like the **server name** and **command**.
- Writes a **small manifest/config entry** into Claude Desktop’s MCP configuration directory (a per-user config location), telling Claude:
  - “This server exists and is named e.g. `Toy MCP Server`.”
  - “To start it, run: `python <path-to-your-project>/main.py` (with the proper environment).”

Importantly:

- **Your code is not copied or reinstalled**; it stays in your project folder.
- The “install” step only creates metadata so Claude Desktop knows how to launch the existing script as an MCP server.

After running `mcp install`:

1. Restart Claude Desktop (if it was open).
2. Open its settings/preferences and navigate to the **MCP / Tools / Servers** section.
3. You should see this server listed (with the name you chose); enable it if needed.
4. Claude will now spawn the server process on demand and call the tools (`random_animal`, `roll_d20`) via MCP.

## Example tool usage (conceptual)

The MCP client (e.g. Claude Desktop, MCP Inspector, or a custom MCP client) will discover and call tools using the MCP protocol rather than raw HTTP endpoints.

- **List tools** – the client inspects the server’s declared tools (`random_animal`, `roll_d20`) via MCP’s capabilities and tool metadata, similar to the examples in the MCP docs ([docs.claude.com](https://docs.claude.com/en/docs/mcp)).
- **Call `random_animal`** – the client sends an MCP tool invocation with no arguments and receives a string result like `"tiger"`.
- **Call `roll_d20`** – the client sends an MCP tool invocation with no arguments and receives an integer result between 1 and 20.

## Integrating with a local LLM (e.g. Claude Desktop, LM Studio)

Because this server is MCP-native, the **ideal** integration path is with MCP-aware clients (e.g. Claude Desktop, Claude Code, MCP Inspector) that speak the protocol directly as described in the MCP docs ([docs.claude.com](https://docs.claude.com/en/docs/mcp)).

For **LM Studio** or other local LLM runtimes that don’t yet natively support MCP, you can:

- Run this MCP server (via stdio or HTTP/SSE using the SDK’s transports).
- Write a **thin adapter** that acts as:
  - An MCP client on one side (talking to this server via the `mcp` Python SDK).
  - A tool/callout provider on the other side (using whatever HTTP or plugin mechanism LM Studio exposes; see e.g. [this overview of LM Studio](https://www.windowscentral.com/artificial-intelligence/ditch-ollama-and-use-lm-studio-for-local-ai-if-you-have-a-laptop-or-mini-pc)).

That way you keep this project focused purely on the MCP server, while still being able to integrate it into your local LLM workflow.
