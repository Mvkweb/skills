# workflow-audit

> Audit for lifecycle, thread, hook, and handle risks with evidence

<!-- source: SwiftlyS2-Toolkit-EN:audit-workflow.md — body verbatim, header only added -->

Use the `swiftlys2-toolkit` skill to perform a **general audit** of a SwiftlyS2 plugin project.

## Audit Objectives

When the user asks to "audit" a SwiftlyS2 plugin or subsystem, do not review code style alone. Cover:

1. Whether the architecture fits the project size and responsibilities
2. Whether the lifecycle is fully closed
3. Whether main-thread risks, deadlock risks, or stale-player reference risks exist
4. Whether high-frequency hooks contain allocation, logging, IO, locking, or blocking hotspots
5. Whether Schema / Protobuf usage follows threading and write-back rules
6. Whether behavioral drift exists if a historical implementation or older version is present
7. Whether the work respects the 64-tick server frame-budget mindset

## Mandatory Rules

- Player-visible behavioral differences from history must be listed separately. Never hide them inside "possible improvements".
- Every risk must carry a severity level: P0 / P1 / P2 / P3
- Audit conclusions must be actionable. Do not give vague advice alone.
- If comment issues are found, evaluate them against the current repository comment conventions; if no extra conventions exist, review against the standard "meaningful and explains non-obvious semantics".
- Synchronously blocking calls and main-thread JSON overhead must always be checked.
- If the audit recommends `Span<T>` / `ReadOnlySpan<T>` / `stackalloc` / `ref`, the safety boundaries of those constructs must be audited at the same time.
- If a historical repository exists in the workspace, treat it only as a temporary source of experience. Never assume it will always exist.
- If mixed bot / real-player storage exists, audit the identity-key design separately, with emphasis on whether bot `SteamID` is misused.
- If the audit scope includes build / test / scenario-regression evidence that was already executed, explicitly distinguish `PASS / FAIL / PARTIAL`; if there is no direct evidence, write only "not directly verified" and never present inference as verified fact.
- `PARTIAL` is only for environment limits, missing dependencies, or unavailable tooling. Never use it to cover up skipped checks or subjective uncertainty.

## Language Input Requirements

- Before every output, detect the primary language of the user's **most recent message** and use that language as the sole output language for this turn.
- If the user switches languages later, the newest user message wins.
- If the input mixes languages, use the primary language with the clearest user intent.
- Unless the user explicitly requests bilingual output, do not mix Chinese and English inside the same audit passage.

## Priority References

### Skill Reference Documents

- `./swiftlys2-plugin-playbook.md`
- `./swiftlys2-performance-optimization-playbook.md` (mandatory when auditing performance, GC, high-frequency hooks, workers, map initialization, or native interop)
- `./swiftlys2-kb-index.md`
- `./swiftlys2-asset-inventory.md`
- `./swiftlys2-current-capability-map.md`

### Public Sources

- SwiftlyS2 official documentation: `https://swiftlys2.net/docs/`
- Thread Safety: `https://swiftlys2.net/docs/development/thread-safety/`
- GameHooks API: `https://swiftlys2.net/docs/api/gamehooks/`
- Game Events: `https://swiftlys2.net/docs/development/game-events/`
- Native Functions and Hooks: `https://swiftlys2.net/docs/development/native-functions-and-hooks/`
- Network Messages: `https://swiftlys2.net/docs/development/netmessages/`
- Dependency Injection: `https://swiftlys2.net/docs/guides/dependency-injection/`
- sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
- SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`

### Current Workspace Custom References (If Present)

Read the nearest `AGENTS.md` in the current scope, and read the project-local skills or reference material it points to as needed; do not write local paths, private repositories, or workspace-specific project names back into the public audit workflow.

## Audit Dimensions

### 1. Architecture Audit
- Does the code look more like modular gameplay, DI/service, or hybrid architecture?
- Is the layering clear?
- Is business logic incorrectly stuffed into the main class / command / event entry points?
- Should it be extracted into a module / service / worker / manager?

### 2. Lifecycle Audit
- `OnClientPutInServer`
- `OnClientDisconnected`
- `OnMapLoad`
- `OnMapUnload`

Check specifically:
- Whether delayed logic still holds an `IPlayer` after the player disconnects
- Whether dirty state survives a map change

### 3. Thread Safety and Async Audit
- Whether main-thread APIs are misused from background threads
- Whether a `lock` creates a main-thread wait risk
- Whether `.Wait()` / `.Result` / synchronous blocking exists
- Whether JSON serialize / deserialize runs on the main thread
- Whether worker stop / flush / cancel is complete
- Whether generation / session validation exists

### 4. High-Frequency Hook Audit
- Whether deprecated `Core.Event.On*Hook` is left on controller / entity / movement / pawn / weapon paths instead of migrating to `Core.GameHooks`?
- Whether `DynamicHook`, `[HookCallback]`, or CSS hook APIs are treated as current SwiftlyS2 implementations?
- Whether `Pre` / `Post` are correct, and whether `Handled` / `Stop` is incorrectly relied upon in Post?
- Whether asymmetric `+=`, dynamic `Guid` hooks, or raw `RemoveHook` calls lack symmetric cancellation?
- Whether `ref struct` contexts, temporary events / accessors / netmessages escape across callbacks, awaits, schedulers, or closures?
- Whether the hotspot was first classified per `swiftlys2-performance-optimization-playbook.md` as a Hook, player-state, buffer, worker, map-init, UI-text, or native-interop hotspot
- Whether the hook is truly needed, or could be replaced by a lower-frequency scheduler / state diff / coarser movement stage
- Whether there are pointless allocations
- Whether there are logging hotspots
- Whether there are IO / API calls
- Whether heavy CPU work such as JSON is mixed in
- Whether fast-path filtering for alive humans / bots / dead state exists
- Whether producer / consumer separation exists
- Whether the 64-tick server budget mindset is respected
- Whether hot-path data transfer can use `Span / ReadOnlySpan / stackalloc / ref`
- Whether concrete landing points exist for ring buffers, bounded queues, generation tokens, StringBuilder reuse, or stable Profiler segments

### 5. Schema / Protobuf Audit
- Whether Schema writes call the currently required `Updated()` for the field, with no leftover CSS `SetStateChanged()` calls
- Whether protobuf / usercmd / entity handles are accessed from unsafe threads
- Whether protobuf data is snapshotted into plain models when needed
- Whether callback-scoped `msg` / `Accessor` / Game Event wrappers are cached

### 6. Bot / Fake-Client Identity-Key Audit
- Whether `SteamID` is incorrectly used to look up bots / fake clients
- Whether it is explicitly understood that bot `SteamID` should be treated as `0` in practice
- Whether `SessionId` is preferred as the lookup key for mixed bot / human runtime state
- Whether mixed storage correctly separates identity-key strategies for humans and bots

### 7. Historical Implementation Alignment Audit (If Applicable)
- List historical reference methods
- List current target methods
- List behavioral differences and player impact

## Output Format

### 1. Audit Scope
- Target repository / plugin
- Audit type
- Primary reference sources used

### 2. Summary Conclusions
- Current architecture verdict
- Overall risk level
- The 3–10 most critical issues
- If direct verification evidence already exists, add a `PASS / FAIL / PARTIAL` summary for key checks; if not, explicitly mark the scope as "not directly verified"

### 3. Issue List
For each issue output:
- **Severity**: P0 / P1 / P2 / P3
- **Issue**
- **Impact**
- **Location** (file + method)
- **Reference** (docs / repository / historical method)
- **Suggested fix direction**
- **Whether performance-optimization boundaries need a parallel note
- **Whether main-thread synchronous blocking or main-thread JSON overhead is involved**

### 4. Fix Priority Recommendations
- What to fix first
- What can be done in parallel
- What needs a further method-level plan

### 5. Regression Matrix
- build
- map load / unload
- connect / disconnect
- gameevent / event / hook related (if applicable)
- high-frequency hook stress points (if relevant)

### 6. Verification Language System
- For executed verification, prefer the evidence chain "**Check item / Actual execution / Observed result / Conclusion**".
- `PASS`: supported by direct evidence.
- `FAIL`: direct evidence shows the requirement is not met.
- `PARTIAL`: direct verification is impossible only because of objective environment limits; attach substitute evidence or describe the gap.
- If the current audit is mainly based on static reading rather than runtime verification, explicitly write "static audit conclusions, not equivalent to executed verification".

## Example Usage

- "Audit the thread safety and lifecycle closure of this SwiftlyS2 plugin."
- "Audit the behavioral gap between the historical implementation and the current implementation, focusing on state sync / high-frequency loops / persistence chains."
- "Audit whether a SwiftlyS2 plugin should stay on modular gameplay architecture or move to DI/service architecture."
- "Audit high-frequency hook performance hotspots and give optimization directions, but do not change code directly."

## See Also

- [workflow-plan](workflow-plan.md)
- [workflow-edit](workflow-edit.md)
