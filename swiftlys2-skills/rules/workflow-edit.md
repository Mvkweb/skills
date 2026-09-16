# workflow-edit

> Smallest correct edit with validation and delivery notes

<!-- source: SwiftlyS2-Toolkit-EN:edit-workflow.md — body verbatim, header only added -->

Use the `swiftlys2-toolkit` skill to directly handle **add-feature / modify-feature / remove-feature** scenarios in SwiftlyS2 plugins.

This workflow applies when the user explicitly wants **direct code changes to land**, rather than a full audit or a long plan first.

## Applicable Scenarios

Prefer this workflow when the user makes requests of the following types:

- "Add a feature"
- "Modify this feature"
- "Remove this feature"
- "Change the code directly"
- "Wire this logic in"
- "Fix this behavior, but don't write a big proposal first"

## Objective

Preserve SwiftlyS2 agent development quality in direct-edit scenarios:

- First identify the feature type and owning subsystem
- Then locate the entry point, state ownership, thread boundaries, and lifecycle closure
- Then make the smallest necessary change
- Finally run build / error checks / regression verification

## Edit Risk Levels

### P0: Narrow the Scope Before Changing
- Spans multiple subsystems with unclear boundaries
- Involves wide behavioral drift in long-lived runtime state / persistence / cross-module state sync
- Has an obvious historical-alignment requirement, but method-level mapping is not done yet
- Continuing to change code directly is likely to break current architectural boundaries

### P1: Direct Edit Allowed, but Under Strong Constraints
- High-frequency hooks
- Schema / entity write-back
- Protobuf / usercmd
- Dense calls to thread-sensitive APIs
- Map lifecycle / disconnect cleanup / auto-controlled entity lifetimes

### P2: Standard Direct-Edit Scenarios
- Menus
- Commands
- Service-local logic
- Worker-local flows
- Single-module behavior fixes

### P3: Low-Risk Direct-Edit Scenarios
- Small-range condition fixes
- Dynamic text binding
- Small cleanups with no behavioral drift

## Mandatory Rules

1. Do not force-upgrade every "direct edit" request into a full audit or plan.
2. If the task has already reached P0 / large-task level, do not silently convert the implementation request into plan-only or audit-only output; first explain the trigger in one sentence, then narrow the scope, request the missing information, or state the blocker explicitly when the scope cannot converge.
3. Before touching code, complete at least one **minimum necessary localization** pass.
4. If the task requires consistency with a historical implementation, treat all player-visible capabilities as core. Never silently drop them.
5. Direct edits must still respect current architectural boundaries. Do not stuff logic back into the main class or write across layers just to save effort.
6. When thread-sensitive APIs are involved:
   - Prefer the `Async` variant in async contexts
   - Do not default to `NextTick` / `NextWorldUpdate` as a catch-all
7. Treat menu `Click` / `ValueChanged` delegates as async contexts.
8. Prefer `BindingText` for dynamic menu text.
9. If bots / fake clients / auto-controlled entities or mixed bot-human storage are involved, never equate bot identity keys with the human-player strategy directly.
10. In hot paths or high-frequency data transfer, if SwiftlyS2 / the current API already provides a parameter as `ref`, prefer keeping `ref`; if small high-frequency data transfer is needed, `Span<T>` / `ReadOnlySpan<T>` may be evaluated, but never abused across `await` or thread boundaries.
11. All comments must follow the current repository conventions; if no extra conventions exist, comments must be meaningful and explain non-obvious intent.
12. High-risk changes must include build plus scenario-regression notes.
13. If mixed bot / human storage is involved, default to `SessionId` as the runtime lookup key. Never treat bot `SteamID` as a reliable primary key.
14. Express verification conclusions as "**Check item / Actual execution / Observed result / Conclusion**" whenever possible, and use `PASS / FAIL / PARTIAL` when direct evidence exists.
15. `PARTIAL` is only for environment limits, missing dependencies, or unavailable tooling. Never use it to cover up skipped execution, subjective uncertainty, or "did not have time to verify yet".
16. Unless the current user explicitly requests compatibility with old versions, old callers, or historical data, do not add compatibility branches, aliases, adapters, fallbacks, dual-write, or dual-read paths.

## Language Input Requirements

- Before every output, detect the primary language of the user's **most recent message** and use that language as the sole output language for this turn.
- If the user switches languages later, the newest user message wins.
- If the input mixes languages, use the primary language with the clearest user intent.
- Unless the user explicitly requests bilingual output, do not mix Chinese and English inside the same change or verification notes.

## Minimum Navigation Before Use

Depending on the task, pair it with the following assets first:

### Command Related
- `../assets/development/commands/command-attribute-template.cs.md`
- `../assets/development/commands/command-service-template.cs.md`
- `../assets/development/commands/client-command-hook-template.cs.md`
- `../assets/development/using-attributes/attribute-registration-checklist.md`

### Menu Related
- `../assets/development/menus/menu-template.cs.md`
- `../assets/development/thread-safety/thread-sensitivity-checklist.md`

### Hook / Runtime / High-Frequency Paths
- `./swiftlys2-performance-optimization-playbook.md`
- `../assets/development/game-hooks/game-hooks-pre-post-guide.md` (typed controller / entity / item / movement / pawn / weapon hooks)
- `../assets/development/game-events/game-events-usage-notes.md` (generated Game Events)
- `../assets/development/native-functions-and-hooks/hook-handler-template.cs.md` (raw native / mid-hooks only when GameHooks does not cover the surface)
- `../assets/development/thread-safety/thread-sensitivity-checklist.md`
- `../assets/development/profiler/hotpath-gc-checklist.md`

### Schema / Entity Write-Back
- `../assets/development/entity/schema-write-checklist.md`
- `../assets/development/entity/entity-key-values-guide.md`
- `../assets/development/thread-safety/thread-sensitivity-checklist.md`

### Configuration / ConVars
- `../assets/development/configuration/config-hot-reload-template.cs.md`
- `../assets/development/convars/convar-template.cs.md`

### Database / Sound / Steamworks / Memory
- `../assets/development/database/database-connection-template.cs.md`
- `../assets/development/sound-events/sound-event-guide.md`
- `../assets/development/steamworks/steamworks-server-guide.md`
- `../assets/development/memory/memory-service-guide.md`

### Worker / Async Persistence / Background Tasks
- `./swiftlys2-performance-optimization-playbook.md`
- `../assets/development/scheduler/scheduler-vs-worker-guide.md`
- `../assets/patterns/background-workers/worker-template.cs.md`
- `../assets/patterns/async-patterns/async-safety-guide.md`
- `../assets/development/core-events/lifecycle-checklist.md`

### DI / Service
- `../assets/guides/dependency-injection/di-service-plugin-template.cs.md`
- `../assets/guides/dependency-injection/service-template.cs.md`
- `../assets/patterns/service-factory/service-factory-template.cs.md`

### Resource Precaching / Lifecycle
- `../assets/development/core-events/precache-resource-template.cs.md`
- `../assets/development/core-events/lifecycle-checklist.md`

### Player Runtime State
- `./swiftlys2-performance-optimization-playbook.md`
- `../assets/patterns/per-player-state/player-state-management-guide.md`

### When Higher-Level Engineering Rules Are Needed
- `./swiftlys2-plugin-playbook.md`
- `./swiftlys2-kb-index.md`
- `./swiftlys2-asset-inventory.md`

## Direct Edit Workflow

### 1. Determine the Task Type First
- **Add**: new capability, entry point, configuration, flow
- **Modify**: adjust existing logic, fix bugs, change behavior
- **Remove**: remove a feature, clean up an entry point, delete dead branches

### 2. Determine the Risk Level
- Which level is it: P0 / P1 / P2 / P3?
- If P0, briefly explain why it already qualifies as a large / high-uncertainty task, then narrow it to a directly implementable file / method-level scope, request the missing information, or state the current blocker; do not unilaterally switch to plan-only or audit-only output inside this workflow
- If P1 / P2 / P3, continue with the direct-edit flow

### 3. Perform Minimum Necessary Localization
Answer at minimum:
- Where are the entry files / methods?
- Which module / service / runtime context owns the state?
- Are commands, menus, events, hooks, workers, schemas, or protobufs involved?
- Are `IPlayer` / `Pawn` / entity lifetimes involved?
- Are thread-sensitive APIs involved?
- Are bot / fake-client identity lookups or mixed-storage key designs involved?
- If bots / fake clients are involved, is `SteamID` incorrectly treated as a reliable key, and should it use `SessionId` instead?
- Is there avoidable high-frequency object copying that should be evaluated for `ref` / `Span`?

### 4. Select the Right Asset
- command (attribute) → command attribute template + attribute checklist
- command (service-owned) → command service template
- command (client command hook) → client-command-hook template
- menu → menu template + thread checklist
- typed game hook → game-hooks guide + thread checklist + hot-path checklist
- generated Game Event → game-events guide + lifecycle checklist
- raw native / mid-hook → native-functions-and-hooks template + thread checklist + hot-path checklist
- schema → schema checklist
- worker → scheduler-vs-worker guide + worker template + lifecycle checklist
- service / DI → service template / DI template
- service factory / keyed DI → service-factory template + di-service-plugin template
- config / configuration hot-reload → config-hot-reload template
- convar → convar template
- precache / resource precaching → precache-resource template + lifecycle checklist
- per-player state / player runtime state → player-state-management guide
- async safety → async-safety guide + lifecycle checklist

### 5. Requirements During Implementation
- Make the smallest possible change
- Do not reformat unrelated code
- Do not copy-paste logic across layers
- Do not introduce "temporary TODO logic" into the main flow
- Revalidate player / entity validity across every `await` / delayed task
- If it is only a dynamic text update, prefer `BindingText`
- If it is a thread-sensitive call in an async context, prefer the `Async` API
- If it sits on a hot path, opportunistically check for removable copies, boxing, or temporary array allocations

### 6. Verification Requirements
Execute at minimum:
- File-level problem checks
- Target plugin build (if the change is real code rather than docs-only)

Supplement by risk:
- map load / unload
- connect / disconnect
- Critical state-transition chains (if relevant)
- bots / long-lived runtime state
- persistence / state restore / cross-module sync

## Output Format

### 1. Task Verdict
- Type: add / modify / remove
- Risk level: P0 / P1 / P2 / P3
- Target plugin / subsystem
- Entry-point localization
- Primary state ownership

### 2. Edit Strategy
- Toolkit assets used
- Why it was landed this way
- Thread / lifecycle boundaries to watch

### 3. Actual Changes
List per file:
- **File**
- **Method / region**
- **Change content**
- **Why it was changed this way**

### 4. Verification Results
- Problem-check results
- Build results (if applicable)
- Covered regression points
- High-risk scenarios not yet executed but recommended
- If direct evidence exists, mark key checks as `PASS / FAIL / PARTIAL`
- If an item is still not directly verified, explicitly write "not directly verified" instead of packaging expectations or inference as passed

## When to Narrow Scope or State a Blocker First

When the following occur, narrow the scope, complete the missing information, or state the blocker first:

- The change spans multiple subsystems with unclear behavioral boundaries
- An obvious historical-behavior alignment need exists, but the gap is not yet clarified
- Wide long-lived runtime-state / persistence / state-sync drift is involved
- State ownership cannot be confirmed, and continuing would break architectural boundaries

In these cases do not silently rewrite the implementation task into plan-only or audit-only output; first narrow the scope, request the missing information, or state the current blocker. If the user explicitly wants only a method-level plan or a systematic audit in this turn, switch to `plan-workflow.md` or `audit-workflow.md` inside the same skill.

## Example Usage

- "Directly add a settings menu to this SwiftlyS2 plugin and wire up the save logic."
- "Modify this command's permissions and prompts without touching other behavior."
- "Remove the old reward entry and complete the cleanup logic."
- "Convert the existing menu to BindingText dynamic text binding."
- "Change this thread-sensitive synchronous call into a more appropriate async-safe form."

## See Also

- [workflow-plan](workflow-plan.md)
- [workflow-audit](workflow-audit.md)
