# kb-asset-inventory

> Catalog of templates, checklists, and guides in assets

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-asset-inventory.md — body verbatim, header only added -->

This inventory describes the public assets in the `swiftlys2-toolkit` skill that are directly relevant to SwiftlyS2 engineering workflows.

## 1. Core Assets

### Skill
- `SKILL.md`

### Workflow References
- `references/plan-workflow.md`
- `references/audit-workflow.md`
- `references/edit-workflow.md`

### References
- `references/swiftlys2-plugin-playbook.md`
- [references/swiftlys2-performance-optimization-playbook.md](./swiftlys2-performance-optimization-playbook.md)
- `references/swiftlys2-kb-index.md`
- `references/swiftlys2-official-docs-map.md`
- `references/swiftlys2-current-capability-map.md`
- `references/swiftlys2-custom-hud.md`
- `references/swiftlys2-asset-inventory.md`

### Templates / Assets
- `assets/README.md`
- `assets/development/getting-started/partial-plugin-template.cs.md`
- `assets/development/using-attributes/attribute-registration-checklist.md`
- `assets/development/swiftly-core/core-service-entrypoints.md`
- `assets/development/commands/command-attribute-template.cs.md`
- `assets/development/commands/command-service-template.cs.md`
- `assets/development/commands/client-command-hook-template.cs.md`
- `assets/development/menus/menu-template.cs.md`
- `assets/development/netmessages/protobuf-handler-template.cs.md`
- `assets/development/game-hooks/game-hooks-pre-post-guide.md`
- `assets/development/native-functions-and-hooks/hook-handler-template.cs.md`
- `assets/development/database/database-connection-template.cs.md`
- `assets/development/entity/entity-key-values-guide.md`
- `assets/development/sound-events/sound-event-guide.md`
- `assets/development/steamworks/steamworks-server-guide.md`
- `assets/development/memory/memory-service-guide.md`
- `assets/development/thread-safety/thread-sensitivity-checklist.md`
- `assets/development/profiler/hotpath-gc-checklist.md`
- `assets/development/entity/schema-write-checklist.md`
- `assets/development/core-events/lifecycle-checklist.md`
- `assets/development/core-events/precache-resource-template.cs.md`
- `assets/development/scheduler/scheduler-vs-worker-guide.md`
- `assets/development/shared-api/shared-interface-template.cs.md`
- `assets/development/game-events/game-events-usage-notes.md`
- `assets/development/configuration/README.md`
- `assets/development/configuration/config-hot-reload-template.cs.md`
- `assets/development/translations/README.md`
- `assets/development/permissions/README.md`
- `assets/development/convars/convar-template.cs.md`
- `assets/guides/dependency-injection/di-service-plugin-template.cs.md`
- `assets/guides/dependency-injection/service-template.cs.md`
- `assets/guides/terminologies/README.md`
- `assets/guides/html-styling/README.md`
- `assets/guides/porting-from-css/porting-checklist.md`
- `assets/resources/runtime-configuration-guide.md`
- `assets/patterns/background-workers/worker-template.cs.md`
- `assets/patterns/async-patterns/async-safety-guide.md`
- `assets/patterns/per-player-state/player-state-management-guide.md`
- `assets/patterns/service-factory/service-factory-template.cs.md`
- `assets/workflows/planning/method-level-plan-template.md`
- `assets/workflows/audit/audit-report-template.md`

### Optional Workspace Layer

The nearest-level `AGENTS.md` in a downstream workspace and the project-local skills it explicitly references form an optional workspace layer. They are not counted as core skill assets.

## 2. Counting Convention

- Skill: 1
- Workflow References: 3
- Domain References: 7
- Templates / Assets: 41
- Optional Workspace Layer: 0

**Total: 52 core assets**

## 3. Layering Principles

### Public Layer

The following are suitable for shipping publicly with the toolkit:

- Skill
- General workflow references
- General references
- General templates and checklists

### Workspace Layer

The following carry customization for the current workspace:

- Nearest-level `AGENTS.md`
- Project-local skills or reference material explicitly referenced by `AGENTS.md`

These files may record:

- Current workspace project maps
- Local reference repository paths
- Workspace-specific build commands
- Current maintainer constraints

But this information must not be written back into the public skill / workflow references / templates.

## 4. Naming Conventions

The current general toolkit uses the following naming strategy:

- Skills / domain references use the `swiftlys2-` prefix uniformly; workflows use `<intent>-workflow.md`
- Assets use "directory carries semantics, filename carries responsibility" and prefer naming aligned with the official Development / Guides categories
- This keeps assets discoverable and avoids repeating verbose prefixes in filenames deep in the tree

## 5. Maintenance Guidance

- When adding a general SwiftlyS2 tool, prefer placing it inside the current toolkit structure and keep the `swiftlys2-` prefix
- When adding one-off task documents, keep them separate from the public toolkit
- If local paths, workspace-specific project names, or maintainer-private repository names leak into public docs, move them back into the downstream repository's `AGENTS.md` or a project-local skill

## See Also

- [kb-index](kb-index.md)
- [kb-docs-map](kb-docs-map.md)
- [kb-capability-map](kb-capability-map.md)
