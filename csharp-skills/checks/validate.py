#!/usr/bin/env python3
"""Structural gate for csharp-skills. No toolchain needed.

Checks (fail fast with a clear message):
  1. SKILL.md frontmatter (name, description, license, metadata.version).
  2. Every `rules/*.md` link in SKILL.md resolves, and every rule file is indexed.
  3. Category-table counts match actual `<prefix>-` file counts per prefix.
  4. Every rule file has: `# id` matching filename, `> summary`,
     `<!-- source: ... -->` provenance comment, `## See Also`.
  5. Every rule file carries at least one fenced block (csharp/xml/bash/json)
     OR at least one http link / markdown table (guide-style rules allowed).
  6. Every `## See Also` link resolves to an existing rule file.
  7. No AGENTS.md / CLAUDE.md copies inside the skill: SKILL.md is the
     single file by design (the repo-root AGENTS.md holds local process).

Usage:  python3 checks/validate.py   (run from the skill root)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = ROOT / "rules"
SKILL = ROOT / "SKILL.md"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    skill = SKILL.read_text()

    # 1. frontmatter
    m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not m:
        fail("SKILL.md: missing YAML frontmatter block")
        front = ""
    else:
        front = m.group(1)
        for key in ("name:", "description:", "license:", "author:", "version:"):
            if key not in front:
                fail(f"SKILL.md frontmatter: missing `{key.rstrip(':')}`")

    # 2. index <-> files parity
    refs = re.findall(r"rules/([a-z0-9-]+\.md)", skill)
    files = sorted(p.name for p in RULES.glob("*.md"))
    for r in refs:
        if r not in files:
            fail(f"SKILL.md links rules/{r} which does not exist")
    for f in files:
        if f not in refs:
            fail(f"rules/{f} exists but is not indexed in SKILL.md")
    if len(refs) != len(set(refs)):
        dupes = sorted({r for r in refs if refs.count(r) > 1})
        fail(f"SKILL.md indexes these twice: {dupes}")

    # 3. category-table counts match prefix counts
    table_counts: dict[str, int] = {}
    for prefix, count in re.findall(r"`([a-z]+)-`\s*\|\s*(\d+)", skill):
        table_counts[prefix] = int(count)
    actual: dict[str, int] = {}
    for f in files:
        actual[f.split("-")[0]] = actual.get(f.split("-")[0], 0) + 1
    for prefix, count in table_counts.items():
        if actual.get(prefix, 0) != count:
            fail(
                f"category `{prefix}-`: table says {count}, "
                f"found {actual.get(prefix, 0)} files"
            )
    for prefix in actual:
        if prefix not in table_counts:
            fail(f"prefix `{prefix}-` has files but no category-table row")

    # 4 + 5 + 6. per-rule structure
    for path in sorted(RULES.glob("*.md")):
        text = path.read_text()
        stem = path.stem
        if not text.startswith(f"# {stem}\n"):
            fail(f"rules/{path.name}: first line must be `# {stem}`")
        if not re.search(r"^> .+", text, re.M):
            fail(f"rules/{path.name}: missing `> one-line summary`")
        if "<!-- source:" not in text:
            fail(f"rules/{path.name}: missing `<!-- source: ... -->` provenance")
        if "## See Also" not in text:
            fail(f"rules/{path.name}: missing `## See Also`")
        has_fence = bool(re.search(r"^```(csharp|xml|bash|json|jsonc|powershell|shell|dotnetcli)", text, re.M))
        has_link = "http" in text
        has_table = bool(re.search(r"^\|.+\|$", text, re.M))
        if not (has_fence or has_link or has_table):
            fail(
                f"rules/{path.name}: no fenced example block and no "
                f"link/table either"
            )
        for link in re.findall(r"\(([a-z0-9-]+\.md)\)", text):
            if link.startswith("http"):
                continue
            if not (RULES / link).exists():
                fail(f"rules/{path.name}: See Also links missing file {link}")

    # 7. no stray agent-compat copies
    for compat in ("AGENTS.md", "CLAUDE.md"):
        if (ROOT / compat).exists() or (ROOT / compat).is_symlink():
            fail(f"{compat}: must not exist — SKILL.md is the single source")

    if errors:
        print(f"{len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    n = len(files)
    cats = len(table_counts)
    print(f"OK: {n} rules across {cats} categories, index + links + compat in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
