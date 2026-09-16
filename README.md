# Agent Skills

<!-- gen:begin:badges -->
![rules](https://img.shields.io/badge/rules-63-3178C6?style=flat-square&logo=typescript&logoColor=white)
![categories](https://img.shields.io/badge/categories-19-89b4fa?style=flat-square&logo=typescript&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?style=flat-square&logo=typescript&logoColor=white)
![ci](https://github.com/Mvkweb/skills/actions/workflows/ci.yml/badge.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)
<!-- gen:end:badges -->

Agents writes good code nowadays but doesn't follow how i usually want. This repo holds patterns against exactly that. Each skill is small rules with a reason, a bad example, a good example, and links onward. The agent reads the index, opens the rules that fit the code, and follows them.

<!-- gen:begin:total -->
85 rules across 3 skills. Each skill has its own index: open its `SKILL.md`.
<!-- gen:end:total -->

## Skills in this repo

<!-- gen:begin:skills -->
| Skill | Rules | Categories | What it covers |
|-------|-------|------------|----------------|
| [typescript-skills](./SKILL.md) | 63 | 19 | Strict TypeScript, TS 7-ready |
| [csharp-skills](./csharp-skills/SKILL.md) | 12 | 6 | Nullable C#, builds, tests |
| [swiftlys2-skills](./swiftlys2-skills/SKILL.md) | 10 | 4 | CS2 server plugins (game APIs) |
<!-- gen:end:skills -->

- **typescript-skills** (this root). Strict TypeScript that stays type-safe at scale. The backbone for anything `.ts/.tsx`. Full table below.
- **[csharp-skills](./csharp-skills/README.md)**. Nullable C#, safe refactoring, cooperative cancellation, build hygiene with binlogs, test discipline. No game APIs.
- **[swiftlys2-skills](./swiftlys2-skills/README.md)**. CS2 server plugin rules: lifecycle closure, main-thread boundaries, `IPlayer`/`SessionId` handling, tick budgets, plan/audit/edit workflows. Game APIs only, pure C# lives in `csharp-skills`.

## Install

A `SKILL.md` at the repo root shadows nested skills, so install each by path:

```bash
npx skills add Mvkweb/skills                    # typescript-skills (repo root)
npx skills add Mvkweb/skills/csharp-skills      # csharp-skills
npx skills add Mvkweb/skills/swiftlys2-skills   # swiftlys2-skills
```

Scope and targets:

```bash
npx skills add Mvkweb/skills/csharp-skills -a opencode   # into the project in your current directory
npx skills add Mvkweb/skills/csharp-skills -g -a opencode # global, available in every project
npx skills list                                          # verify what landed where
```

Project installs land in `./.agents/skills/<name>/`. Global installs land in the agent native dir (`~/.config/opencode/skills/` for OpenCode). OpenCode reads `.opencode/skills`, `.agents/skills`, and `.claude/skills`, so no extra config is needed either way.

## Example

```ts
// before
function firstWord(s: any) {
  return s.split(" ")[0]!;
}
```

```ts
// after — any-no-explicit-any, null-no-non-null-assertion, fn-return-type-branches
function firstWord(s: string): string | undefined {
  return s.split(" ")[0];
}
```

## TypeScript skill contents

<!-- gen:begin:categories -->
63 rules split into 19 categories:

| Category | Rules | What it covers |
|----------|-------|----------------|
| **Any & Unknown Safety** | 4 | Ban any, narrow unknown |
| **Null & Undefined Safety** | 4 | Strict nulls, no ! |
| **Narrowing & Type Guards** | 6 | Unions, guards, schemas first |
| **Type Design & Domain Modeling** | 8 | Valid states, brands, derives |
| **Generics & Inference** | 4 | Minimal params, conditionals |
| **Functions & Signatures** | 4 | Return types, object args |
| **Error Handling** | 3 | unknown catch, Error-only |
| **Async & Concurrency** | 3 | No floats, Promise.all |
| **Objects, Arrays & Collections** | 4 | Indexed access, readonly |
| **Enums, Literals & Erasable Syntax** | 2 | Erasable code, unions |
| **Classes & OOP** | 2 | #private, no getters |
| **Modules & Declarations** | 2 | import type, export types |
| **Config & Compiler (TS 7)** | 5 | strict, erasable, TS7 split |
| **Performance (types + build)** | 2 | Emit speed, parallel flags |
| **Testing (types)** | 1 | expectTypeOf |
| **Documentation (TSDoc)** | 1 | Intent over types |
| **Linting & Tooling** | 1 | Lint/TS version split |
| **Project Structure** | 1 | devDeps, rootDir |
| **Anti-patterns** | 6 | Fix-ups index |
<!-- gen:end:categories -->

Every rule has a reason, a bad example, a good example, and links onward. Full rule list with links: [SKILL.md](./SKILL.md).

## How it works

Each skill is one index (`SKILL.md`) plus one file per rule (`rules/`). Prefixes match categories. That is the whole design. Rule files are the source of truth. Everything tabular in these READMEs regenerates from them, and CI fails if the index is stale.

## Manual install

```bash
git clone https://github.com/Mvkweb/skills.git <agent-skills-dir>/typescript-skills
```

For `csharp-skills` or `swiftlys2-skills`, clone the repo and copy that subdir into your agent skills dir. Targets per agent:

- Claude Code (global): `~/.claude/skills/<skill-name>`
- Claude Code (one project): `.claude/skills/<skill-name>`
- OpenCode: `.opencode/skills/<skill-name>`
- Cursor: `.cursor/skills/<skill-name>`, or single file via `curl -o .cursorrules https://raw.githubusercontent.com/Mvkweb/skills/main/SKILL.md`
- Codex: `.codex/skills/<skill-name>`
- Copilot: `curl -o .github/copilot-instructions.md https://raw.githubusercontent.com/Mvkweb/skills/main/SKILL.md`
- Any AGENTS.md agent: `curl -o AGENTS.md https://raw.githubusercontent.com/Mvkweb/skills/main/SKILL.md`

Then: `/typescript-skills review this function`.

## Contributing

Small focused changes. Every rule traces to a fetched human source or to upstream instruction text (provenance in `<!-- source: -->`).

```bash
# 1. write <skill>/rules/<prefix>-<name>.md  (# id, > summary, Why / Bad / Good / See Also)
python3 <skill>/checks/gen_index.py --write  # 2. refresh that skill index
bash <skill>/checks/check.sh                 # 3. keep it green, baseline empty
python3 eng/gen_root.py --write              # 4. refresh this front page
```

Never hand-edit inside `<!-- gen:begin -->` markers.

## Sources

TypeScript skill: Vanderkam's Effective TypeScript, Pocock's Total TypeScript tips, Goldberg's Learning TypeScript, Microsoft's Handbook, Cursor's pstack modeling rules. C# skill: verbatim excerpts from dotnet/skills (MIT). SwiftlyS2 skill: official SwiftlyS2 docs, sw2-mdwiki, official repository. Synthesized and reorganized, not copied where it matters. Upstream materials remain under their own licenses. Original text is MIT.
