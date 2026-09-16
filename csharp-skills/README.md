# C# Skills

<!-- gen:begin:badges -->
![rules](https://img.shields.io/badge/rules-12-512BD4?style=flat-square&logo=csharp&logoColor=white)
![categories](https://img.shields.io/badge/categories-6-89b4fa?style=flat-square&logo=csharp&logoColor=white)
![C#](https://img.shields.io/badge/C%23-nullable-512BD4?style=flat-square&logo=csharp&logoColor=white)
![ci](https://github.com/Mvkweb/skills/actions/workflows/ci.yml/badge.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)
<!-- gen:end:badges -->

Pure C# and .NET guidelines for agents. No game APIs here — those live in `swiftlys2-skills`.

## Install

```bash
npx skills add Mvkweb/skills/csharp-skills
```

Or clone it into your agent's skills dir. Then: `/csharp-skills review this file`.

## What's in here

<!-- gen:begin:categories -->
12 rules split into 6 categories:

| Category | Rules | What it covers |
|----------|-------|----------------|
| **Nullable Safety** | 1 | NRT migration, zero warnings |
| **Async & Cancellation** | 1 | Cooperative CancellationToken |
| **Performance** | 1 | Anti-pattern scan, tiered fixes |
| **Refactoring** | 1 | Behavior-preserving edits |
| **Build & MSBuild** | 5 | Binlogs, props, antipatterns |
| **Testing** | 3 | Run tests, platform, seams |
<!-- gen:end:categories -->

Every rule keeps its upstream instruction text verbatim (provenance in `<!-- source: -->`).

## How it works

[`SKILL.md`](./SKILL.md) is the index. [`rules/`](./rules) holds one file per rule. Prefixes match categories. That is the whole design.

Full rule list with links: [SKILL.md](./SKILL.md).

## Sources

dotnet/skills official C# set (MIT). Reorganized, not rewritten.
