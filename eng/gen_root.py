#!/usr/bin/env python3
"""Keep the repo-root README skill index in sync with all skills.

Each skill dir is the source of truth (its own rules/ + SKILL.md index).
This script rewrites two marked regions in the repo-root README.md:

  README.md  <!-- gen:begin:skills --> / <!-- gen:begin:total -->

Every per-skill check.sh stays independent; CI also runs this script in
--check mode so a stale root index fails the build. Usage:

  python3 eng/gen_root.py           check only (CI-safe default)
  python3 eng/gen_root.py --write   rewrite README.md
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

SKILLS = [
    {"dir": ".", "name": "typescript-skills",
     "covers": "Strict TypeScript, TS 7-ready",
     "skill_ref": "./SKILL.md"},
    {"dir": "csharp-skills", "name": "csharp-skills",
     "covers": "Nullable C#, builds, tests",
     "skill_ref": "./csharp-skills/SKILL.md"},
    {"dir": "swiftlys2-skills", "name": "swiftlys2-skills",
     "covers": "CS2 server plugins (game APIs)",
     "skill_ref": "./swiftlys2-skills/SKILL.md"},
]


def fail(msg: str) -> "NoReturn":
    raise SystemExit(f"gen_root: {msg}")


def stats(skill_dir: pathlib.Path) -> tuple[int, int]:
    rules = sorted((skill_dir / "rules").glob("*.md"))
    if not rules:
        fail(f"{skill_dir}: no rules/*.md found")
    prefixes = {p.name.split("-")[0] for p in rules}
    # Count rows inside the generated category table only (task-mapping
    # tables elsewhere also use `prefix-` backticks).
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- gen:begin:table -->\n(.*?)(\n<!-- gen:end:table -->)",
                  skill_text, re.S)
    table_prefixes = re.findall(r"`([a-z]+)-`\s*\|", m.group(1)) if m else []
    ncat = len(table_prefixes) if table_prefixes else len(prefixes)
    return len(rules), ncat


def region(text: str, name: str) -> tuple[str, str, str]:
    pattern = re.compile(
        r"(<!-- gen:begin:" + name + r" -->\n)(.*?)(\n<!-- gen:end:" + name + r" -->)",
        re.S,
    )
    m = pattern.search(text)
    if not m:
        fail(f"missing <!-- gen:begin:{name} --> markers in README.md")
    return m.group(1), m.group(2), m.group(3)


def render() -> str:
    rows = []
    total_rules = 0
    for s in SKILLS:
        d = ROOT / s["dir"]
        n, cats = stats(d)
        total_rules += n
        rows.append(
            f"| [{s['name']}]({s['skill_ref']}) | {n} | {cats} | {s['covers']} |"
        )
    table = ("| Skill | Rules | Categories | What it covers |\n"
             "|-------|-------|------------|----------------|\n"
             + "\n".join(rows))
    total = (f"{total_rules} rules across {len(SKILLS)} skills. "
             f"Each skill has its own index: open its `SKILL.md`.")
    readme = README.read_text(encoding="utf-8")
    pre, _, post = region(readme, "skills")
    readme = readme.replace(pre + region(readme, "skills")[1] + post,
                            pre + table + post)
    pre, _, post = region(readme, "total")
    readme = readme.replace(pre + region(readme, "total")[1] + post,
                            pre + total + post)
    return readme


def main() -> int:
    rendered = render()
    if "--write" not in sys.argv:
        if rendered != README.read_text(encoding="utf-8"):
            print("OUT OF DATE: README.md — run `python3 eng/gen_root.py --write`")
            return 1
        print("OK: root index matches all skills/")
        return 0
    README.write_text(rendered, encoding="utf-8")
    print("wrote root index")
    return 0


from typing import NoReturn

if __name__ == "__main__":
    sys.exit(main())
