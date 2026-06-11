# dice

A minimal, well-typed **dice-rolling MCP server**. One tool, `roll_dice`, that an AI
agent can call to roll any number of dice with any number of sides and get back every
roll plus the total. Built on [Arcade](https://arcade.dev)'s `arcade-mcp-server`.

## Install

```bash
uv sync          # or: pip install -e .
```

## Run

Streamable HTTP (primary — remotely reachable, fully MCP-compliant):

```bash
uv run src/dice/server.py            # serves on http://0.0.0.0:8000
```

stdio (local CLI testing):

```bash
uv run src/dice/server.py stdio
```

## Connect an MCP client

```json
{
  "mcpServers": {
    "dice": { "type": "http", "url": "http://localhost:8000" }
  }
}
```

## Tool: `roll_dice`

Roll `count` dice that each have `sides` sides; returns every roll and the total.

| Parameter | Type | Constraint | Example |
|---|---|---|---|
| `count` | int | 1–100 | `3` |
| `sides` | int | 2–1000 | `6` (d6), `20` (d20) |

**Returns**

```json
{ "rolls": [4, 2, 6], "total": 12, "count": 3, "sides": 6 }
```

- `rolls` — one result per die, length `count`, each value in `1..sides`
- `total` — sum of `rolls`
- `count`, `sides` — echo the inputs used

**Example**

```python
roll_dice(count=3, sides=6)
# -> {"rolls": [4, 2, 6], "total": 12, "count": 3, "sides": 6}
```

Out-of-range inputs raise a `ValueError` with a clear message (e.g. `count` must be 1–100).

## MCP compliance

`dice` is a standard MCP server built on `arcade-mcp-server`. It exposes the **Tools**
capability over **Streamable HTTP**, follows MCP `initialize` / `tools/list` / `tools/call`
semantics, and annotates `roll_dice` with behavior hints (read-only, non-destructive,
non-idempotent — each roll is random). A Tools-only server is fully MCP-compliant per the
specification.

## Support

Please open a GitHub issue on this repository for bugs or feature requests.

## License

[MIT](./LICENSE)
