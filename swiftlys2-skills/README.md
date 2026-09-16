# SwiftlyS2 Skills

<!-- gen:begin:badges -->
![rules](https://img.shields.io/badge/rules-10-E8930C?style=flat-square&logo=counterstrike&logoColor=white)
![categories](https://img.shields.io/badge/categories-4-89b4fa?style=flat-square&logo=counterstrike&logoColor=white)
![SwiftlyS2](https://img.shields.io/badge/SwiftlyS2-CS2-E8930C?style=flat-square&logo=counterstrike&logoColor=white)
![ci](https://github.com/Mvkweb/skills/actions/workflows/ci.yml/badge.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)
<!-- gen:end:badges -->

CS2 server plugin guidelines for agents. Game APIs only — pure C# lives in `csharp-skills`.

## Install

```bash
npx skills add Mvkweb/skills/swiftlys2-skills
```

Or clone it into your agent's skills dir. Then: `/swiftlys2-skills plan a warmup plugin`.

For C# fundamentals (nullable, builds, tests), also install `csharp-skills`.

## What's in here

<!-- gen:begin:categories -->
10 rules split into 4 categories:

| Category | Rules | What it covers |
|----------|-------|----------------|
| **Playbooks** | 2 | Architecture, lifecycle, perf |
| **Workflows** | 3 | Plan, audit, edit |
| **Knowledge Index** | 4 | Docs map, assets, surface |
| **Custom HUD** | 1 | Layout, dialog, input |
<!-- gen:end:categories -->

Every rule keeps its toolkit reference text (provenance in `<!-- source: -->`).

## How it works

[`SKILL.md`](./SKILL.md) is the index. [`rules/`](./rules) holds one file per rule. Prefixes match categories. That is the whole design.

Full rule list with links: [SKILL.md](./SKILL.md).

## Sources

SwiftlyS2 official docs, sw2-mdwiki, official repository. Reorganized, not rewritten.
