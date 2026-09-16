# checks — verify the skill

One gate, same as CI:

```bash
bash checks/check.sh   # run from the skill root
```

- `validate.py` — structure, links, C# separation, index parity. Python only.
- `gen_index.py` — regenerates the marked index regions from `rules/`.
  Check (default) or rewrite with `--write`. Adding a rule means writing the
  rule file, then running `--write`. Never hand-edit inside the markers.

No compiler gate by design: CS2 server APIs only exist inside the game
server, so snippets can't build in CI. Pure-C# helpers follow the
`csharp-skills` dotnet gate instead.
