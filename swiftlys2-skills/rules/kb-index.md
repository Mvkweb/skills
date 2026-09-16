# kb-index

> Index of official docs, wiki, repo, and toolkit entry points

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-kb-index.md — body verbatim, header only added -->

This index is for quickly locating **publicly citable** SwiftlyS2 reference entries.

If the current workspace also has local reference repositories, project maps, historical reference projects, or customized experience, register them in the nearest-level `AGENTS.md` or in a project-local skill it explicitly references. Do not write them back here.

## 1. SwiftlyS2 Official Entries

### Root Entry

- Docs Root: `https://swiftlys2.net/docs/`
- Docs Map (this toolkit's condensed navigation): `./swiftlys2-official-docs-map.md`
- Current Capability Map (official snapshot comparison for this pass): `./swiftlys2-current-capability-map.md`
- API Reference: `https://swiftlys2.net/docs/api/`

### Main Development Section Entries

- Installation: `https://swiftlys2.net/docs/installation/`
- Getting Started: `https://swiftlys2.net/docs/development/getting-started/`
- Swiftly Core: `https://swiftlys2.net/docs/development/swiftly-core/`
- Using attributes: `https://swiftlys2.net/docs/development/using-attributes/`
- Thread Safety: `https://swiftlys2.net/docs/development/thread-safety/`
- Commands: `https://swiftlys2.net/docs/development/commands/`
- Configuration: `https://swiftlys2.net/docs/development/configuration/`
- Translations: `https://swiftlys2.net/docs/development/translations/`
- Entity: `https://swiftlys2.net/docs/development/entity/`
- Entity Key Values: `https://swiftlys2.net/docs/development/entitykeyvalues/`
- Game Events: `https://swiftlys2.net/docs/development/game-events/`
- Core Events: `https://swiftlys2.net/docs/development/core-events/`
- GameHooks API: `https://swiftlys2.net/docs/api/gamehooks/`
- Network Messages: `https://swiftlys2.net/docs/development/netmessages/`
- Menus: `https://swiftlys2.net/docs/development/menus/`
- Convars: `https://swiftlys2.net/docs/development/convars/`
- Native Functions and Hooks: `https://swiftlys2.net/docs/development/native-functions-and-hooks/`
- Scheduler: `https://swiftlys2.net/docs/development/scheduler/`
- Shared API: `https://swiftlys2.net/docs/development/shared-api/`
- Permissions: `https://swiftlys2.net/docs/development/permissions/`
- Profiler: `https://swiftlys2.net/docs/development/profiler/`
- Database: `https://swiftlys2.net/docs/development/database/`
- Sound Events: `https://swiftlys2.net/docs/development/soundevents/`
- Steamworks: `https://swiftlys2.net/docs/development/steamworks/`
- Custom HUD: `https://swiftlys2.net/docs/development/custom-hud/`

### Main Resources Section Entries

- CLI Options: `https://swiftlys2.net/docs/resources/cli-options/`
- Core Configuration: `https://swiftlys2.net/docs/resources/core-configuration/`
- Command Overrides: `https://swiftlys2.net/docs/resources/command-overrides/`
- Console Filter: `https://swiftlys2.net/docs/resources/console-filter/`

### Main Guides Section Entries

- Dependency Injection: `https://swiftlys2.net/docs/guides/dependency-injection/`
- Development Flow (still a placeholder todo on the official site): `https://swiftlys2.net/docs/guides/development-flow/`
- Chat & CenterHTML Styling: `https://swiftlys2.net/docs/guides/chat-and-html-styling/`
- Porting from CounterStrikeSharp: `https://swiftlys2.net/docs/guides/porting-from-css/`
- Terminologies: `https://swiftlys2.net/docs/guides/terminologies/`

### API Reference Usage Guidance

- This toolkit does not embed a full API Reference extraction, to avoid size bloat.
- Read first: the lean API Reference navigation in `./swiftlys2-official-docs-map.md`.
- Then drill down online per section as needed: e.g. `commands`, `netmessages`, `players`, `schemas`, `services`.
- If existing navigation is still insufficient, treat `https://swiftlys2.net/llms-full.txt` as the last-resort full-text source; ask the user before reading it and only do local keyword / segmented retrieval.

### Full LLM Documentation

- Address: `https://swiftlys2.net/llms-full.txt`
- Content: single-file LLM-optimized build of all SwiftlyS2 official docs (intro, installation, API Reference, Development guides, Guides, Porting guides, etc.).
- Purpose: **last-resort** API lookup, full-text search, interface-signature confirmation, and official-example lookup.
- Usage constraint: ask the user before reading; after approval only do local keyword or segmented retrieval. Never scan the whole file.

## 2. This Toolkit's Asset Navigation

- Assets Root: `../assets/README.md`
- Current Capability Map: `./swiftlys2-current-capability-map.md`
- Performance Playbook: `./swiftlys2-performance-optimization-playbook.md`
- Development-topic assets: `../assets/development/`
- Guides-topic assets: `../assets/guides/`
- Unofficial engineering patterns: `../assets/patterns/`
- Workflow templates: `../assets/workflows/`

## 3. sw2-mdwiki Quick Entries

Repository: `https://github.com/himenekocn/sw2-mdwiki`

### Frequently Checked Categories

- `SwiftlyS2/Shared/Players/IPlayer.md`
- `SwiftlyS2/Shared/Players/IPlayerManagerService.md`
- `SwiftlyS2/Shared/IInterfaceManager.md`
- `SwiftlyS2/Shared/ISwiftlyCore.md`
- `SwiftlyS2/Shared/Commands/ICommandContext.md`
- `SwiftlyS2/Shared/Commands/Command.md`
- `SwiftlyS2/Shared/Commands/CommandAlias.md`
- `SwiftlyS2/Shared/Events/`
- `SwiftlyS2/Shared/NetMessages/INetMessageService.md`
- `SwiftlyS2/Shared/ProtobufDefinitions/README.md`
- `SwiftlyS2/Shared/SchemaDefinitions/README.md`
- `SwiftlyS2/Shared/EntitySystem/IEntitySystemService.md`
- `SwiftlyS2/Shared/Menus/`
- `SwiftlyS2/Core/Menus/OptionsBase/`

## 4. SwiftlyS2 Official Repository Entries

Repository: `https://github.com/swiftly-solution/swiftlys2`

### Structure Overview

- `src/`: C++ core framework
- `managed/src/`: C# managed layer
- `natives/`: native definitions
- `generator/`: code generation tools
- `plugin_files/`: plugin / package assets

## 5. Decide First, Then Look Up Docs

- **I want to register commands / aliases / chat hooks** → `Commands`
- **I want to listen to map / player / entity lifecycles** → `Core Events`
- **I want typed entity / controller / movement / pawn / weapon hooks** → `GameHooks` API + `assets/development/game-hooks/`
- **I want raw native functions / mid-hooks** → `Native Functions and Hooks` + `Memory`
- **I want to send typed protobuf / netmessages** → `Network Messages`
- **I want cross-plugin interfaces** → `Shared API`
- **I am unsure about await / NextTick / thread-sensitive APIs** → `Thread Safety`
- **I am unsure about controller / pawn / player / entity handles** → `Terminologies` + `Entity`

## 6. Scenario Index (Detailed)

### I Want to Write Commands

#### 1) I want partial / attribute commands

- Read the official docs first:
	1. `Commands`
	2. `Using attributes`
	3. `Thread Safety`
- Then read local assets:
	- `../assets/development/commands/command-attribute-template.cs.md`
	- `../assets/development/using-attributes/attribute-registration-checklist.md`
- Common APIs / keywords:
	- `ICommandContext`
	- `[Command]`
	- `[CommandAlias]`
	- `Reply` / `ReplyAsync`
- Common pitfalls:
	- Using attributes on non-main-class objects without `Core.Registrator.Register(this)`
	- Piling business logic directly into the command entry
	- Misusing synchronous thread-sensitive APIs in async contexts

#### 2) I want service-owned commands

- Read the official docs first:
	1. `Commands`
	2. `Dependency Injection`
	3. `Thread Safety`
- Then read local assets:
	- `../assets/development/commands/command-service-template.cs.md`
	- `../assets/guides/dependency-injection/service-template.cs.md`
- Common APIs / keywords:
	- `RegisterCommand`
	- `RegisterCommandAlias`
	- `UnregisterCommand`
	- `HookClientChat`
	- `HookClientCommand`
- Common pitfalls:
	- Not saving the `Guid`
	- Command registered by the root but assumed cleanable from a service
	- Alias cleanup diverging from the main-command cleanup path

#### 3) I want to add permissions to commands

- Read the official docs first:
	1. `Commands`
	2. `Permissions`
- Then read local assets:
	- `../assets/development/permissions/README.md`
	- `../assets/development/commands/command-attribute-template.cs.md`
- Common pitfalls:
	- Only restricting the UI without a real permission check
	- Leaving wildcard / sub-permission relationships unsorted

### I Want to Write Menus

#### 1) I want menu entries / submenus / save flows

- Read the official docs first:
	1. `Menus`
	2. `Thread Safety`
- Then read local assets:
	- `../assets/development/menus/menu-template.cs.md`
	- `../assets/development/thread-safety/thread-sensitivity-checklist.md`
- Common APIs / keywords:
	- `IMenuManagerAPI`
	- `ButtonMenuOption`
	- `ToggleMenuOption`
	- `ChoiceMenuOption`
	- `SubmenuMenuOption`
- Common pitfalls:
	- Blocking on IO directly in callbacks
	- Not revalidating the player after crossing `await`
	- Storing state in the menu instead of runtime / services

#### 2) I want BindingText dynamic text

- Read the official docs first:
	1. `Menus`
	2. `HTML Styling` (if the text involves HTML)
- Then read local assets:
	- `../assets/development/menus/menu-template.cs.md`
	- `../assets/guides/html-styling/README.md`
- Common pitfalls:
	- Manually refreshing `Text` instead of binding
	- Stuffing heavy computation / IO into binding evaluation

### I Want Custom HUD

#### 1) I want to show players a custom HUD with server-driven state updates

- Read the official docs first:
	1. `Custom HUD`
	2. `Thread Safety`
	3. `Entity`
- Then read local references:
	- `./swiftlys2-custom-hud.md`
- Common APIs / keywords:
	- `CCSCustomHudLayout`
	- `SetDialogVariableString(ForPlayer)` / `RemoveDialogVariableStringForPlayer`
	- `SetHasClass(ForPlayer)` / `EHudPanelClassStatus_t`
	- `StrLayout` / `StrLayoutUpdated`
- Common pitfalls:
	- Writing all variables in full every tick with no dirty checks
	- Calling thread-unsafe setters directly from background tasks (use the `Async` variants)
	- Assuming `GetDialogVariableStringForPlayer` falls back to the global value
	- Not cleaning up entities on map / plugin unload; mismatched subscribe / unsubscribe for click events

#### 2) I want clickable buttons inside Custom HUD

- Read the official docs first:
	1. `Custom HUD` (Input Capture / Handling Button Clicks)
- Then read local references:
	- `./swiftlys2-custom-hud.md`
- Common APIs / keywords:
	- `SetInputCaptureEnabled(ForPlayer)`
	- `Core.Event.OnCustomHudClicked`
	- `IOnCustomHudClickedEvent` (`PlayerId` / `ButtonId` / `CustomHudLayout`)
- Common pitfalls:
	- Handling a ButtonId without comparing the `CustomHudLayout` entity when multiple layouts exist
	- Forgetting to disable input capture after interaction, leaving the player cursor trapped

### I Want to Write Hooks

#### 1) I want typed GameHooks / high-frequency runtime hooks

- Read the official docs first:
	1. `GameHooks` API
	2. `Thread Safety`
	3. `Profiler`
- Then read local assets:
	- `./swiftlys2-performance-optimization-playbook.md`
	- `../assets/development/game-hooks/game-hooks-pre-post-guide.md`
	- `../assets/development/thread-safety/thread-sensitivity-checklist.md`
	- `../assets/development/profiler/hotpath-gc-checklist.md`
- Common pitfalls:
	- JSON / IO / high-frequency logging on hot paths
	- No player / pawn / fake-client filtering
	- Stuffing complex logic directly into hook callbacks
	- Letting `ref struct` contexts / usercmds / temporary wrappers escape the callback
	- Depending on cancellation semantics in Post

#### 2) I want generated Game Events

- Read the official docs first:
	1. `Game Events`
	2. `GameEventDefinitions` API
- Then read local assets:
	- `../assets/development/game-events/game-events-usage-notes.md`
- Common APIs / keywords:
	- `HookPre<T>` / `HookPost<T>`
	- `Unhook(Guid)`
	- `FireAsync<T>`
	- `DontBroadcast` / `Accessor`
- Common pitfalls:
	- Saving events / accessors into delayed or async callbacks
	- Treating unreliable Game Events as core lifecycle

#### 3) I want native function hooks / mid-hooks

- Read the official docs first:
	1. `Native Functions and Hooks`
	2. `Thread Safety`
- Then read local assets:
	- `./swiftlys2-performance-optimization-playbook.md`
	- `../assets/development/native-functions-and-hooks/hook-handler-template.cs.md`
- Common pitfalls:
	- Mismatched delegate prototypes
	- Not knowing the difference between `Call()` and `CallOriginal()`
	- Corrupting registers in mid-hooks

### I Want to Write NetMessages / Protobuf

#### 1) I want to send typed netmessages

- Read the official docs first:
	1. `Network Messages`
	2. `Thread Safety`
- Then read local assets:
	- `../assets/development/netmessages/protobuf-handler-template.cs.md`
- Common APIs / keywords:
	- `Core.NetMessage.Send<T>`
	- `Core.NetMessage.Create<T>`
	- `Recipients`
- Common pitfalls:
	- Forgetting to release reusable messages
	- Using magic numbers instead of typed APIs

#### 2) I want to hook client / server messages

- Read the official docs first:
	1. `Network Messages`
	2. `INetMessageService` in API Reference
- Then read local assets:
	- `../assets/development/netmessages/protobuf-handler-template.cs.md`
	- `../assets/development/thread-safety/thread-sensitivity-checklist.md`
- Common pitfalls:
	- Handing protobuf handles directly to background threads
	- Not distinguishing client-message hooks from server-message hooks

### I Want to Write Shared APIs

#### 1) I want to provide a shared interface

- Read the official docs first:
	1. `Shared API`
	2. `Dependency Injection`
- Then read local assets:
	- `../assets/development/shared-api/shared-interface-template.cs.md`
	- `../assets/guides/dependency-injection/di-service-plugin-template.cs.md`
- Common pitfalls:
	- Skipping the contracts DLL
	- Overly vague key naming
	- No versioning considered

#### 2) I want to consume a shared interface

- Read the official docs first:
	1. `Shared API`
- Then read local assets:
	- `../assets/development/shared-api/shared-interface-template.cs.md`
- Common pitfalls:
	- Not using `TryGetSharedInterface(...)` for optional dependencies
	- Assuming the interface already exists before the provider loads
	- Holding stale interface references after unload

### I Want to Write Schedulers / Workers / Background Tasks

#### 1) I need to decide between Scheduler and background workers

- Read the official docs first:
	1. `Scheduler`
	2. `Thread Safety`
- Then read local assets:
	- `./swiftlys2-performance-optimization-playbook.md`
	- `../assets/development/scheduler/scheduler-vs-worker-guide.md`
	- `../assets/patterns/background-workers/worker-template.cs.md`
	- `../assets/development/core-events/lifecycle-checklist.md`
- Common pitfalls:
	- Treating a background worker as a Scheduler
	- Accessing main-thread-sensitive APIs directly from worker threads
	- Missing stop / flush / cancel closure

### I Want Databases, Sound, Steamworks, Memory, or Server Runtime Configuration

| Scenario | Read the official docs first | Then read local assets |
| --- | --- | --- |
| Plugin DB connections with ADO.NET / ORM | `Database` | `../assets/development/database/database-connection-template.cs.md` |
| Entity key-values before spawn | `Entity Key Values` | `../assets/development/entity/entity-key-values-guide.md` |
| Custom sounds with recipients | `Sound Events` + `Thread Safety` | `../assets/development/sound-events/sound-event-guide.md` |
| Steam server / Workshop / auth callbacks | `Steamworks` | `../assets/development/steamworks/steamworks-server-guide.md` |
| Signatures / vtables / xrefs / allocation | `Memory` API | `../assets/development/memory/memory-service-guide.md` |
| Startup args, core config, command permission overrides, console filters | `Resources` | `../assets/resources/runtime-configuration-guide.md` |
| CSS migration | `Porting from CounterStrikeSharp` | `../assets/guides/porting-from-css/porting-checklist.md` |

## 7. Recommended Search Keywords

### Lifecycle

- `OnClientPutInServer`
- `OnClientDisconnected`
- `OnMapLoad`
- `OnMapUnload`

### Commands

- `ICommandContext`
- `Command`
- `CommandAlias`
- `Reply`

### Hooks / Movement

- `Core.GameHooks`
- `ProcessUsercmdsPreContext` / `ProcessUsercmdsPostContext`
- `RunCommandMovementPreContext` / `RunCommandMovementPostContext`
- `TakeDamageEntityPreContext`
- `GameHookHandler`
- `MidHookContext`

### Performance / GC

- `AggressiveInlining`
- `stackalloc`
- `Span`
- `StringBuilder`
- `PeriodicTimer`
- `Generation`
- `Backpressure`
- `StructLayout`

### NetMessages / Protobuf

- `INetMessageService`
- `ITypedProtobuf`
- `IProtobufAccessor`

### Shared API

- `IInterfaceManager`
- `ConfigureSharedInterface`
- `UseSharedInterface`
- `HasSharedInterface`
- `TryGetSharedInterface`
- `OnSharedInterfaceInjected`

### Database / Sound / Steam / Memory

- `IDatabaseService` / `GetConnectionInfo`
- `SoundEvent` / `EmitAsync`
- `SteamGameServerUGC` / `Callback<T>` / `CallResult<T>`
- `IMemoryService` / `GetAddressBySignature` / `GetUnmanagedFunctionByAddress`

### Schema / Entity

- `IEntitySystemService`
- `AcceptInput`
- `DispatchSpawn`
- `Despawn`
- `Updated`

### Menus

- `IMenuAPI`
- `IMenuOption`
- `ButtonMenuOption`
- `ToggleMenuOption`
- `SliderMenuOption`
- `SubmenuMenuOption`
- `BindingText`

### Custom HUD

- `CCSCustomHudLayout`
- `EHudPanelClassStatus_t`
- `IOnCustomHudClickedEvent`
- `SetDialogVariableStringForPlayer`
- `SetHasClassForPlayer`
- `SetInputCaptureEnabledForPlayer`

## 8. Usage Guidance

- **Pick the scenario first, then the source.**
- **Check the official site and mdwiki first, then decide whether current-workspace supplements are needed.**
- **Enter official details via `swiftlys2-official-docs-map.md` first, then drill down online to specific pages as needed.**
- **Enter local templates and checklists via `../assets/README.md` first. Do not guess filenames directly.**
- **Public docs own API and framework boundaries; the workspace knowledge base owns current-workspace experience.**

## See Also

- [kb-docs-map](kb-docs-map.md)
- [kb-asset-inventory](kb-asset-inventory.md)
- [kb-capability-map](kb-capability-map.md)
