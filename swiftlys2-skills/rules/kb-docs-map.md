# kb-docs-map

> Lean navigation map for the official SwiftlyS2 docs

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-official-docs-map.md — body verbatim, header only added -->

This file organizes `https://swiftlys2.net/docs/` into a **public navigation suitable for fast agent retrieval and follow-up online drilling**.

Its goal is not to copy the official site's full text into the toolkit, but to:

- Keep stable entries
- Distill "what this page is for" per page
- Pre-compress the engineering semantics most critical to SwiftlyS2 plugin development
- Avoid bloating the toolkit by stuffing in the full API Reference

## Usage Rules

- **Installation**: `https://swiftlys2.net/docs/installation/`; keep the entry, but this toolkit does not extract its body text.
- **Read priority**: prefer this navigation, targeted SwiftlyS2 official pages, and `sw2-mdwiki` first; treat `https://swiftlys2.net/llms-full.txt` only as a last-resort full-text source.
- **API Reference**: keep only the lean navigation plus retrieval guidance; when detailed APIs are needed, agents drill online into `https://swiftlys2.net/docs/api/` themselves. Only when targeted pages plus existing indexes are still insufficient may the official full LLM document be used for local full-text search, and only after user approval.
- **Development Flow**: the current official page is still a `todo` placeholder and must not be treated as reliable engineering guidance.
- **Full LLM document**: `https://swiftlys2.net/llms-full.txt` contains the full official content, but because it is **unindexed and expensive to scan**, it is only suitable for local lookup and keyword search after user approval.
- **Current snapshot comparison**: this toolkit's `./swiftlys2-current-capability-map.md` records the official pages covered in this pass, dynamic API boundaries, and snapshot provenance.

## Docs Root

- Root entry: `https://swiftlys2.net/docs/`
- Homepage scope: introduces SwiftlyS2 as a Metamod:Source-based CS2 server plugin framework, highlighting Commands, Convars, Entity System, Events, GameEvents, Memory, Menus, Hooks, NetMessages, Profiler, Scheduler, Schemas, Sounds, and similar capabilities.
- Homepage use: suitable as a **capability overview and section entry**, not as a detail reference.

## Development Section Navigation

### 1. Getting Started

- Address: `https://swiftlys2.net/docs/development/getting-started/`
- Scope: new-plugin onboarding, template installation, publishing flow entry.
- Key points:
  - Requires `.NET 10.0 SDK`
  - Create the plugin template via `SwiftlyS2.CS2.PluginTemplate`
  - Template versions may lag; manually update `PackageReference` as needed
  - Published output lands in `build/publish`
  - The official docs explicitly recommend reading `Dependency Injection` before writing real code
- Suitable for: creating new plugins, checking template project structure, confirming the base publish flow.

### 2. Swiftly Core

- Address: `https://swiftlys2.net/docs/development/swiftly-core/`
- Scope: `ISwiftlyCore` root entry documentation.
- Key points:
  - `ISwiftlyCore` is the framework's central singleton
  - Aggregates Event, Engine, GameEvent, GameHooks, NetMessage, Helpers, Game, Command, EntitySystem, ConVar, Configuration, GameData, PlayerManager, Memory, Profiler, Trace, Scheduler, Database, Translation, Permission, Registrator, MenusAPI, PluginManager, and other services
  - Officially recommended to share `ISwiftlyCore` via dependency injection
  - Closely tied to plugin lifecycle and hot reload
- Suitable for: sorting out service boundaries, looking up core service entries, designing DI architecture.

### 3. Using Attributes

- Address: `https://swiftlys2.net/docs/development/using-attributes/`
- Scope: explains the applicability boundaries of the attribute-registration mechanism.
- Key points:
  - Attributes work directly only inside the main class inheriting `BasePlugin` by default
  - When attributes are used in other classes, call `Core.Registrator.Register(this)` first
- Suitable for: explaining why `[Command]` or event attributes in services / modules have no effect.

### 4. Thread Safety

- Address: `https://swiftlys2.net/docs/development/thread-safety/`
- Scope: main-thread-sensitive API inventory.
- Key points:
  - Calling thread-unsafe APIs off the main thread may crash directly
  - API Reference marks synchronously dangerous calls with `[ThreadUnsafe]`; prefer awaiting the matching Async API
  - Async variants normally execute directly on the main thread and schedule safely off it, but the current signature still wins for each API
  - Explicitly listed main-thread-sensitive calls:
    - `IPlayer.Send* / Kick / ChangeTeam / SwitchTeam / TakeDamage / Teleport / ExecuteCommand`
    - `IGameEventService.Fire*`
    - `IEngineService.ExecuteCommand*`
    - `CEntityInstance.AcceptInput / AddEntityIOEvent / DispatchSpawn / Despawn`
    - `IPlayerManagerService.Send*`
    - `ICommandContext.Reply`
    - `CBaseModelEntity.SetModel / SetBodygroupByName`
    - `IEngineService.DispatchParticleEffect`
    - `CCSPlayerController.Respawn`
    - `Projectile.EmitGrenade`
    - `CPlayer_ItemServices.* / CPlayer_WeaponServices.*`
- Suitable for: auditing async tasks, menu callbacks, background workers, hook hot-path write-backs.

### 5. Commands

- Address: `https://swiftlys2.net/docs/development/commands/`
- Scope: commands, command aliases, client command / chat hooks.
- Key points:
  - Available via `[Command]` or `Core.Command.RegisterCommand`
  - Available via `[CommandAlias]` or `Core.Command.RegisterCommandAlias`
  - `registerRaw` controls whether the `sw_` prefix is skipped
  - Built-in permission parameter supported
  - `ICommandContext.Args` is `string[]`; current command metadata supports `helpText`
  - `registerRaw` only controls the `sw_` prefix; client-command hooks do not depend on it
  - Client command / chat hooks both return `HookResult`
  - Automatically cleaned up on unload, with manual `Unregister` / `Unhook` also supported
- Suitable for: command-system design, chat interception, client-command filtering.

### 6. Configuration

- Address: `https://swiftlys2.net/docs/development/configuration/`
- Scope: plugin configuration init, loading, hot reload.
- Key points:
  - Entry is `Core.Configuration`
  - Config files can be initialized from templates
  - `InitializeJsonWithModel<T>` / `InitializeTomlWithModel<T>` generate default configs from C# models
  - `Configure(builder => ...)` can append `json / jsonc / toml` config sources
  - Recommended with `IOptionsMonitor<T>` plus `reloadOnChange`
  - Fluent method chaining supported
  - Supports `BasePath` / `BasePathExists` / `GetConfigPath` plus model / template initialization that only runs on first creation
- Suitable for: config-model design, hot reload, DI + Options patterns.

### 7. Translations

- Address: `https://swiftlys2.net/docs/development/translations/`
- Scope: translation-resource organization and localized reads.
- Key points:
  - Translation files live in `resources/translations/*.jsonc`
  - Named with language codes such as `en.jsonc`, `zh-CN.jsonc`
  - Common entry: `Core.Translation.GetPlayerLocalizer(player)`
  - `Core.Localizer` is for server / default lookup; custom language codes are not auto-resolved by player localizers
  - Parameterized placeholders `{0}`, `{1}` supported
  - Missing keys return the key itself by default
  - Always ship `en.jsonc` as the fallback
  - Recommended unified key naming: `category.subcategory.key`
- Suitable for: player-localized messages, command prompts, menu-text internationalization.

### 8. Entity

- Address: `https://swiftlys2.net/docs/development/entity/`
- Scope: entity creation, queries, handle safety.
- Key points:
  - Create via `Core.EntitySystem.CreateEntity<T>()` or by designer name
  - Can enumerate all entities or filter by class
  - The official docs explicitly stress: **holding raw entities long-term is very dangerous**
  - Long-term tracking should use `CHandle<T>` / `GetRefEHandle(entity)`
  - `handle.Value` may be null; check `handle.IsValid` first
- Suitable for: cross-frame entity tracking, preview entities, beams / world text, entity references in delayed tasks.

### 9. Entity Key Values

- Address: `https://swiftlys2.net/docs/development/entitykeyvalues/`
- Scope: type-safe key-value writes via `CEntityKeyValues`.
- Key points:
  - `CEntityKeyValues` implements `IDisposable`
  - Provides `SetBool / SetInt32 / SetUInt32 / SetInt64 / SetFloat / SetString / ...`
  - Also supports generic `Set<T>` and `Get<T>` access
  - Unsupported types throw `InvalidOperationException`
- Suitable for: building entity key-values, configuring entity properties before spawn.

### 10. Game Events

- Address: `https://swiftlys2.net/docs/development/game-events/`
- Scope: Game Event firing and hooking.
- Key points:
  - Available via `Core.GameEvent.Fire<T>`, `FireToPlayer`
  - Use `FireAsync*` off the main thread
  - Supports `HookPre<T>` / `HookPost<T>`
  - Dynamic hooks return a `Guid` cleanable via `Unhook(Guid)` or type-wide unhook
  - `@event` is a transient object for the current tick and must not be held long-term
  - The official docs specifically warn: **many game events are effectively deprecated in Source 2 and some do not work**
- Suitable for: use only when the matching Game Event exists and is verified working; never blindly trust every event to be reliable.

### 11. Core Events

- Address: `https://swiftlys2.net/docs/development/core-events/`
- Scope: SwiftlyS2's own typed core-listener system.
- Key points:
  - Core events are not game events
  - Listeners are destroyed on hot reload / unload
  - `+=` / `-=` suit dynamic early subscribe / unsubscribe
  - Legacy entity / movement / controller / pawn / weapon Core `On*Hook` entries should migrate to `Core.GameHooks`
  - Each event's parameter types carry field information
  - See `EventDelegates` for the full event list
- Suitable for: map, player, entity, tick, hook-callback, and other lifecycle listeners.

### GameHooks API (Current Typed-Hook Surface)

- Address: `https://swiftlys2.net/docs/api/gamehooks/`
- Scope: typed Pre / Post hooks for controller, entities, items, movement, pawn, weapons under `Core.GameHooks`.
- Key points:
  - Hooks expose `Pre` / `Post` events with callbacks taking `ref XxxPreContext` / `ref XxxPostContext`.
  - Contexts are `ref struct` and must not be stored across callbacks, awaits, schedulers, or closures.
  - Pre controls the original call via `ctx.SetHookResult(...)`; `Handled` / `Stop` have no effect in Post.
  - Several legacy Core `On*Hook` entries are marked obsolete; see this toolkit's `assets/development/game-hooks/game-hooks-pre-post-guide.md` for the migration map.
- Suitable for: current typed native hooks for usercmd, touch, damage, movement, item, pawn, weapon.

### 12. Network Messages

- Address: `https://swiftlys2.net/docs/development/netmessages/`
- Scope: typed-protobuf net-message sending and hooking.
- Key points:
  - Net messages are protobuf + message-ID based
  - Can be sent directly via `Core.NetMessage.Send<T>`
  - For high-frequency reuse, `Create<T>()` once, reuse, and release with `using`
  - Supports client / server / internal-server message hooks plus matching unhooks
  - Callback messages and accessors are transient wrappers; copy them out inside the callback only
  - See `ProtobufDefinitions` and `INetMessageService` for detailed types
- Suitable for: Shake, sounds, HUD, client / server net-message interception and sending.

### 13. Menus

- Address: `https://swiftlys2.net/docs/development/menus/`
- Scope: complete menu system.
- Key points:
  - Current entry is `Core.MenusAPI` / `IMenuManagerAPI`
  - Builder fluent API supported
  - Built-in option types: `Button / Toggle / Slider / Choice / Text / Input / ProgressBar / Submenu`
  - Hierarchical menus, dynamic content, global events, per-player validation and formatting supported
  - `BeforeFormat` / `AfterFormat` / `Validating` / `Click` / `ValueChanged` supported
  - Scrolling styles, key overrides, player freezing, auto-close, and similar behaviors supported
- Suitable for: interactive menus, dynamic HUD menus, permission-aware menus.

### 14. Convars

- Address: `https://swiftlys2.net/docs/development/convars/`
- Scope: ConVar creation, lookup, replication to clients, client queries.
- Key points:
  - `Core.ConVar.Create<T>()` / `Find<T>()`
  - `CreateOrFind<T>()` can reuse same-named entries; unknown types can use `FindAsString`
  - Assigning `.Value` enters an internal event queue and may not take effect immediately
  - For temporary immediate changes, prefer `.SetInternal(T value)`
  - `ReplicateToClient`, `QueryClient` supported
  - `TryGetMinValue` / `TryGetMaxValue` / `TryGetDefaultValue` suit safe range reads on existing entries
  - Flag add / remove / read / write supported
- Suitable for: temporarily toggling cvars, reading game convars, client-convar queries.

### 15. Native Functions and Hooks

- Address: `https://swiftlys2.net/docs/development/native-functions-and-hooks/`
- Scope: signatures, addresses, delegates, function hooks, mid-hooks.
- Key points:
  - Resolve signatures from gamedata, then resolve addresses
  - Delegate prototypes must match native signatures exactly
  - `Call()` goes through the currently possibly-hooked address; `CallOriginal()` takes the original path
  - When a typed hook already exists, prefer `Core.GameHooks`; raw hooks use exact delegates + `AddHook(next => ...)`
  - Function hooks and mid-hook address hooks supported
  - Mid-hooks can read / write registers, but wrong edits crash the server directly
  - All hooks must be uninstalled in pairs; the framework cleans up automatically on plugin unload
- Suitable for: advanced native calls, vtable functions, Detour / MidHook-level extensions.

### 16. Scheduler

- Address: `https://swiftlys2.net/docs/development/scheduler/`
- Scope: NextTick and tick-based timers.
- Key points:
  - `NextTick` schedules onto the next tick
  - `Delay / Repeat / DelayAndRepeat` are in **game ticks** by default
  - Second-based callers must use the `*BySeconds` variants
  - Returns a `CancellationTokenSource` for cancellation
  - `StopOnMapChange(token)` auto-cancels on map change
  - `Repeat*` executes immediately the first time; do not pass async callbacks to NextTick / NextWorldUpdate — the related overloads are obsolete / unsafe
  - `AddTimer` can dynamically decide the next step via `TimerStep.Spin / Wait / Stop`
- Suitable for: main-thread delays, small periodic tasks, automatic cleanup on map switches.

### 17. Shared API

- Address: `https://swiftlys2.net/docs/development/shared-api/`
- Scope: shared interfaces between plugins.
- Key points:
  - Provide interfaces via `ConfigureSharedInterface`
  - Consume interfaces via `UseSharedInterface`
  - React to re-injection via `OnSharedInterfaceInjected`
  - Interfaces belong in a separate contracts DLL shared by providers / consumers
  - Recommended to let interfaces inherit `IDisposable`
  - Keys need explicit naming plus versioning thought
  - Optional dependencies should prefer `TryGetSharedInterface`
- Suitable for: cross-plugin shared services, exposing points / permission / economy systems.

### 18. Permissions

- Address: `https://swiftlys2.net/docs/development/permissions/`
- Scope: permission checks, groups, sub-permissions.
- Key points:
  - `Core.Permission.PlayerHasPermission(steamId, permission)`
  - `PlayerHasPermissions` is an all-of check; `GetPlayerPermissions` shows effective permissions including inheritance
  - Wildcard `*` supported
  - Supports `AddPermission` / `RemovePermission` / `ClearPermissions`; do not add calls to the deprecated `ClearPermission`
  - `permissions.jsonc` supports player groups plus `__default`
  - Supports `AddSubPermission(parent, child)` / `RemoveSubPermission(...)` to form and revoke permission hierarchies
  - Recommended naming: `plugin.category.action`
- Suitable for: command permissions, menu visibility, module access control.

### 19. Profiler

- Address: `https://swiftlys2.net/docs/development/profiler/`
- Scope: performance measurement and naming conventions.
- Key points:
  - `StartRecording` / `StopRecording`
  - `RecordTime` can also record microsecond values manually
  - Hierarchical names recommended, e.g. `Database.Players.Load`
- Suitable for: hot-path performance sampling, staged timing of complex flows.

### 20. Database

- Address: `https://swiftlys2.net/docs/development/database/`
- Scope: unified database-connection config entry.
- Key points:
  - `Core.Database.GetConnection(key)` reads the SwiftlyS2-global `configs/database.jsonc`
  - Falls back to the default connection when the key is missing
  - Use `GetConnectionString` / `GetConnectionInfo` to diagnose connections; never log passwords / raw URIs
  - Officially recommended to use ORM / ADO.NET tooling such as Dapper, FreeSql, EF Core
- Suitable for: plugin database access, global connection reuse.

### 21. Sound Events

- Address: `https://swiftlys2.net/docs/development/soundevents/`
- Scope: sound-event creation and emission.
- Key points:
  - `SoundEvent` needs `using` / dispose
  - Recipients must be added before sending
  - `Name / Volume / Pitch / SourceEntityIndex` can be set
  - Position plus various field parameters can be attached
  - Use `Emit()` on the main thread, `await EmitAsync()` off it
- Suitable for: custom notification sounds, weapon sounds, ambient broadcasts.

### 22. Steamworks

- Address: `https://swiftlys2.net/docs/development/steamworks/`
- Scope: trimmed Steamworks.NET (game-server side) integration.
- Key points:
  - Consume via `using SwiftlyS2.Shared.SteamAPI;`
  - Covers Steam IDs, auth, server info, Workshop downloads, callback handling, etc.
  - Callback references must be kept alive to avoid GC collection
  - `Callback<T>` / `CallResult<T>` are held by the plugin / service and disposed on unload
  - Establish Steam-API-dependent init through `OnSteamAPIActivated`
  - Workshop uses `SteamGameServerUGC`; do not add calls to deprecated connect / disconnect auth APIs
  - Full `SteamAPI` signatures are in API Reference
- Suitable for: ownership checks, Workshop downloads, server-info reporting.

### 23. Custom HUD

- Address: `https://swiftlys2.net/docs/development/custom-hud/`
- Scope: per-player custom HUD via the `custom_hud_layout` entity (Panorama XML / CSS UI + server-side state updates).
- Key points:
  - Entity creation: `CreateEntity<CCSCustomHudLayout>` → `StrLayout` → `StrLayoutUpdated()` → `DispatchSpawn()`
  - Dynamic strings: `Set / Get / RemoveDialogVariableString(ForPlayer)`; per-player override reads never fall back to global values
  - Dynamic CSS classes: `Set / GetHasClass(ForPlayer)` + `EHudPanelClassStatus_t` (HasClass / DoesNotHaveClass / Undefined)
  - Input capture: `SetInputCaptureEnabled(ForPlayer)`; button clicks flow through `Core.Event.OnCustomHudClicked` (`IOnCustomHudClickedEvent`: PlayerId / ButtonId / CustomHudLayout)
  - State-mutating methods are thread-unsafe; background tasks use the `Async` variants; getters stay synchronous
  - Officially marked new and unstable; Valve may introduce breaking changes
- Local reference: `swiftlys2-custom-hud.md`
- Suitable for: player HUD state updates, in-HUD interactive buttons, per-player differentiated display.

## Guides Section Navigation

### 1. Dependency Injection

- Address: `https://swiftlys2.net/docs/guides/dependency-injection/`
- Scope: SwiftlyS2's officially recommended design pattern.
- Key points:
  - Recommended `ServiceCollection().AddSwiftly(Core)`
  - Common injectables: `ISwiftlyCore`, `ILogger<T>`, `IOptionsMonitor<T>`
  - When attributes are used inside services, register the object explicitly
- Suitable for: new-plugin architecture, service layering, Options patterns.

### 2. Development Flow

- Address: `https://swiftlys2.net/docs/guides/development-flow/`
- Current state: the official body text is still `todo`
- Usage guidance: keep the entry, but **do not treat this page as authoritative**.

### 3. Chat & CenterHTML Styling

- Address: `https://swiftlys2.net/docs/guides/chat-and-html-styling/`
- Scope: Panorama UI HTML styling guide.
- Key points:
  - Officially listed usable tags: `div`, `span`, `p`, `a`, `img`, `br`, `hr`, `h1-h6`, `strong`, `em`, `b`, `i`, `u`, `pre`
  - Styling is not standard `style="..."` but direct attributes such as `color="red"`
  - Prefer built-in classes such as `fontSize-l`, `fontSize-xl`, `fontWeight-bold`, `CriticalText`
  - `class` and `color` can be combined for "dynamic color + fixed size / weight" patterns
  - Official examples cover ready counts, countdowns, progress bars, score displays, multi-line rules explanations, and other notification-style UIs
  - Complex layouts, deep nesting, and unusual classes must all be tested in-game
  - The official docs also give a SteamDatabase Panorama-styles reference entry for further lookup in `panorama_base.css`, `gamestyles.css`, and similar files
- Suitable for: `SendCenterHTML`, center notifications, menu formatting, rich-text UI scenarios such as `BindingText` / `BeforeFormat` / `AfterFormat`.
- Detailed toolkit notes: `../assets/guides/html-styling/README.md`

### 4. Porting from CounterStrikeSharp

- Address: `https://swiftlys2.net/docs/guides/porting-from-css/`
- Scope: systematic guide for migrating from CounterStrikeSharp to SwiftlyS2.
- Key points:
  - Compares .csproj, events, commands, menus, configs, databases, ConVars, listeners, GameData hooks, migration order
  - Stresses SwiftlyS2 uses `.NET 10`
  - Stresses `Updated()` instead of CSS `SetStateChanged`
  - Gives replacement thinking from utility classes to `Core.*` services
- Toolkit migration checklist: `../assets/guides/porting-from-css/porting-checklist.md`
- Suitable for: historical repository migration, aligning CSS semantics, structuring migration plans.

### 5. Terminologies

- Address: `https://swiftlys2.net/docs/guides/terminologies/`
- Scope: unifies managed / native / controller / pawn / player-object / handle concepts.
- Key points:
  - Explains the managed vs native boundary
  - Distinguishes controller, pawn, slot / playerId, player objects
  - Explains entity index ranges and handle concepts
  - Distinguishes temporary / permanent entities
- Suitable for: terminology alignment, reducing conceptual confusion in migration and audits.

## Resources Section Navigation

- Resources Root: `https://swiftlys2.net/docs/resources/`
- CLI Options: `https://swiftlys2.net/docs/resources/cli-options/`, for `-sw_path`, `-sw_logpath`, console-log visibility and levels.
- Core Configuration: `https://swiftlys2.net/docs/resources/core-configuration/`, for `core.jsonc` framework-level command, plugin, menu, language, filter, and Steam-auth behavior.
- Command Overrides: `https://swiftlys2.net/docs/resources/command-overrides/`, for command-permission remapping without changing plugin code.
- Console Filter: `https://swiftlys2.net/docs/resources/console-filter/`, for filtering confirmed noise plus reload / status operations.
- Local operations boundary: `../assets/resources/runtime-configuration-guide.md`.

## API Reference Lean Navigation

### Root Entry

- API Root: `https://swiftlys2.net/docs/api/`

### Core Entries Given on the Official Homepage

- Core Object: `https://swiftlys2.net/docs/api/iswiftlycore/`
- Game Events: `https://swiftlys2.net/docs/api/gameevents/`
- Core Listeners: `https://swiftlys2.net/docs/api/events/`
- SteamWorks API: `https://swiftlys2.net/docs/api/steamapi/`
- Commands: `https://swiftlys2.net/docs/api/commands/`
- GameHooks: `https://swiftlys2.net/docs/api/gamehooks/`

### High-Value Categories Visible in the Homepage Sidebar

- Memory: `https://swiftlys2.net/docs/api/memory/`
- CommandLine: `https://swiftlys2.net/docs/api/commandline/`
- Convars: `https://swiftlys2.net/docs/api/convars/`
- Database: `https://swiftlys2.net/docs/api/database/`
- Engine: `https://swiftlys2.net/docs/api/engine/`
- EntitySystem: `https://swiftlys2.net/docs/api/entitysystem/`
- GameEventDefinitions: `https://swiftlys2.net/docs/api/gameeventdefinitions/`
- GameHooks: `https://swiftlys2.net/docs/api/gamehooks/`
- Menus: `https://swiftlys2.net/docs/api/menus/`
- Natives: `https://swiftlys2.net/docs/api/natives/`
- NetMessages: `https://swiftlys2.net/docs/api/netmessages/`
- Permissions: `https://swiftlys2.net/docs/api/permissions/`
- Players: `https://swiftlys2.net/docs/api/players/`
- Plugins: `https://swiftlys2.net/docs/api/plugins/`
- ProtobufDefinitions: `https://swiftlys2.net/docs/api/protobufdefinitions/`
- Scheduler: `https://swiftlys2.net/docs/api/scheduler/`
- SchemaDefinitions: `https://swiftlys2.net/docs/api/schemadefinitions/`
- Schemas: `https://swiftlys2.net/docs/api/schemas/`
- Services: `https://swiftlys2.net/docs/api/services/`
- Sounds: `https://swiftlys2.net/docs/api/sounds/`
- SteamAPI: `https://swiftlys2.net/docs/api/steamapi/`
- Trace: `https://swiftlys2.net/docs/api/trace/`
- StringTable: `https://swiftlys2.net/docs/api/stringtable/`
- Translation: `https://swiftlys2.net/docs/api/translation/`
- Helper: `https://swiftlys2.net/docs/api/helper/`
- Helpers: `https://swiftlys2.net/docs/api/helpers/`
- Misc: `https://swiftlys2.net/docs/api/misc/`

### Recommended Online Retrieval Flow

When the toolkit summaries are insufficient, drill online in this order:

1. Determine the owning section first: e.g. `Commands`, `Menus`, `NetMessages`, `Schemas`
2. Open the matching API category homepage first instead of searching the whole site randomly
3. Then enter the concrete interface, e.g.:
   - `ICommandService`
   - `ICommandContext`
   - `INetMessageService`
   - `IEntitySystemService`
   - `ISchedulerService`
   - `IInterfaceManager`
   - `IPermissionManager`
4. For generated types (protobuf, schema definitions, game events), keep drilling down from the category page

## Recommended Reading Paths

### New Plugins

1. `Getting Started`
2. `Dependency Injection`
3. `Swiftly Core`
4. `Thread Safety`
5. Matching subsystem pages (Commands / Menus / Configuration / Translations ...)

### Auditing Existing Plugins

1. `Thread Safety`
2. `Core Events`
3. `Entity`
4. `Scheduler`
5. `Profiler`
6. Matching subsystem pages

### Cross-Plugin Sharing

1. `Shared API`
2. `Dependency Injection`
3. `Permissions`
4. `IInterfaceManager` in API Reference

### UI / Menus / HUD

1. `Menus`
2. `HTML Styling`
3. `Translations`
4. `NetMessages`

### Migration

1. `Terminologies`
2. `Porting from CounterStrikeSharp`
3. `Dependency Injection`
4. `Thread Safety`
5. Matching legacy feature-module pages

## See Also

- [kb-index](kb-index.md)
- [kb-asset-inventory](kb-asset-inventory.md)
- [kb-capability-map](kb-capability-map.md)
