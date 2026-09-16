#!/usr/bin/env python3
"""Extract opt-in ```csharp blocks from rules/*.md into checks/examples/.

Only ```csharp blocks inside a ## Good section AND preceded by an
`<!-- compile -->` marker are extracted: most rule bodies are verbatim
guide prose with fragmentary snippets that must NOT compile. Each block
becomes one file in a shared console project so rules can't interfere
with each other.

Generated per-file snippets plus checks/support/Smoke.cs (always built)
form the dotnet compile gate. Generated files are disposable (gitignored).

Usage:
    cd checks && python3 gen.py
"""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = ROOT / "rules"
CHECKS = ROOT / "checks"
OUT = CHECKS / "examples"


def good_compilable_blocks(text: str) -> list[str]:
    """Return ```csharp blocks in ## Good sections marked <!-- compile -->."""
    m = re.search(r"^## Good\s*$", text, re.M)
    if not m:
        return []
    tail = text[m.end():]
    nxt = re.search(r"^## \S", tail, re.M)
    section = tail[: nxt.start()] if nxt else tail
    out = []
    for mm in re.finditer(r"<!-- compile -->\s*\n```csharp\n(.*?)```", section, re.S):
        out.append(mm.group(1))
    return out


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    total = 0
    for path in sorted(RULES.glob("*.md")):
        for i, block in enumerate(good_compilable_blocks(path.read_text())):
            total += 1
            (OUT / f"{path.stem}--{i}.cs").write_text(
                f"// generated from rules/{path.name} ## Good block {i}\n"
                f"{block.strip()}\n"
            )
    print(f"extracted {total} compile-tagged Good blocks from {len(list(RULES.glob('*.md')))} rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
