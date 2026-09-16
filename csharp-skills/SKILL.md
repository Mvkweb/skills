---
name: csharp-skills
description: >
  C# coding guidelines for modern .NET. Use when writing, reviewing, or refactoring .cs/.csproj files.
license: MIT
metadata:
  author: Mvk
  version: "0.1.0"
  sources:
    - dotnet/skills official C# skill set (MIT, dotnet org)
---

# C# Best Practices

Guidelines for writing high-quality, idiomatic C# that stays null-safe and fast at scale. Contains 12 rules across 6 categories, prioritized by impact to guide LLMs in code generation and refactoring. Current for .NET 8/10.

C# nullable reference types plus build hygiene catch bugs before runtime while staying out of the way. Out of the box, agents write *decent* C# at best: `!` to silence warnings, `Thread.Abort` instead of `CancellationToken`, missing `/bl` binlogs on failing builds, shared `Directory.Build.props` mistakes, and untestable static calls (`DateTime.Now`, `File`, `Environment`). These rules encode what careful C# looks like.

Rule bodies are verbatim excerpts from the official `dotnet/skills` set (see `<!-- source: -->` provenance in each file); only the `# id` / `> summary` header was added. This skill is pure C# and .NET — game-server API rules live in `swiftlys2-skills`, not here.

## When to Apply

Reference these guidelines when:

- Enabling nullable reference types or fixing `CS860x` warnings
- Replacing `Thread.Abort` with cooperative cancellation
- Reviewing hot paths for allocations or async mistakes
- Diagnosing a failing `dotnet build` (always capture a binlog first)
- Organizing multi-project builds with `Directory.Build.*` / CPM
- Running `dotnet test` (pick VSTest vs MTP syntax first)
- Finding untestable static dependencies and seams

## Rule Categories by Priority

<!-- gen:begin:table -->
| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Nullable Safety | CRITICAL | `null-` | 1 |
| 2 | Async & Cancellation | HIGH | `async-` | 1 |
| 3 | Performance | HIGH | `perf-` | 1 |
| 4 | Refactoring | HIGH | `refactor-` | 1 |
| 5 | Build & MSBuild | MEDIUM | `build-` | 5 |
| 6 | Testing | MEDIUM | `test-` | 3 |
<!-- gen:end:table -->

---

## Quick Reference

<!-- gen:begin:quickref -->
### 1. Nullable Safety (CRITICAL)

- [`null-nullable-references`](rules/null-nullable-references.md) - Enable nullable reference types and resolve all warnings

### 2. Async & Cancellation (HIGH)

- [`async-cooperative-cancellation`](rules/async-cooperative-cancellation.md) - Replace Thread.Abort with cooperative CancellationToken

### 3. Performance (HIGH)

- [`perf-antipattern-scan`](rules/perf-antipattern-scan.md) - Scan .NET code for performance anti-patterns with tiered severity

### 4. Refactoring (HIGH)

- [`refactor-safe-refactoring`](rules/refactor-safe-refactoring.md) - Safe behavior-preserving C# refactoring, verified by build plus tests

### 5. Build & MSBuild (MEDIUM)

- [`build-binlog-failure-analysis`](rules/build-binlog-failure-analysis.md) - Diagnose build failures from an existing .binlog file
- [`build-binlog-generation`](rules/build-binlog-generation.md) - Capture a binary log on every MSBuild-based command
- [`build-directory-organization`](rules/build-directory-organization.md) - Organize shared builds with Directory.Build.props and targets
- [`build-msbuild-antipatterns`](rules/build-msbuild-antipatterns.md) - Detect and fix MSBuild anti-patterns in project files
- [`build-property-patterns`](rules/build-property-patterns.md) - Define overridable MSBuild properties with safe patterns

### 6. Testing (MEDIUM)

- [`test-detect-static-dependencies`](rules/test-detect-static-dependencies.md) - Locate hard-to-test static APIs blocking test seams
- [`test-platform-detection`](rules/test-platform-detection.md) - Identify VSTest or MTP plus the test framework in use
- [`test-run-tests`](rules/test-run-tests.md) - Choose the repo-compatible dotnet test command and flags
<!-- gen:end:quickref -->

---

## How to Use

This skill provides rule identifiers for quick reference. When generating or reviewing C# code:

1. **Check relevant category** based on task type
2. **Apply rules** with matching prefix
3. **Prioritize** CRITICAL > HIGH > MEDIUM
4. **Read rule files** in `rules/` for detailed guidance

### Rule Application by Task

| Task | Primary Categories |
|------|-------------------|
| Nullable warnings | `null-` |
| Threading / shutdown | `async-` |
| Hot path review | `perf-` |
| Refactor | `refactor-` |
| Failing build | `build-` |
| Run tests | `test-` |

---

## Sources & Attribution

Verbatim excerpts from [dotnet/skills](https://github.com/dotnet/skills) (MIT, Microsoft/dotnet org), reorganized into one-index-plus-rules format. Upstream materials remain under their own licenses. Nothing here covers game APIs — see `swiftlys2-skills`.

## Manual install

```bash
git clone https://github.com/Mvkweb/skills.git <agent-skills-dir>/csharp-skills
```

Targets per agent:

- Claude Code (global): `~/.claude/skills/csharp-skills`
- Claude Code (one project): `.claude/skills/csharp-skills`
- OpenCode: `.opencode/skills/csharp-skills`
- Cursor: `.cursor/skills/csharp-skills`
- Codex: `.codex/skills/csharp-skills`
