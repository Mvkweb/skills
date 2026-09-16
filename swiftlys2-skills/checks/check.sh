#!/usr/bin/env bash
# One command that reproduces CI locally. Run from the skill root:
#
#     bash checks/check.sh
#
# No compiler gate: CS2 server APIs don't exist outside the game server.
# Pure-C# helpers are covered by the csharp-skills dotnet gate instead.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> structure, links, separation, and index parity"
python3 "$ROOT/checks/validate.py"
python3 "$ROOT/checks/gen_index.py" --check

echo "All checks passed."
