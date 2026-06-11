---
name: toolbench-improve
description: Improve an Arcade MCP server against ToolBench by running the community grader CLI, reading definitionQuality and protocolReadiness gaps in the JSON output, rewriting server.py and docs, and re-scoring until the grade reaches B or code dimensions plateau. Use when ToolBench grading, MCP production readiness, or dice-mcp improvement is requested.
---

# ToolBench Self-Improvement Loop

Improve this MCP server until ToolBench's **Definition Quality** and **Protocol Readiness**
scores plateau. The community CLI is the fitness function.

## Procedure

1. **Run the grader.**
   ```bash
   cd ~/arcade-marketplace/toolbench
   npx tsx scripts/community/process-repo.ts https://github.com/thierrypdamiba/dice-mcp --force-refresh
   ```
2. **Read the output JSON** at `~/arcade-marketplace/toolbench/output/thierrypdamiba-dice-mcp.json`.
   Focus on `scores.definitionQuality.topIssues` and `scores.protocolReadiness.issues`.
3. **Fix code and docs** — typically `src/dice/server.py`, `README.md`, `pyproject.toml`:
   - One focused tool with verb-noun name and LLM-readable description
   - Typed inputs with constraints; documented output shape
   - HTTP transport (not STDIO-only) for Protocol
   - README, LICENSE, MCP compliance section
   - `ToolMetadata` / `Behavior` annotations on the tool
4. **Verify without hanging imports:** `python3 -m py_compile src/dice/server.py`
5. **Commit, push if grading remote URL, re-run grader.** Repeat until overall grade is **B (70+)**
   or Definition/Protocol stop improving.
6. **Report honestly:** overall grade, three dimension scores, what you fixed, and what remains
   (usually Supportability — stars, contributors, org — which code cannot fix quickly).

## Notes

- **B is success** for a brand-new personal repo. A requires adoption signals, not just code.
- Do not weaken the grader or fake GitHub stars. Fix the repo.
- Supportability (~38) is expected for 0-star solo repos. Say so in the report.
