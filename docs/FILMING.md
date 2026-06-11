# Filming run-of-show — ToolBench (Piece 2)

**Repo:** [thierrypdamiba/dice-mcp](https://github.com/thierrypdamiba/dice-mcp)  
**Target length:** ~5 min  
**Arc:** Untouched scaffold **F → B**. Code maxed; Support is adoption.

---

## Pre-flight

```bash
cd ~/dice-mcp-build/dice
git fetch --tags
git checkout baseline/scaffold          # untouched arcade new dice

# ToolBench community CLI (requires .env with ANTHROPIC_API_KEY, GITHUB_TOKEN)
cd ~/arcade-marketplace/toolbench
grep -E 'ANTHROPIC|GITHUB' .env
```

For a live GitHub grade during filming, push the scaffold state to a filming branch first, or use `--force-refresh` against a branch URL.

---

## Beat 1 — The scaffold (~35s)

```bash
cd ~/dice-mcp-build/dice
cat src/dice/server.py
```

**Talk track:** "This is what `arcade new dice` gives you — placeholder tools, secrets demo, STDIO. Nothing deliberately broken. It just isn't production-shaped."

```bash
ls -la README.md LICENSE 2>/dev/null || echo "no README/LICENSE yet"
```

---

## Beat 2 — The red baseline (~45s)

**Option A — community CLI (recommended for filming):**

```bash
cd ~/arcade-marketplace/toolbench
npx tsx scripts/community/process-repo.ts https://github.com/thierrypdamiba/dice-mcp --force-refresh
```

**Expected (scaffold):** Grade **D (~50)** or **F (~36 official)** — weak Definition, low Support.

**Talk track:** "ToolBench scores three things: Definition Quality, Protocol Readiness, and Supportability. This scaffold fails on all three — vague tools, no docs, no adoption signals."

**Option B — official site:** show [toolbench.arcade.dev](https://toolbench.arcade.dev) entry for the scaffold submission if you have one cached.

---

## Beat 3 — Fable 5 runs the loop (~2 min)

```bash
cd ~/dice-mcp-build/dice
claude --model claude-fable-5
```

**Prompt:**

```
This repo is an Arcade MCP server scored by ToolBench. Run the community grader:
  cd ~/arcade-marketplace/toolbench && npx tsx scripts/community/process-repo.ts https://github.com/thierrypdamiba/dice-mcp --force-refresh
Read the JSON output in toolbench/output/thierrypdamiba-dice-mcp.json — focus on
definitionQuality and protocolReadiness topIssues. Improve src/dice/server.py,
README.md, and pyproject.toml until Definition and Protocol are as high as possible.
Re-run the grader after each round. Don't ask — keep iterating until the overall
grade reaches B or the code dimensions stop improving.
```

**Narrate as it works:**

1. Reads grader JSON — names top issues (empty schemas, no README, STDIO)
2. Replaces scaffold tools with `roll_dice(count, sides)`
3. Adds README, LICENSE, HTTP transport
4. Adds behavior metadata on the tool
5. Re-runs grader — grade climbs

---

## Beat 4 — B (~30s)

```bash
cd ~/arcade-marketplace/toolbench
npx tsx scripts/community/process-repo.ts https://github.com/thierrypdamiba/dice-mcp --force-refresh
```

**Expected (improved):**

```
Grade: B (74-75/100)
  Definition Quality: 89-92/100
  Protocol Readiness: 90-95/100
  Supportability: 38/100
```

**Talk track:** "F to B in one pass. Definition and Protocol are essentially topped out for a minimal dice server. Supportability is 38 — zero stars, solo repo, created today. ToolBench doesn't just grade code. It asks whether you'd bet on this in production. The agent maxed what it could write. The rest is community."

---

## Outro (~20s)

> "Same loop as Piece 1 — read the grader, rewrite, re-run. Arcade eval tests whether a model calls your tool correctly. ToolBench tests whether you'd ship the server. F to B. That's the honest outcome — and it's the point."

---

## Reset between takes

```bash
cd ~/dice-mcp-build/dice
./scripts/rehearse-reset.sh scaffold    # back to F/D baseline
./scripts/rehearse-reset.sh improved    # jump to reference B state
```

---

## Tags

| Tag | Commit | Use |
|---|---|---|
| `baseline/scaffold` | Initial `arcade new dice` | Film Beat 1–2 |
| `improved/b` | Best B pass (~75) | Reference / Beat 4 if not live-looping |

---

## DO / DON'T

| DO | DON'T |
|---|---|
| "F → B — code maxed" | "We got an A" |
| "ToolBench is thorough — code + protocol + adoption" | "ToolBench is unfair" |
| "Supportability is stars and org backing" | "The loop failed" |
| Name Arcade as the grader | Over-index on Fable 5 hype |
