# playbook-plugin-playbook

> SwiftlyS2 plugin architecture, lifecycle, thread and state rules

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-plugin-playbook.md — body verbatim, header only added -->

This manual is the core engineering reference for `swiftlys2-toolkit`, narrowing down the **publicly reusable** SwiftlyS2 development methodology.

Default public evidence comes from:

- SwiftlyS2 official documentation: `https://swiftlys2.net/docs/`
- This toolkit's condensed official navigation: `./swiftlys2-official-docs-map.md`
- sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
- SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`

If a workspace also owns local reference repositories, current project maps, historical reference projects, or specialized experience, register them in the nearest-level `AGENTS.md` or in a project-local skill it explicitly references. Do not turn them into permanent hard dependencies here.

## 1. Three Common Architectures

### A. Modular Gameplay Plugin

Suitable when:

- A single plugin contains substantial gameplay logic
- It needs `Commands / Events / Hooks / Modules / Workers / Models`
- It needs player runtime state, state synchronization, and persistence working together

Typical characteristics:

- The plugin main class is usually split into partials
- Command, event, and hook entry points are layered separately from business modules
- Heavy computation and background write-backs are moved into workers
- Player runtime state has one unified state object instead of mirrored copies scattered around

### B. DI / Service-Oriented Plugin

Suitable when:

- The plugin is medium or large
- It needs interface → implementation layering
- It needs explicit install / uninstall / initialize / cleanup lifecycles

Typical characteristics:

- Uses `ServiceCollection` with `AddSwiftly(Core)`
- The root is responsible for composition
- Services own their listeners, command registrations, conditional hooks, and uninstall closure

### C. Hybrid Architecture

Suitable when:

- The core is closer to a modular gameplay plugin
- But some subsystems fit services better
- A small number of installable / uninstallable DI / service capabilities must be embedded into the modular core

## 2. Main-Thread and Async Boundaries

Per the official `Thread Safety` documentation, the following operations are main-thread-sensitive by default:

- `IPlayer` message, control, movement, and entity-related calls
- `ICommandContext.Reply`
- `IGameEventService.Fire*`
- `IEngineService.ExecuteCommand*`
- `CEntityInstance.AcceptInput / DispatchSpawn / Despawn`
- `CBaseModelEntity.SetModel / SetBodygroupByName`
- `CCSPlayerController.Respawn`
- `CPlayer_ItemServices.*`
- `CPlayer_WeaponServices.*`

### Engineering Rules for Main-Thread / Async Boundaries

1. **Writing game state, entities, Schemas, or protobufs: return to the main thread by default.**
2. **Background threads are mainly for computation, encoding, disk IO, network IO, and batching.**
3. **In async contexts, prefer the `Async` API.**
4. **Never bring `.Wait()`, `.Result`, synchronous joins, or blocking IO onto the main thread.**
5. **Run JSON encode / decode in the background by default, not in hooks / RuntimeLoops / menu callbacks.**

## 3. Lifecycle Closure

Every SwiftlyS2 plugin change must explicitly check at minimum:

- map load / unload
- player connect / disconnect
- start / stop of long-lived subsystems
- worker start / stop / flush / cancel

### Additional Rules

- Delayed or async logic must not trust a stale `IPlayer` by default
- Map-level caches must be cleaned up explicitly in the map lifecycle
- Bidirectional maps across objects / sessions must be unbound atomically on shutdown

## 4. IPlayer and Bot / Fake-Client Identity

- Long-term identity for real human players normally uses a stable player identifier
- Bots / fake clients must not be assumed to support `SteamID`
- In practice, treat bot `SteamID` as fixed `0`. It cannot be used as a reliable lookup key.
- When bots and humans are stored together, prefer `SessionId` as the runtime lookup key
- Mixed storage must explicitly separate identity-key strategies for humans and bots. Do not apply the human long-term identity-key strategy directly to bots.
- Every delayed task must revalidate the player object when it executes

## 5. Long-Lived Entity Tracking

- Across frames, delays, or maps, do not hold raw entity wrappers long-term
- Prefer stable-handle thinking
- Validate before access
- Be especially careful with delayed despawns, preview entities, beams / world text, and other scenarios exposed to entity-slot reuse

### `DispatchSpawn` / `SetModel` and the Staging List (EF_IN_STAGING_LIST)

The engine asserts in `CModelState::SetupModel()` that when `SetModel()` is called, the entity's **OwnerEntity must not be in the staging list** (the `EF_IN_STAGING_LIST` flag). Violating this assertion makes tier0 write `0xDEADBEEF` to a null pointer — an instant crash.

**Safe entity-creation order**:

```csharp
// ✅ Spawn first, then SetModel — after DispatchSpawn the entity leaves the staging list
var entity = Core.EntitySystem.CreateEntityByDesignerName<CBaseModelEntity>("prop_dynamic");
entity.DispatchSpawn();
entity.SetModel("path/to/model.vmdl");

// ❌ SetModel before Spawn — the entity is still in the staging list, assertion fails → crash
var entity = Core.EntitySystem.CreateEntityByDesignerName<CBaseModelEntity>("prop_dynamic");
entity.SetModel("path/to/model.vmdl"); // CRASH: EF_IN_STAGING_LIST
entity.DispatchSpawn();
```

**Trap when calling `SetModel` on an existing entity**:

If the target entity's OwnerEntity (e.g. a weapon's owner = pawn) happens to be flagged `EF_IN_STAGING_LIST` in the current frame (common right after `*Updated()` fires), calling `SetModel` on that entity triggers the same assertion. In that case defer `SetModel` to `NextWorldUpdate` and run it after the engine flushes the staging list:

```csharp
// ✅ Defer SetModel to the next frame to avoid the staging-list assertion
Core.Scheduler.NextWorldUpdate(() =>
{
    if (weapon.IsValid)
        weapon.SetModel(string.Empty);
});
```

### Skipping Pawn Schema Writes on Disconnect / Map Change

After a player disconnects or the map changes, the pawn is about to be destroyed by the engine. Schema writes to the pawn at that point (Render, Collision, ViewEntity, ActiveWeapon, etc.) plus `*Updated()` mark the pawn dirty, and the engine dereferences freed pawn memory when processing the dirty flags on the next tick → null-pointer crash.

Cleanup paths must distinguish "destructive cleanup" (Disconnect / MapUnload) from "normal cleanup" (death / exit / timeout); the former skips pawn writes.

### Entity Parent-Child Cleanup

If entities have `SetParent` / `FollowEntity` relationships, call `AcceptInput("ClearParent")` before Despawn to release the engine-side parent chain and prevent the engine from traversing a dangling parent pointer after Despawn.

## 6. Hook Hot Paths

Shared rules for high-frequency hooks:

1. Filter out irrelevant objects as early as possible
2. Avoid unnecessary allocations
3. Avoid JSON, IO, locks, and synchronous waits
4. Avoid high-frequency logging
5. Prefer producer / consumer separation
6. Keep the 64-tick frame budget in mind

### Hook Governance Boundaries

- A hook is a **governance layer**, not a privilege layer; a hook's allow / continue cannot bypass a higher-level deny / stop rule.
- Pre hooks own early filtering, precondition checks, and lightweight fixes; Post hooks own result collection, finalization, and observability. Do not cram all heavy business logic into hooks.
- Hook failures should be "**visible but isolated**" by default, so exceptions in stats, logging, or side-channel governance code do not take down the main execution chain.
- Blocking semantics must be explicit: when to `Stop`, when to `Continue`, and when to only log a warning. Never leave callers guessing.

### `Span<T>` / `stackalloc` / `ref`

Consider only when all of the following hold:

- The code is actually on a synchronous hot path
- Data volume is small with a short lifetime
- It does not cross `await`
- It does not cross threads
- It will not be captured by closures or escape

If there is no evidence of benefit, do not abuse these constructs just to look "advanced".

### `ref` / `in` Parameters: Only for Structs

The `ref` and `in` keywords are only meaningful when passing **structs (value types)** — avoiding stack-copy overhead for structures.

**Classes (reference types) are already passed by reference**. Passing one copies only a pointer-sized reference, never the whole object. Adding `ref` / `in` to classes buys no performance and only adds noise and misleading signals.

```csharp
// ✅ struct with in — avoids copying a large struct
void Process(in Vector position) { ... }
void Modify(ref QAngle angle) { ... }

// ❌ class with ref / in — pointless, classes are already reference types
void Handle(in IPlayer player) { ... }  // 'in' not needed
void Update(ref Config config) { ... }  // 'ref' not needed

// ✅ pass classes directly
void Handle(IPlayer player) { ... }
void Update(Config config) { ... }
```

Exception: the only legitimate use of `ref` on a class parameter is when the callee must **re-point the reference to another instance** (i.e. mutate the caller's reference itself). This is extremely rare in SwiftlyS2 plugins.

## 7. Schema / NetMessages / Protobuf

### Schema

- Writes belong on the main thread
- Add the matching `Updated()` notification for the current field when needed; CSS `SetStateChanged()` does not enter new implementations
- If an async chain needs the data, first take a safe snapshot on the main thread

### NetMessages / Protobuf

Per the official `Network Messages` documentation:

- Network messages are typed-protobuf based
- Send, hook, and unhook each have explicit APIs
- Best read early on the main thread, converted to plain models, then handed to async chains

### Native Functions and Hooks

Per the official `Native Functions and Hooks` documentation:

- Signature and address resolution must have a clear provenance
- Delegate prototypes must match exactly
- Hooks must be uninstalled in pairs
- Mid-hooks are powerful but high-risk: corrupting registers crashes the server directly

### GameHooks

- Prefer `Core.GameHooks` for typed controller, entity, item, movement, pawn, and weapon native hooks.
- Each hook's `Pre` / `Post` context is a callback-scoped `ref struct`; do not carry it across `await`, schedulers, closures, or workers.
- `HookResult.Handled` / `Stop` carry no cancellation semantics in Post.
- Do not use deprecated `Core.Event.On*Hook` as a new-implementation entry point.

## 8. Menu Callbacks

Review menu callbacks as async contexts by default:

- `Click`
- `ValueChanged`
- `Submenu` build callbacks

Recommended rules:

- Prefer `BindingText` for dynamic text
- Prefer `Async` APIs inside callbacks
- Revalidate player / pawn / runtime objects after crossing await points
- Menus are UI shells; push state reads / writes down into modules / services

## 9. Worker / Scheduler

### Scenarios Better Suited to the Scheduler

- Lightweight, low-frequency, main-thread-safe periodic tasks

### Scenarios Better Suited to Background Workers or Cancellable Async Loops

- Disk / network IO
- JSON encode / decode
- Batching
- Dense polling
- Sustained work that must not block the main thread

### Mandatory Checkpoints

- Whether Start / Stop / Flush / Cancel are paired
- Whether dangling fire-and-forget tasks exist
- Whether objects and generations are revalidated before write-back

## 10. DI Guidance

Per the official `Dependency Injection` documentation:

- Prefer DI for new plugins
- `ServiceCollection` + `AddSwiftly(Core)` is the base entry
- Inject `ISwiftlyCore`, logging, configuration, and other dependencies via service constructors
- If a service uses the attribute-registration mechanism, register it explicitly

Three more engineering rules:

1. The root owns composition; it does not babysit every local listener state
2. Commands, events, and hooks registered by a service should be uninstalled by that service
3. Conditional hooks must explicitly maintain on / off state instead of staying mounted forever and idling in callbacks

## 11. Configuration Hot-Reload

### Standard Initialization Flow

```csharp
Core.Configuration.InitializeJsonWithModel<Config>("config.jsonc", "Main")
    .Configure(builder => builder.AddJsonFile("config.jsonc", optional: false, reloadOnChange: true));

var monitor = ServiceProvider.GetRequiredService<IOptionsMonitor<Config>>();
Config = monitor.CurrentValue;
monitor.OnChange(newConfig => { Config = newConfig; /* optional side effects */ });
```

### Engineering Rules for Configuration Hot-Reload

1. **Config class fields must have defaults** so the first serialization generates a complete config file.
2. **Use JSONC format** (`config.jsonc`) so comments keep it maintainable.
3. **Handle side effects in the hot-reload callback**: scheduler restarts, cache invalidation, service reconnects, etc.
4. **Do no blocking IO in the hot-reload callback.**

See the template: `../assets/development/configuration/config-hot-reload-template.cs.md`.

## 12. ConVars

Per the official `Convars` documentation:

- ConVars are for server parameters adjustable instantly at runtime.
- Use `Create` to surface duplicate-registration errors; use `CreateOrFind` when intentionally reusing the same entry. The latter implies no concurrency-safety guarantee.
- Supports bool, integer, float, Color, QAngle, Vector families, and string; min / max overloads are limited to `unmanaged` types.
- `SERVER_CAN_EXECUTE` is not access control; normal ConVars default to `ConvarFlags.NONE`, with permissions enforced at the command / RCON / Permission layers.

### ConVar vs Config Split

- **ConVar**: instant console tuning by admins, runtime switches, temporary tweaks.
- **Config**: structured configuration, nested objects, arrays, persisted defaults.
- **Combined**: ConVars for switches / tweaks, Config for structured defaults.

### Declarative Organization

Prefer declaring them centrally in a partial file `MyPlugin.ConVars.cs`, using the `required` modifier to force initialization:

```csharp
public required IConVar<bool> ConVar_Enable { get; set; }
public required IConVar<int> ConVar_Limit { get; set; }
```

### Range Conventions

- `-1` = unlimited
- `0` = disabled
- `>0` = concrete value

See the template: `../assets/development/convars/convar-template.cs.md`.

## 13. Per-Player State Management

### Pattern Gradient

1. **Lightweight key-values**: `ConcurrentDictionary<ulong, T>` (single-value state, small plugins)
2. **Runtime state objects**: `ConcurrentDictionary<ulong, PlayerRuntime>` (multiple fields, medium plugins)
3. **With DB restore**: async restore from DB on connect, persist on disconnect
4. **Slot arrays + generations**: `PlayerState?[64]` + generation counter (large gameplay, O(1) lookup in high-frequency hooks)

### Identity-Key Strategy

- Real-human long-term storage → `SteamID (ulong)`
- Bots / fake clients → `SessionId` (bot SteamID is fixed `0`)
- Lookups inside high-frequency hooks → slot arrays for O(1)

### Cleanup Timing

Must remove on `OnClientDisconnected`, clear map caches on `OnMapLoad / Unload`, and clear everything in `Unload()`.

### Concurrency Safety

- Prefer `TryAdd` / `TryRemove` / `GetOrAdd` / `AddOrUpdate`
- Avoid two-step `ContainsKey + Add` / `ContainsKey + Remove` patterns
- `AddOrUpdate` merge predicates guard against state downgrades

See the guide: `../assets/patterns/per-player-state/player-state-management-guide.md`.

## 14. Async Safety Patterns

### `FireAndForget` Pattern

When firing non-critical async work from a synchronous entry point (commands, event callbacks), use the toolkit-defined `FireAndForget(task, logger, context)` instead of `_ = Task`:

```csharp
FireAndForget(OnMyCommandAsync(context), Logger, "MyPlugin.OnMyCommand");
```

Do not fire critical gameplay operations without awaiting; keep results, cancellation, and error paths explicitly in the call chain.

### StopOnMapChange

`Core.Scheduler.StopOnMapChange(cts)` only binds the CTS passed in. Bind business async tasks and the timer CTSs returned by `Delay` / `Repeat` / `AddTimer` separately.

### Re-Acquire IPlayer After Async

After any `await`, `IPlayer` must be re-acquired and validated via `IsValid`. Real players can use `SteamID` + `GetPlayerFromSteamId`; bots / mixed runtime state should prefer `SessionId` + `GetPlayerFromSessionId`.

### Generation Counter

Before async write-back, validate freshness with a generation counter (`Interlocked.Increment` + `Volatile.Read`).

See the guide: `../assets/patterns/async-patterns/async-safety-guide.md`.

## 15. Service Factory / Keyed Service / Multi-Implementation

### Factory Pattern

One feature interface with multiple strategy implementations, selected at runtime by name / configuration.

### Keyed Singleton

Multiple independent configured instances of the same interface, managed via `AddKeyedSingleton` + `GetRequiredKeyedService`.

### `GetServices<T>()` Multi-Implementation Resolution

When every implementation must be invoked (e.g. multiple trigger types), resolve all of them with `sp.GetServices<T>()`.

### Batched Lifecycle Management

All services share `Install() / Uninstall()` with exception isolation (one failure does not affect the others).

See the template: `../assets/patterns/service-factory/service-factory-template.cs.md`.

## 16. GameEvent Pre vs Post

### Pre Hooks (HookMode.Pre)

- Fire before the event takes effect
- May return `HookResult.Stop` to intercept the event
- Suitable for: blocking event propagation, altering the final behavior, conditional cancellation

### Post Hooks (HookMode.Post)

- Fire after the event takes effect
- Suitable for: follow-up work based on the event result (logging, rewards, state updates)
- Common pattern: Post hook + `DelayBySeconds` to operate after state settles

### Engineering Rules for GameEvent Hooks

- When unsure between Pre and Post, prefer Post (safer)
- Only intercept in a Pre hook when blocking is genuinely required
- Entity operations in Post hooks commonly need NextTick / DelayBySeconds to wait for stable state
- Events and `Accessor` objects are transient; delayed logic keeps only plain values, `SessionId`, or handles
- Dynamic hooks keep their `Guid` and `Unhook` when the owner deactivates

## 17. ClientCommandHookHandler

### Applicable Scenarios

- Globally intercepting client commands (jointeam, radio, buy, etc.)
- Permission checks or behavior replacement at the earliest stage of the command pipeline

### Key Points

- `[ClientCommandHookHandler]` itself intercepts any client command; `registerRaw` only controls the `sw_` prefix for self-registered commands
- `HookResult.Stop` blocks the command, `HookResult.Continue` lets it through
- Parse the raw `commandLine` string yourself

See the template: `../assets/development/commands/client-command-hook-template.cs.md`.

## 18. OnPrecacheResource

- Fires early on map load for precaching models, sounds, and particle resources.
- Resources not precached fail silently in `SetModel`, `EmitSound`, and similar calls.
- Supports static resources and config-driven dynamic resources.
- Multi-service scenarios may delegate resource registration to each service.

See the template: `../assets/development/core-events/precache-resource-template.cs.md`.

## 19. Cross-Plugin Command Jumps

Medium/large plugin hubs jump to other plugins' menus via `player.ExecuteCommand("sw_TargetPluginCommand")`:

- Loosely coupled: no direct dependency on the other plugin's code
- Can close the current menu after jumping via `CloseAfterClick = true`
- Ensure the target command is registered and available to the current player

## 20. Verification Gates and Evidence Chains

- Build passing ≠ requirements done; verification evidence must be aligned item-by-item with prompt requirements.
- Prefer writing each key verification as: **Check item / Actual execution / Observed result / Conclusion**.
- `PASS` = executed with direct evidence; `FAIL` = evidence shows the requirement is unmet; `PARTIAL` = direct verification is impossible due to environment limits, but the gap plus substitute evidence must be stated.
- `PARTIAL` is only for environment limits, unavailable external dependencies, missing tooling, and other objective blockers. Never use it to mask unverified work, subjective inference, or uncertainty.
- For high-risk changes, add at least one adversarial / regression-oriented check beyond build success, e.g.: repeated install / uninstall, async callbacks after disconnect, map-change cleanup, bot / human mixed-state switching.

## 21. Comments and Output

- Comments should explain intent, thread boundaries, lifecycle reasons, and engine limits
- Avoid noise comments
- Plans, audits, and implementation records should land at method level whenever possible

## 22. Public Reference Entries

- Docs Map: `./swiftlys2-official-docs-map.md`
- Getting Started: `https://swiftlys2.net/docs/development/getting-started/`
- Swiftly Core: `https://swiftlys2.net/docs/development/swiftly-core/`
- Dependency Injection: `https://swiftlys2.net/docs/guides/dependency-injection/`
- Thread Safety: `https://swiftlys2.net/docs/development/thread-safety/`
- Native Functions and Hooks: `https://swiftlys2.net/docs/development/native-functions-and-hooks/`
- Network Messages: `https://swiftlys2.net/docs/development/netmessages/`
- sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
- SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`

## See Also

- [playbook-performance-playbook](playbook-performance-playbook.md)
