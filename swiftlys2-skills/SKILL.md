---
name: swiftlys2-skills
description: >
  SwiftlyS2 CS2 server plugin guidelines. Use when planning, auditing, or editing C#/.NET SwiftlyS2 plugins: lifecycle, main-thread safety, IPlayer handles, hooks, menus, HUD, workers, config, database.
license: MIT
metadata:
  author: Mvk
  version: "0.1.0"
  sources:
    - SwiftlyS2 official docs (swiftlys2.net/docs)
    - sw2-mdwiki community wiki
    - swiftly-solution/swiftlys2 repository
---

# SwiftlyS2 Best Practices

Guidelines for building correct SwiftlyS2 CS2 server plugins. Contains 10 rules across 4 categories. Game-server API rules only — pure C# fundamentals (nullable, builds, tests) live in `csharp-skills`, not here.

SwiftlyS2 plugins run hot, on the main thread, against entities and players that can vanish mid-`await`. Out of the box, agents write *decent* plugins at best: stale `IPlayer` after delays, JSON on the tick path, `Thread.Abort` instead of cancellation, unbounded workers, unvalidated `CHandle<T>`. These rules encode what careful server code looks like: lifecycle closure, main-thread boundaries, `SessionId` relookup, tick budgets, producer/consumer separation.

Rule bodies come from the SwiftlyS2 toolkit references (see `<!-- source: -->` provenance in each file); only the `# id` / `> summary` header was added.

## Public reference allowlist

By default, reference only public sources:

1. SwiftlyS2 official documentation: `https://swiftlys2.net/docs/`
2. sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
3. SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`
4. Full-text fallback only with user approval: `https://swiftlys2.net/llms-full.txt`

Keep workspace mappings, private repos, and credentials in the nearest `AGENTS.md`, never in this skill.

## When to Apply

Reference these guidelines when:

- Planning a new plugin or module (`workflow-plan` + `playbook-plugin-playbook`)
- Auditing lifecycle, thread safety, hooks, or handles (`workflow-audit`)
- Editing plugin code directly (`workflow-edit` + closest playbook)
- Optimizing tick paths or GC pressure (`playbook-performance-playbook`)
- Finding docs or templates (`kb-index`, `kb-docs-map`, `kb-asset-inventory`)
- Building custom HUD (`hud-custom-hud`)

## Rule Categories by Priority

<!-- gen:begin:table -->
| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Playbooks | HIGH | `playbook-` | 2 |
| 2 | Workflows | HIGH | `workflow-` | 3 |
| 3 | Knowledge Index | MEDIUM | `kb-` | 4 |
| 4 | Custom HUD | MEDIUM | `hud-` | 1 |
<!-- gen:end:table -->

---

## Quick Reference

<!-- gen:begin:quickref -->
### 1. Playbooks (HIGH)

- [`playbook-performance-playbook`](rules/playbook-performance-playbook.md) - Classify hotspots first, then apply tick-budget optimizations
- [`playbook-plugin-playbook`](rules/playbook-plugin-playbook.md) - SwiftlyS2 plugin architecture, lifecycle, thread and state rules

### 2. Workflows (HIGH)

- [`workflow-audit`](rules/workflow-audit.md) - Audit for lifecycle, thread, hook, and handle risks with evidence
- [`workflow-edit`](rules/workflow-edit.md) - Smallest correct edit with validation and delivery notes
- [`workflow-plan`](rules/workflow-plan.md) - Plan first: classification, method plan, regression matrix

### 3. Knowledge Index (MEDIUM)

- [`kb-asset-inventory`](rules/kb-asset-inventory.md) - Catalog of templates, checklists, and guides in assets
- [`kb-capability-map`](rules/kb-capability-map.md) - Snapshot of documented SDK surface and drift warnings
- [`kb-docs-map`](rules/kb-docs-map.md) - Lean navigation map for the official SwiftlyS2 docs
- [`kb-index`](rules/kb-index.md) - Index of official docs, wiki, repo, and toolkit entry points

### 4. Custom HUD (MEDIUM)

- [`hud-custom-hud`](rules/hud-custom-hud.md) - Custom HUD layout, dialog vars, and input capture rules
<!-- gen:end:quickref -->

---

## How to Use

1. **Check relevant category** based on task type
2. **Apply rules** with matching prefix
3. **Prioritize** HIGH > MEDIUM
4. **Read rule files** in `rules/` for detailed guidance

### Rule Application by Task

| Task | Primary Categories |
|------|-------------------|
| New plugin / module | `playbook-`, `workflow-` |
| Risk audit | `workflow-`, `playbook-` |
| Hot path optimization | `playbook-` |
| Find docs / templates | `kb-` |
| Custom HUD | `hud-` |

### Task routing

- **Plan:** `playbook-plugin-playbook` → `workflow-plan`
- **Audit:** `playbook-plugin-playbook` (+ `playbook-performance-playbook` for hot paths) → `workflow-audit`
- **Edit:** `workflow-edit` + closest subsystem rule
- **Lookup:** `kb-index` → `kb-docs-map` → `kb-asset-inventory` → `kb-capability-map`

## Failure-mode-first rules

Prefer rules that map to concrete failure modes over abstract virtues:

- Do not claim validation without direct evidence.
- Do not treat a successful build as proof of player-visible behavior.
- Do not add bridge/helper layers unless reuse, lifecycle isolation, or boundary clarity clearly requires them.

## Verification quality bar

- Prefer evidence-backed verification over narrative confidence.
- Distinguish `PASS`, `FAIL`, `PARTIAL` in audits and delivery notes.
- `PARTIAL` only for objective environment limits, never for uncertainty.
- For lifecycle / hook / runtime work, add at least one adversarial or regression check beyond build success.

## Sources & Attribution

Synthesized from official SwiftlyS2 docs, the community wiki, and the official repository. Not affiliated with or endorsed by Swiftly. Upstream materials remain under their own licenses.

## Manual install

```bash
git clone https://github.com/Mvkweb/skills.git <agent-skills-dir>/swiftlys2-skills
```

Targets per agent:

- Claude Code (global): `~/.claude/skills/swiftlys2-skills`
- Claude Code (one project): `.claude/skills/swiftlys2-skills`
- OpenCode: `.opencode/skills/swiftlys2-skills`
- Cursor: `.cursor/skills/swiftlys2-skills`
- Codex: `.codex/skills/swiftlys2-skills`
