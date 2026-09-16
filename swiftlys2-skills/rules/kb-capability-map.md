# kb-capability-map

> Snapshot of documented SDK surface and drift warnings

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-current-capability-map.md — body verbatim, header only added -->

This matrix is the toolkit's synchronization record for capability boundaries. It is not a mirror of the official documentation. It records the coverage scope of this pass against the latest official `llms-full.txt`, the directly reusable local assets, and the generated interfaces that must still be confirmed on the official API pages.

## Snapshot Provenance

- URL: `https://swiftlys2.net/llms-full.txt`
- Pulled at: `2026-09-04`
- File size: `20,740,301` bytes
- SHA-256: `99FFB2799F49FF87D665DDD8779683F150BCB738FD990C1C71D7373957E6EFCD`

"New" in this file only means **already public in the current official snapshot, but not covered or inaccurately described by the older toolkit**. It does not claim in which version an API was first released.

## Comparison Principles

1. Manually maintained Development, Guides, and Resources pages are included in the matrix page by page.
2. API Reference currently contains a large number of generated pages (about 6,253 API H1 entries in this snapshot, including Protobuf, Schema, Game Event, and GameHooks types); the toolkit only maintains category entries and usage boundaries, and never statically copies member signatures.
3. When local templates are outdated, remove the old API path and converge on the single current path; do not keep fallbacks for CSS or old SwiftlyS2 calls.
4. After every SDK / server upgrade, re-check the snapshot on this page plus the relevant official category pages before changing executable templates.

## 1. Development Pages

| Official Topic | Current Capability Focus | Local Entry |
| --- | --- | --- |
| Commands | attribute, service registration, client command / chat hooks, queries and help text | `assets/development/commands/` |
| Configuration | JSONC / TOML, template init, options monitor, base path | `assets/development/configuration/` |
| Convars | typed / string APIs, replication, client queries, safe min / max / default reads | `assets/development/convars/convar-template.cs.md` |
| Core Events | lifecycle, event subscribe / unsubscribe, high-frequency event boundaries | `assets/development/core-events/` |
| Custom HUD | `custom_hud_layout` entity, per-player dialog-variable / CSS-class / input-capture state, `OnCustomHudClicked` | `references/swiftlys2-custom-hud.md` |
| Database | global config, `IDbConnection`, ADO.NET / ORM, secret handling | `assets/development/database/database-connection-template.cs.md` |
| Entity | create / spawn, handles, input / output, schema boundaries | `assets/development/entity/` |
| Entity Key Values | typed key-value container, dispose, spawn integration | `assets/development/entity/entity-key-values-guide.md` |
| Game Events | generated event fire / hook, Pre / Post, temporary wrappers | `assets/development/game-events/game-events-usage-notes.md` |
| Getting Started | project / plugin baseline | `assets/development/getting-started/partial-plugin-template.cs.md` |
| Menus | builder, option types, dynamic binding, async callbacks | `assets/development/menus/menu-template.cs.md` |
| Native Functions and Hooks | gamedata, memory, exact delegates, function / mid hooks | `assets/development/native-functions-and-hooks/hook-handler-template.cs.md` |
| Network Messages | typed send / create, client / server / internal hooks, temporary wrappers | `assets/development/netmessages/protobuf-handler-template.cs.md` |
| Permissions | checks, groups, hierarchy, current clear / remove APIs | `assets/development/permissions/README.md` |
| Profiler | record / measure and hot-path evidence | `assets/development/profiler/hotpath-gc-checklist.md` |
| Scheduler | main-loop dispatch, timer CTS, `AddTimer` | `assets/development/scheduler/scheduler-vs-worker-guide.md` |
| Shared API | provider / consumer callbacks and interface lifecycle | `assets/development/shared-api/shared-interface-template.cs.md` |
| Sound Events | recipient filters, typed fields, `Emit` / `EmitAsync` | `assets/development/sound-events/sound-event-guide.md` |
| Steamworks | server APIs, activation, callback lifetime, workshop / auth | `assets/development/steamworks/steamworks-server-guide.md` |
| Swiftly Core | service entry points and thread awareness | `assets/development/swiftly-core/core-service-entrypoints.md` |
| Thread Safety | `[ThreadUnsafe]`, async pairs, explicit main-loop dispatch | `assets/development/thread-safety/thread-sensitivity-checklist.md` |
| Translations | player / server localizers and placeholders | `assets/development/translations/README.md` |
| Using attributes | discovery, registration, and signature validation | `assets/development/using-attributes/attribute-registration-checklist.md` |

## 2. Guides and Resources

| Official Topic | Current Capability Focus | Local Entry |
| --- | --- | --- |
| Chat & CenterHTML Styling | chat colors and Panorama HTML | `assets/guides/html-styling/README.md` |
| Dependency Injection | `AddSwiftly`, service ownership, attribute registration | `assets/guides/dependency-injection/` |
| Development Flow | Official page is still placeholder content; do not use as an implementation basis | `references/swiftlys2-official-docs-map.md` |
| Porting from CounterStrikeSharp | current API migration and CSS-only API removal | `assets/guides/porting-from-css/porting-checklist.md` |
| Terminologies | controller / pawn / player / entity / handle vocabulary | `assets/guides/terminologies/README.md` |
| CLI Options | startup paths / log levels / log visibility | `assets/resources/runtime-configuration-guide.md` |
| Core Configuration | `core.jsonc` global runtime policy | `assets/resources/runtime-configuration-guide.md` |
| Command Overrides | deployment-side command permission remapping | `assets/resources/runtime-configuration-guide.md` |
| Console Filter | verified noise filtering and reload workflow | `assets/resources/runtime-configuration-guide.md` |

## 3. API Category Coverage

The following categories all exist in the current official snapshot. The toolkit covers them via "check the current signature from the category page first" and does not keep stale local copies for generated types.

| Area | API Categories |
| --- | --- |
| Core / DI | `ConsoleOutput`, `FileSystem`, `Helpers`, `HtmlGradient`, `IInterfaceManager`, `ISwiftlyCore`, `PluginMetadata`, `Scheduler`, `Shared`, `SwiftlyCoreInjection`, `SwiftlyInject`, `SwiftlyOptionsFactory` |
| Runtime services | `CommandLine`, `Commands`, `Convars`, `Database`, `Engine`, `EntitySystem`, `Events`, `GameEvents`, `Memory`, `Menus`, `NetMessages`, `Permissions`, `Plugins`, `Players`, `Profiler`, `Services`, `Sounds`, `SteamAPI`, `StringTable`, `Trace`, `Translation` |
| Native / generated surfaces | `Datamaps`, `GameEventDefinitions`, `GameHooks`, `Natives`, `Schemas`, `ProtobufDefinitions`, `SchemaDefinitions`, `Misc`, `Helper` |

New or drift-prone categories to track first:

- `GameHooks`: typed Pre / Post contexts replacing several legacy `Core.Event.On*Hook` entries.
- `GameEventDefinitions`: generated Game Event fields change with game / SDK updates.
- `Datamaps`, `Schemas`, `SchemaDefinitions`: native layout and generated schemas cannot be inferred from old examples.
- `ProtobufDefinitions`, `NetMessages`: message fields and hook pipelines follow the current API.
- `CommandLine`, `Engine`, `EntitySystem`, `Profiler`, `Trace`: runtime diagnostics entries that local navigation used to miss.
- `CCSCustomHudLayout`, `EHudPanelClassStatus_t`, `IOnCustomHudClickedEvent`: Custom HUD is marked new and unstable by the official docs; schema and event surfaces drift fastest with SDK changes, so check the current API page before implementing.

## 4. High-Priority Diffs in This Sync

| Old Toolkit Problem | Current Sync Conclusion |
| --- | --- |
| Treating `DynamicHook` / `[HookCallback]` as SwiftlyS2 native-hook templates | Removed; typed hooks go through `Core.GameHooks`, raw hooks go through `Core.Memory` + exact delegate + `next()` chain |
| Core event hooks still used for usercmd, touch, damage, movement, weapon paths | Marked as migration targets; use the matching `Core.GameHooks` category instead |
| Game Events documented with attributes only | Added `HookPre` / `HookPost` `Guid`, `Unhook`, temporary event / accessor, `FireAsync*` |
| Post hooks implying cancellation | Clarified that `Handled` / `Stop` have no effect in Post |
| Client command hooks assumed to depend on `registerRaw` | Removed that precondition; `registerRaw` only controls the `sw_` prefix |
| Command templates using `Arguments` and the old attributes namespace | Changed to `ICommandContext.Args` and `SwiftlyS2.Shared.Commands` |
| `SERVER_CAN_EXECUTE` treated as a permission restriction | Changed to `ConvarFlags.NONE` by default; permissions are enforced at the command / RCON / permission layers |
| Old scheduler examples assuming timers auto-bind to the map CTS | Timers return their own CTS, passed explicitly to `StopOnMapChange`; async scheduler lambdas are forbidden |
| `GetPlayerBySteamId`, `.Valid()`, `SetStateChanged()` | Changed to current `GetPlayerFromSteamId` / `GetPlayerFromSessionId`, `IsValid`, `Updated()` |
| Resources and several Development pages with official links but no local entries | Added database, KeyValues, sound, Steamworks, Memory, migration, and operations assets |
| Officially added Custom HUD development page (2026-09-04 snapshot) | Added `references/swiftlys2-custom-hud.md`: entity creation chain, per-player state semantics (overrides do not fall back to global), click events and Async boundaries |

## 5. Scope Deliberately Not Copied Statically

The following must be re-verified per task from the official site / API category pages instead of baking the current snapshot into the skill:

- Exact fields and availability of each generated Game Event, Protobuf, Schema, and Datamap.
- Exact params, Pre / Post contexts, and writable values for each GameHook.
- Raw signatures, vtable indexes, calling conventions, mid-hook register layouts.
- Steam callback types, game app IDs, current server / Workshop environment behavior.
- Actual install paths and current server deployment overrides for Resources configs.

This is not an omission. It prevents local static copies from becoming stale API sources of truth again.

## See Also

- [kb-index](kb-index.md)
- [kb-docs-map](kb-docs-map.md)
- [kb-asset-inventory](kb-asset-inventory.md)
