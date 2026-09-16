# checks — verify the skill

Two gates, same as CI:

```bash
bash checks/check.sh   # run from the skill root
```

- `validate.py` — structure, links, index parity. Python only.
- `gen_index.py` — regenerates the marked index regions from `rules/`.
  Check (default) or rewrite with `--write`. Adding a rule means writing the
  rule file, then running `--write`. Never hand-edit inside the markers.
- `gen.py` + `dotnet build` — compiles `checks/support/Smoke.cs` plus any
  rule `## Good` snippet tagged `<!-- compile -->`. Most rule bodies are
  verbatim guide prose with fragment snippets, so compilation is opt-in per
  snippet, not all-fences. The gate project uses `net8.0`, `Nullable enable`,
  warnings as errors.

`baseline.txt` lists accepted suspects (currently none).
Generated files (`examples/`, `gate/`, `check.log`) are gitignored.
