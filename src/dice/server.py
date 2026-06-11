"""dice MCP server — roll dice with uniform, independent results."""

import logging
import random
from typing import Annotated

from arcade_core.errors import ErrorKind, ToolRuntimeError
from arcade_mcp_server import MCPApp
from arcade_mcp_server.metadata import Behavior, Operation, ToolMetadata
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

app = MCPApp(name="dice", version="1.0.0")


class RollResult(BaseModel):
    """Structured result for a dice roll."""

    rolls: list[int] = Field(
        description="One result per die, length equals count, each value in 1..sides.",
    )
    total: int = Field(description="Sum of all rolls.")
    count: int = Field(description="Number of dice rolled.")
    sides: int = Field(description="Number of sides on each die.")


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
) -> RollResult:
    """Roll `count` dice that each have `sides` sides and return every roll plus the total.

    Use this whenever a user wants to roll dice, resolve a tabletop roll such as
    "3d6" or "roll two d20", or draw uniform random integers in a fixed range. Each
    die is independent and uniformly distributed over 1..sides (inclusive).

    Args:
        count: Number of dice to roll (1-100).
        sides: Number of faces on each die (2-1000).

    Returns:
        RollResult with rolls, total, count, and sides echo fields.

    Example:
        roll_dice(count=3, sides=6)
        -> {"rolls": [4, 2, 6], "total": 12, "count": 3, "sides": 6}

    Raises:
        ToolRuntimeError: if `count` or `sides` are outside the allowed bounds.
    """
    if not 1 <= count <= 100:
        raise ToolRuntimeError(
            message=f"count must be between 1 and 100, got {count}",
            kind=ErrorKind.TOOL_RUNTIME_BAD_INPUT_VALUE,
            extra={"parameter": "count", "min": 1, "max": 100, "actual": count},
        )
    if not 2 <= sides <= 1000:
        raise ToolRuntimeError(
            message=f"sides must be between 2 and 1000, got {sides}",
            kind=ErrorKind.TOOL_RUNTIME_BAD_INPUT_VALUE,
            extra={"parameter": "sides", "min": 2, "max": 1000, "actual": sides},
        )

    logger.info("roll_dice count=%s sides=%s", count, sides)
    rolls = [random.randint(1, sides) for _ in range(count)]
    result = RollResult(rolls=rolls, total=sum(rolls), count=count, sides=sides)
    logger.debug("roll_dice result=%s", result.model_dump())
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(transport="http", host="0.0.0.0", port=8000)
