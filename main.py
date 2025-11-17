import logging
import random

from mcp.server.fastmcp import FastMCP

from logging_config import setup_logger


"""
Toy MCP server implemented with the official MCP Python SDK.

This focuses purely on the MCP server (no extra web framework) and
defines two tools:

- random_animal: select a random animal from a predefined list of 10 animals
- roll_d20: roll a 20-sided dice and return the result

You can run it in different modes using the `mcp` CLI, for example:

- stdio (for Claude Desktop / other MCP-native clients)
- streamable HTTP / SSE transports (for localhost HTTP integration)

See the MCP SDK docs and quickstart on PyPI for details:
https://pypi.org/project/mcp/
"""


ANIMALS: list[str] = [
    "cat",
    "dog",
    "elephant",
    "giraffe",
    "lion",
    "tiger",
    "panda",
    "kangaroo",
    "dolphin",
    "eagle",
]


# Set up logging for the entire process
setup_logger()
logger = logging.getLogger(__name__)


# Create the FastMCP server instance
mcp = FastMCP("Toy MCP Server")


@mcp.tool()
def random_animal() -> str:
    """
    Select a random animal from a predefined list of 10 animals.

    Returns the animal name as a string.
    """
    animal = random.choice(ANIMALS)
    logger.info("Tool random_animal called -> %s", animal)
    return animal


@mcp.tool()
def roll_d20() -> int:
    """
    Roll a 20-sided dice.

    Returns an integer between 1 and 20 (inclusive).
    """
    roll = random.randint(1, 20)
    logger.info("Tool roll_d20 called -> %d", roll)
    return roll


if __name__ == "__main__":
    # For local development you typically use the `mcp` CLI, e.g.:
    #   uv run mcp dev main.py
    #
    # Direct execution is also supported via FastMCP.run(),
    # which will start an appropriate MCP server loop.
    logger.info("Starting Toy MCP Server via direct execution (python main.py)")
    mcp.run()
