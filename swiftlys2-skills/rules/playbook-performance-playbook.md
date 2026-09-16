# playbook-performance-playbook

> Classify hotspots first, then apply tick-budget optimizations

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-performance-optimization-playbook.md — body verbatim, header only added -->

This manual guides agents through performance optimization, hot-path auditing, and high-frequency runtime-state refactoring in SwiftlyS2 plugins.

It is not bound to any concrete project. Always identify which hotspot category the current code belongs to first, then land the matching pattern — instead of vaguely saying "reduce GC" or "optimize hooks".

## 0. Classify Before Optimizing

Put the target code into one or more categories first:

| Category | Common Locations | Primary Risk | Preferred Optimization Direction |
| --- | --- | --- | --- |
| Hook hot paths | native hooks, movement hooks, high-frequency events | Repeated per tick / per player | Early exits, lower frequency, less dispatch, no IO |
| Player runtime state | per-player state, HUD state, timer state | Repeated dictionary lookups, dirty writes after disconnect / reconnect | slot state, generation tokens, unified cleanup |
| Sampling buffers | movement samples, replay frames, trace samples | Per-frame allocation, array growth | ring buffers, preallocation, immutable snapshots |
| Background work | JSON, files, network, database, compression | Main-thread stalls, queue backlog | bounded queues, batch drains, backpressure |
| Map-level init | zone / map / rank / static-entity scans | Stale async tasks polluting the new map | map generations, cancel-previous, main-thread commit |
| UI / HUD text | periodic HUD, menus, status text | String and LINQ allocations | StringBuilder reuse, refresh-on-change, throttling |
| Native / binary interop | signatures, protobuf mirrors, native callbacks | Layout errors, bridge-call cost | StructLayout, unmanaged callbacks, signature audits |

If the code fits none of these categories, do not micro-optimize yet. First prove it runs frequently, affects the main-thread frame budget, or causes observable stalls / GC / queue backlog.

## 1. Hook Hot-Path Optimization

### 1.1 Decide Whether the Hook Is Needed at All

Do not enable the finest-grained hook by default.

Priority:

1. Solvable with a low-frequency scheduler / state diff: do not mount a high-frequency hook.
2. Solvable with a movement-stage hook: do not escalate to a usercmd-level hook.
3. Only when per-input-frame precision is mandatory: consider usercmd / command-level hooks.

### 1.2 Standard Hot-Hook Entry Shape

High-frequency hook entries should roughly follow this order:

1. Whether the current feature / timer / mode is enabled.
2. Whether player / pawn / controller exists and is valid.
3. Whether fake clients / bots should be excluded.
4. Whether the current player runtime state can be resolved.
5. Whether subscribers / forwards / modules exist.
6. Only then build the smallest snapshot or call lightweight dispatch.

Example shape:

```csharp
var runtime = runtimeProvider.Current;
if (runtime is null || !runtime.Enabled)
    return ContinueOriginal();

var player = ResolvePlayer();
if (player is null || !player.IsValid || player.IsFakeClient)
    return ContinueOriginal();

var state = playerStateRegistry.TryGet(player.PlayerID);
if (state is null || !state.IsCurrent(player))
    return ContinueOriginal();

var subscribers = runtime.MovementSubscribers;
if (subscribers.Count == 0)
    return ContinueOriginal();

var snapshot = BuildSmallSnapshot(player);
foreach (var subscriber in subscribers)
    subscriber.OnSample(state, snapshot);
```

### 1.3 Forbidden Items Inside Hooks

The following are forbidden by default inside high-frequency hooks:

- JSON serialize / deserialize
- File, network, database IO
- High-frequency logging, chat messages, console output
- Full sorts, directory recursion, full scans over all players / all records
- `Task.Wait()` / `.Result` / synchronous joins
- Per-frame `new List<>` / `new[]` / `ToArray()` / `ToList()`

### 1.4 Hook Dispatch Governance

- Hooks are sampling and governance layers, not business-logic dumping grounds.
- Business logic belongs down in modules / services.
- Every hook needs a clear Install / Uninstall pair.
- Conditional hooks should be installed when the condition holds and uninstalled when it stops holding. Do not idle forever.
- Profiler names must be paired, stable, and distinguishable by stage, e.g. `MyHook.PreDispatch` / `MyHook.PostDispatch`.
- Prefer `Core.GameHooks` for typed controller / entity / item / movement / pawn / weapon hooks; raw native hooks are only for surfaces not covered by typed APIs.
- `ref struct` hook contexts, usercmds, and temporary wrappers are used only inside the current callback stack frame; copy plain values out before dispatching to the background.

## 2. Player Runtime-State Optimization

### 2.1 State Ownership

Player runtime state should be centralized into one per-player runtime object instead of scattered across multiple `Dictionary<ulong, TValue>` instances.

Suggested layering:

1. Small plugins: `Dictionary<ulong, T>` or `ConcurrentDictionary<ulong, T>`.
2. Medium plugins: `PlayerRuntime` aggregating multiple fields and collections.
3. High-frequency plugins: `PlayerRuntime?[]` indexed by slot for O(1) access, plus a SteamID side index.
4. Cross-async write-back: slot + generation / session-token validation.

### 2.2 Slot-State Pattern

Applicable when:

- Runtime state is accessed every tick / per player.
- The player-slot upper bound is well-defined.
- Disconnects / reconnects, bots, fake clients, and delayed callbacks are common.

Pattern:

```csharp
public readonly record struct PlayerToken(int Slot, int Generation);

public sealed class PlayerRuntime
{
    public int Slot { get; }
    public int Generation { get; private set; }
    public ulong SessionId { get; private set; }
    public bool Attached { get; private set; }

    public PlayerToken SnapshotToken() => new(Slot, Generation);
}
```

Write-back rules:

- Save the token when the async task starts.
- Validate the token before writing state back on the main thread.
- Drop results on token mismatch. Do not do "fallback write-backs".

### 2.3 Lifecycle Cleanup

Every runtime-state field must know its cleanup point:

- disconnect: clear player session state, cancel player-level CTS.
- map unload / map reset: clear map-bound state, preview entities, trigger caches.
- plugin unload: clear all state, stop workers, uninstall hooks.
- session reattach: reset stale session fields but keep reusable objects.

Prefer reusing collections:

```csharp
runtime.TouchingZones.Clear();
runtime.PendingOutputs.Clear();
runtime.RecentSamples.Clear();
```

Do not create new collections in high-frequency resets unless the old collection's capacity is demonstrably out of control and there is an explicit shrink strategy.

## 3. Allocation and GC Optimization

### 3.1 stackalloc / Span for Fixed Small Data

Applicable when:

- Synchronous hot path.
- Small fixed-size data.
- Never crosses `await`, never crosses threads, never captured by closures.

Example:

```csharp
Span<Vector> points = stackalloc Vector[7];
FillBoundsSamples(origin, points);
if (zoneService.Overlaps(points, zone))
{
    // ...
}
```

Not applicable when:

- Data length is unbounded.
- It must be stored in fields.
- It must be passed into async tasks.

### 3.2 Avoid Hot-Path LINQ

On hot paths, prefer hand-written loops over:

- `Where(...).ToList()`
- `OrderBy(...).FirstOrDefault()`
- `Select(...).ToArray()`
- `Any(...)` with complex nested closures

Example:

```csharp
Item? firstEnabled = null;
foreach (var item in items)
{
    if (!item.Enabled)
        continue;

    firstEnabled = item;
    break;
}
```

### 3.3 Text Building

For periodic HUD / status text:

- Reuse a `StringBuilder`.
- Refresh on state change instead of concatenating every branch every tick.
- Throttle chat messages and logs.

Example:

```csharp
_builder ??= new StringBuilder(512);
_builder.Clear();
_builder.Append("Speed: ");
_builder.Append(speed);
```

### 3.4 Object-Pool Boundaries

Priority:

1. Do not allocate.
2. Reuse lifetime objects.
3. Preallocate arrays / ring buffers.
4. Only when large buffers, large byte arrays, or clear peak temporary objects exist, consider `ArrayPool<T>` / object pools.

Object pooling is not a default optimization. Pooled objects must have a clear return point and must not carry stale player, map, or entity state.

## 4. Sampling Buffers and Replay-Like Data

### 4.1 Hot-Path Sampling Writes Lightweight Structs Only

On every-tick sampling, only:

- Read the necessary fields.
- Write structs / small snapshots.
- Append to preallocated buffers.

Never:

- JSON
- Compression
- File writes
- Large object-graph copies
- Network requests

### 4.2 Ring Buffers

Suitable when:

- Only the last N frames / last N seconds are needed.
- Pre-run, pre-event, debug samples.

```csharp
public void Write(in Sample sample)
{
    _buffer[_head] = sample;
    _head = (_head + 1) % _buffer.Length;
    if (_count < _buffer.Length)
        _count++;
}
```

### 4.3 Linear Preallocated Arrays

Suitable when:

- The full sequence must be kept during a formal run.
- Common capacity can be estimated.

```csharp
if (_count >= _frames.Length)
{
    Array.Resize(ref _frames, Math.Max(_frames.Length * 2, _count + 1));
}
_frames[_count++] = frame;
```

Long-running scenarios must add caps, segmented flushing, or degradation strategies. Never grow unbounded.

### 4.4 Batched Binary Encoding

Large numbers of homogeneous numeric frames should not default to JSON. Consider:

- `struct` frame representation.
- Fixed layout.
- Batched conversion to bytes.
- JSON only for headers / metadata.

Boundaries:

- Fixed layouts must carry a version.
- Field order, size, and alignment changes must stay compatible or explicitly reject old formats.
- Do not force ordinary business DTOs into binary layouts.

## 5. Background Queues and Workers

### 5.1 Suitable Work

Put in the background:

- JSON serialize / deserialize
- File reads / writes, compression, cleanup
- HTTP / DB / API queries
- Directory scans
- Aggregate statistics
- Deferrable persistence

Do not put in the background:

- Direct player / pawn / entity manipulation
- Schema write-back
- Game-event firing
- Decisions that must affect the game result on the current tick

### 5.2 Bounded Queues

Background queues must have capacity plus backpressure strategies:

| Business Type | Backpressure Strategy |
| --- | --- |
| Droppable telemetry / debug samples | drop newest or drop oldest |
| Rebuildable cache refreshes | coalesce by key |
| Replay / file exports | bounded queue + alerts + optional drop-oldest |
| Transactions / strongly consistent events | Never drop silently; needs a durable queue or failure feedback |

### 5.3 Worker Lifecycle

A worker must at minimum define:

- Start
- Stop / Cancel
- Flush / Drain
- fault logging
- bounded batch size
- shutdown timeout

Before writing back to the main thread:

- Validate the map generation.
- Validate the player token.
- Re-acquire the entity handle.
- Confirm the plugin / module is still active.

## 6. Map-Level Async Initialization

### 6.1 Standard Flow

Map loads, zone loads, rank loads, and static-entity scans should use:

1. `Interlocked.Increment` to generate a map generation.
2. Cancel / dispose the previous round's CTS.
3. Write provisional state on the main thread first to avoid stale-map residue.
4. Prepare pure-data DTOs in the background.
5. Commit once back on the main thread.
6. Validate the generation both before and after commit.
7. Notify downstream modules that the map context is ready.

### 6.2 DTO Boundaries

Background DTOs may contain:

- map id / map name
- API response models
- Parsed plain data
- File-index results

Background DTOs must not contain:

- live `IPlayer`
- live entity wrappers
- pawn / controller wrappers
- Unvalidated `CHandle<T>` dereference results

### 6.3 Downstream Tasks

Downstream load tasks must also inherit the map generation. Even when the underlying API cannot be cancelled, the current map must still be validated before write-back.

## 7. Caching Strategy

### 7.1 Lifecycle Layering

| Cache Type | Cleanup Point |
| --- | --- |
| tick cache | end of current tick |
| player cache | disconnect / session reattach |
| run cache | run end / abort / player reset |
| map cache | map unload / map context shutdown |
| plugin cache | unload / dispose |

### 7.2 Read-Heavy Caches

Good candidates:

- Current map's top records / summaries.
- Current map's zone / static-entity scans.
- Directory indexes.
- Parsed configuration.

Bad candidates:

- Data that changes every tick with no reuse value.
- Player / entity wrappers with no cleanup point.
- Externally strongly consistent state without an invalidation protocol.

### 7.3 Rules Inside Locks

Inside locks, do memory operations only:

- add / remove / update dictionary
- copy small snapshots
- compute small aggregates

Outside locks:

- IO
- network
- DB
- file deletes
- compression
- large sorts

## 8. Logging, Prompts, and Profiler

### 8.1 Throttle High-Frequency Output

Do not output directly on high-frequency paths. Instead:

- At most once per N seconds.
- Output on state change.
- Output the first exception, count repeats.
- Output verbose logs only when a debug convar is enabled.
- Avoid concatenating dynamic identifiers such as player names, SteamIDs, or entity IDs into high-frequency logs; for localization prefer stable segment names, counters, or redacted summaries.

### 8.2 Profiler Usage

- Every `StartRecording` must have a matching `StopRecording`.
- Names must be stable. Do not concatenate player names, SteamIDs, or entity IDs.
- Segments must localize problems, e.g. `Hook.ResolvePlayer`, `Hook.DispatchPre`, `Worker.Flush`.
- Do not let the profiler itself become a high-frequency allocation source.

## 9. JIT / Compile / Native-Interop Optimization

### 9.1 AggressiveInlining

Suitable for:

- Extremely short methods.
- Repeated calls on hot paths.
- Pure wrappers, flag checks, slot lookups, small math checks.

Not suitable for:

- Large methods.
- Logic with IO / logging / exception-heavy paths.
- Adding it just to "look optimized".

Example:

```csharp
[MethodImpl(MethodImplOptions.AggressiveInlining)]
public static bool HasFlagFast(uint flags, uint mask) => (flags & mask) != 0;
```

### 9.2 StructLayout / Fixed Binary Layout

Suitable for:

- Native struct mirrors.
- Binary replay / sample frames.
- Protobuf memory mirrors.
- Unmanaged interop buffers.

Requirements:

- Explicit `Pack` / `Size` / field order.
- A versioning strategy.
- Tests or assertions validating sizes.

### 9.3 UnmanagedCallersOnly / Unmanaged Function Pointers

Only for native callbacks / vtables / trampoline scenarios.

Requirements:

- Delegate / function-pointer signatures match native exactly.
- Every pointer lifetime is explicit.
- No managed objects are captured.
- On error, prefer disabling the optimization over tolerating undefined behavior.

### 9.4 Project-Level Configuration

For server plugins, evaluate:

- `AllowUnsafeBlocks`: only when native interop / pointer APIs require it.
- `ServerGarbageCollection`: long-running server load.
- `ConcurrentGarbageCollection`: reduced pause risk.
- Release-build optimization: never judge real performance from Debug builds.

These are scenario-specific recommendations and must not be written unconditionally into every template.

## 10. Optimization Output Format

When an agent is asked to "optimize performance", the output must at minimum include:

- Hotspot type: Hook / player state / buffer / worker / map init / UI text / native interop.
- Evidence: why this code is hot.
- Current risks: allocation, IO, locks, lifecycle, stale write-backs, overly fine hooks, etc.
- Change direction: which pattern is adopted concretely.
- What not to do: explicitly rejected over-optimizations or compatibility branches.
- Verification: build, profiler, log throttling, lifecycle regression, disconnect / map-change / unload tests.

## 11. Quick Decision Table

| Finding | Preferred Handling |
| --- | --- |
| JSON / IO inside a hook | Switch to main-thread sampling + background worker |
| Per-tick `new[]` inside a hook | `stackalloc` / reused buffers |
| Multiple dictionaries holding player state | Merge into PlayerRuntime |
| Async callbacks writing player state | Add session / generation tokens |
| Slow map loads with post-change corruption | map generation + cancel-previous + main-thread commit |
| High periodic-HUD allocation | StringBuilder reuse + refresh-on-change |
| Directory-scan stalls | map-bound index + top-directory scan + background refresh |
| Oversized record / replay frames | struct frames + prealloc / ring buffer + binary encoding |
| Log spam | Throttling + debug convar |
| High native-callback overhead | Review whether unmanaged callbacks fit, but verify signature safety first |

## See Also

- [playbook-plugin-playbook](playbook-plugin-playbook.md)
