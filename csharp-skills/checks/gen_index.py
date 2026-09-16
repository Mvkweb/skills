#!/usr/bin/env python3
"""Keep the generated index regions in sync with rules/.

Rule files are the source of truth: each file's `# id` header, its
`> summary` line, and the CATEGORIES table below (prefix -> title, impact,
README blurb). The script rewrites four marked regions plus the SKILL lede
sentence:

  SKILL.md   <!-- gen:begin:table --> / <!-- gen:begin:quickref -->
  README.md  <!-- gen:begin:badges --> / <!-- gen:begin:categories -->

Rule order inside a category follows the current SKILL.md; brand-new rules
are appended alphabetically. Usage:

  python3 checks/gen_index.py           check only (CI-safe default)
  python3 checks/gen_index.py --write   rewrite SKILL.md + README.md
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RULES = ROOT / "rules"
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"

CATEGORIES = [
    {"prefix": "null-", "title": "Nullable Safety", "impact": "CRITICAL",
     "covers": "NRT migration, zero warnings"},
    {"prefix": "async-", "title": "Async & Cancellation", "impact": "HIGH",
     "covers": "Cooperative CancellationToken"},
    {"prefix": "perf-", "title": "Performance", "impact": "HIGH",
     "covers": "Anti-pattern scan, tiered fixes"},
    {"prefix": "refactor-", "title": "Refactoring", "impact": "HIGH",
     "covers": "Behavior-preserving edits"},
    {"prefix": "build-", "title": "Build & MSBuild", "impact": "MEDIUM",
     "covers": "Binlogs, props, antipatterns"},
    {"prefix": "test-", "title": "Testing", "impact": "MEDIUM",
     "covers": "Run tests, platform, seams"},
]


def fail(msg: str) -> "NoReturn":
    raise SystemExit(f"gen_index: {msg}")


def summaries() -> dict[str, str]:
    """Map rule id -> its `> summary` line."""
    out = {}
    for path in RULES.glob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("> "):
                out[path.stem] = line[2:].strip()
                break
        else:
            fail(f"rules/{path.name} has no `> summary` line")
    return out


def grouped(by_summary: dict[str, str]) -> dict[str, list[str]]:
    """Bucket rule ids per category prefix, preserving SKILL.md order."""
    known = {c["prefix"] for c in CATEGORIES}
    stray = sorted({rid.split("-")[0] + "-" for rid in by_summary} - known)
    if stray:
        fail(f"unknown prefix (add to CATEGORIES): {stray}")

    current = re.findall(r"rules/([a-z0-9-]+)\.md", SKILL.read_text(encoding="utf-8"))
    seen = set()
    ordered_all = [r for r in current if r not in seen and not seen.add(r)]

    groups: dict[str, list[str]] = {}
    for cat in CATEGORIES:
        in_cat = [r for r in ordered_all if r.startswith(cat["prefix"])]
        fresh = sorted(r for r in by_summary if r.startswith(cat["prefix"]) and r not in in_cat)
        groups[cat["prefix"]] = in_cat + fresh
    return groups


def region(text: str, name: str) -> tuple[str, str, str]:
    """Split text into (before, inside, after) a gen marker pair."""
    pattern = re.compile(
        r"(<!-- gen:begin:" + name + r" -->\n)(.*?)(\n<!-- gen:end:" + name + r" -->)",
        re.S,
    )
    m = pattern.search(text)
    if not m:
        fail(f"missing <!-- gen:begin:{name} --> markers")
    return m.group(1), m.group(2), m.group(3)


def build_table(groups: dict[str, list[str]]) -> str:
    head = "| Priority | Category | Impact | Prefix | Rules |"
    sep = "|----------|----------|--------|--------|-------|"
    rows = [
        f"| {i} | {c['title']} | {c['impact']} | `{c['prefix']}` | {len(groups[c['prefix']])} |"
        for i, c in enumerate(CATEGORIES, 1)
    ]
    return head + "\n" + sep + "\n" + "\n".join(rows)


def build_quickref(groups: dict[str, list[str]], by_summary: dict[str, str]) -> str:
    parts = []
    for i, cat in enumerate(CATEGORIES, 1):
        lines = [f"### {i}. {cat['title']} ({cat['impact']})", ""]
        for rid in groups[cat["prefix"]]:
            lines.append(f"- [`{rid}`](rules/{rid}.md) - {by_summary[rid]}")
        parts.append("\n".join(lines))
    return "\n\n".join(parts)


def build_badges(total: int, ncat: int) -> str:
    base = "https://img.shields.io/badge"
    flat = "style=flat-square"
    return "\n".join([
        f"![rules]({base}/rules-{total}-512BD4?{flat}&logo=csharp&logoColor=white)",
        f"![categories]({base}/categories-{ncat}-89b4fa?{flat}&logo=csharp&logoColor=white)",
        f"![C#]({base}/C%23-nullable-512BD4?{flat}&logo=csharp&logoColor=white)",
        "![ci](https://github.com/Mvkweb/skills/actions/workflows/ci.yml/badge.svg)",
        f"![PRs]({base}/PRs-welcome-brightgreen?{flat})",
        f"![license]({base}/license-MIT-green?{flat})",
    ])


def build_categories(groups: dict[str, list[str]]) -> str:
    lines = [f"{sum(len(v) for v in groups.values())} rules split into {len(CATEGORIES)} categories:", ""]
    lines.append("| Category | Rules | What it covers |")
    lines.append("|----------|-------|----------------|")
    for cat in CATEGORIES:
        lines.append(f"| **{cat['title']}** | {len(groups[cat['prefix']])} | {cat['covers']} |")
    return "\n".join(lines)


def render() -> tuple[str, str]:
    by_summary = summaries()
    groups = grouped(by_summary)
    total = sum(len(v) for v in groups.values())

    skill = SKILL.read_text(encoding="utf-8")
    pre, _, post = region(skill, "table")
    skill = skill.replace(pre + region(skill, "table")[1] + post,
                          pre + build_table(groups) + post)
    pre, _, post = region(skill, "quickref")
    skill = skill.replace(pre + region(skill, "quickref")[1] + post,
                          pre + build_quickref(groups, by_summary) + post)
    skill, n = re.subn(r"\d+ rules across \d+ categories",
                        f"{total} rules across {len(CATEGORIES)} categories", skill)
    if n != 1:
        fail("SKILL lede sentence not found (expected one `N rules across M categories`)")

    readme = README.read_text(encoding="utf-8")
    pre, _, post = region(readme, "badges")
    readme = readme.replace(pre + region(readme, "badges")[1] + post,
                            pre + build_badges(total, len(CATEGORIES)) + post)
    pre, _, post = region(readme, "categories")
    readme = readme.replace(pre + region(readme, "categories")[1] + post,
                            pre + build_categories(groups) + post)
    return skill, readme


def main() -> int:
    skill_new, readme_new = render()
    if "--write" not in sys.argv:
        stale = []
        if skill_new != SKILL.read_text(encoding="utf-8"):
            stale.append("SKILL.md")
        if readme_new != README.read_text(encoding="utf-8"):
            stale.append("README.md")
        if stale:
            print(f"OUT OF DATE: {', '.join(stale)} — run `python3 checks/gen_index.py --write`")
            return 1
        print("OK: index matches rules/")
        return 0
    SKILL.write_text(skill_new, encoding="utf-8")
    README.write_text(readme_new, encoding="utf-8")
    print("wrote index")
    return 0


from typing import NoReturn

if __name__ == "__main__":
    sys.exit(main())
