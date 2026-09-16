#!/usr/bin/env bash
# One command that reproduces CI locally. Run from the skill root:
#
#     bash checks/check.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> structure, links, and index parity"
python3 "$ROOT/checks/validate.py"
python3 "$ROOT/checks/gen_index.py" --check

echo "==> generating example files from rules"
cd "$ROOT/checks"
python3 gen.py

echo "==> dotnet compile gate"
mkdir -p gate
cp support/Smoke.csproj gate/gate.csproj
cp support/Smoke.cs gate/Program.cs
if compgen -G "examples/*.cs" > /dev/null; then
  cp examples/*.cs gate/
  echo "including $(ls examples/*.cs | wc -l) opt-in rule snippet(s)"
else
  echo "no opt-in rule snippets; building smoke only"
fi
dotnet build gate/gate.csproj --nologo -v q
rm -rf gate

echo "All checks passed."
