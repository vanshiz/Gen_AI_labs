"""Exercise 5: a tiny MCP server (stdio transport).
Setup: pip install "mcp[cli]"
Test:  npx @modelcontextprotocol/inspector python exercises/05_mcp_server.py
Use:   claude mcp add notes -- python exercises/05_mcp_server.py
TODO: add a resource (notes://all), a prompt template, then wrap a real API.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")
NOTES: list[str] = []


@mcp.tool()
def add_note(text: str) -> str:
    """Save a note and return its index."""
    NOTES.append(text)
    return f"Saved as note #{len(NOTES) - 1}"


@mcp.tool()
def list_notes() -> list[str]:
    """List all saved notes."""
    return NOTES


if __name__ == "__main__":
    mcp.run()  # stdio: never print() to stdout here, it corrupts the protocol
