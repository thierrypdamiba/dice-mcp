"""dice MCP server — roll dice with uniform, independent results."""

import random
from typing import Annotated

from arcade_mcp_server import MCPApp
from arcade_mcp_server.metadata import Behavior, Operation, ToolMetadata

app = MCPApp(name="dice", version="1.0.0")


@app.tool(
    metadata=ToolMetadata(
        behavior=Behavior(
            operations=[Operation.READ],
            read_only=True,
            destructive=False,
            idempotent=False,
            open_world=False,
        ),
    ),
)
def roll_dice(
    count: Annotated[
        int,
        "How many dice to roll. Integer from 1 to 100. Example: 3 rolls three dice.",
    ],
    sides: Annotated[
        int,
        "Number of sides on each die. Integer from 2 to 1000. "
        "Example: 6 for a standard d6, 20 for a d20.",
    ],
) -> dict:
    """Roll `count` dice that each have `sides` sides and return every roll plus the total.

    Use this whenever a user wants to roll dice, resolve a tabletop roll such as
    "3d6" or "roll two d20", or draw uniform random integers in a fixed range. Each
    die is independent and uniform over 1..sides.

    Args:
        count: Number of dice to roll (1-100).
        sides: Number of faces on each die (2-1000).

    Returns:
        A JSON object:
            {
              "rolls": list[int],  # one result per die, length == count, each in 1..sides
              "total": int,        # sum of all rolls
              "count": int,        # the count that was used
              "sides": int         # the sides that was used
            }

    Example:
        roll_dice(count=3, sides=6)
        -> {"rolls": [4, 2, 6], "total": 12, "count": 3, "sides": 6}

    Raises:
        ValueError: if `count` is not in 1..100 or `sides` is not in 2..1000.
    """
    if not 1 <= count <= 100:
        raise ValueError(f"count must be between 1 and 100, got {count}")
    if not 2 <= sides <= 1000:
        raise ValueError(f"sides must be between 2 and 1000, got {sides}")

    rolls = [random.randint(1, sides) for _ in range(count)]
    return {"rolls": rolls, "total": sum(rolls), "count": count, "sides": sides}


if __name__ == "__main__":
    # Streamable HTTP is the primary transport: remotely reachable by hosted MCP
    # clients and fully protocol-compliant. Use stdio only for local CLI testing.
    app.run(transport="http", host="0.0.0.0", port=8000)
