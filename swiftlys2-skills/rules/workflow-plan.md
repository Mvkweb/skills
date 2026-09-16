# workflow-plan

> Plan first: classification, method plan, regression matrix

<!-- source: SwiftlyS2-Toolkit-EN:plan-workflow.md — body verbatim, header only added -->

Use the `swiftlys2-toolkit` skill to generate an **executable, method-level implementation plan with reference sources** for SwiftlyS2 plugin tasks.

## Objective

When the user wants to create, modify, optimize, refactor, migrate, or audit a SwiftlyS2 plugin project:

- First identify the task type and target plugin
- Then decide which architecture category applies
- Then output a method-level plan plus regression matrix
- If a historical implementation or older version exists, use it as a **temporary experience source** to extract behavioral and design experience

## Mandatory Rules

1. If the task requires behavioral consistency with a historical implementation, **treat every player-visible capability as a core feature**. Never mark it as deferrable.
2. Preserve the current project's existing architectural boundaries. Do not roll back the directory structure just for "fast alignment".
3. Every plan must be broken down to:
   - files
   - methods
   - reference sources
   - change actions
   - regression points
4. When high-frequency hooks, Schema, Protobuf, or `IPlayer` lifetimes are involved, explicitly state thread / lifecycle boundaries.
5. All code comments must follow the current repository conventions; if no extra conventions exist, keep them meaningful and add no noise comments.
6. Account for the CS2 server 64-tick frame budget. Never plan an implementation that would slow down the main thread.
7. If the plan recommends `Span<T>` / `ReadOnlySpan<T>` / `stackalloc` / `ref` for hot-path optimization, also spell out the safety boundaries.
8. If a historical repository exists in the workspace, use it only as a temporary reference. Never turn it into a long-term future dependency.
9. If mixed bot / human storage is involved, explicitly design the identity-key strategy; default to `SessionId` as the runtime lookup key and never treat bot `SteamID` as a stable key.
10. If the input already provides direct build / test / scenario-regression evidence, explicitly distinguish `PASS / FAIL / PARTIAL`; if no direct evidence exists, never write planned expectations as "verified".
11. `PARTIAL` is only for objective blockers such as constrained environments, missing dependencies, or unavailable tooling. Never use it to cover up skipped execution or subjective uncertainty.

## Language Input Requirements

- Before every output, detect the primary language of the user's **most recent message** and output the full plan, discussion conclusions, and follow-up questions in that language.
- If the user switches languages later, the newest user message wins.
- If the input mixes languages, use the primary language with the clearest user intent.
- Unless the user explicitly requests bilingual output, do not mix Chinese and English inside the same plan.

## Reference Material (Must Be Preferred Before Generating a Plan)

### In-Skill Reference Documents

- `./swiftlys2-plugin-playbook.md`
- `./swiftlys2-performance-optimization-playbook.md` (mandatory when performance, GC, high-frequency hooks, workers, map initialization, or native interop are involved)
- `./swiftlys2-kb-index.md`
- `./swiftlys2-asset-inventory.md`
- `./swiftlys2-current-capability-map.md`

### Public Sources

- SwiftlyS2 official documentation: `https://swiftlys2.net/docs/`
- Getting Started: `https://swiftlys2.net/docs/development/getting-started/`
- Dependency Injection: `https://swiftlys2.net/docs/guides/dependency-injection/`
- Thread Safety: `https://swiftlys2.net/docs/development/thread-safety/`
- GameHooks API: `https://swiftlys2.net/docs/api/gamehooks/`
- Game Events: `https://swiftlys2.net/docs/development/game-events/`
- Native Functions and Hooks: `https://swiftlys2.net/docs/development/native-functions-and-hooks/`
- Network Messages: `https://swiftlys2.net/docs/development/netmessages/`
- Swiftly Core: `https://swiftlys2.net/docs/development/swiftly-core/`
- sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
- SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`

### Current Workspace Custom References (If Present)

Read the nearest `AGENTS.md` in the current scope, and read the project-local skills or reference material it points to as needed; do not write local paths, private repositories, or workspace-specific project names back into the public plan workflow.

## Architecture Decision Rules

### If It Is a Gameplay / State-Sync / Player-Runtime Plugin

Prefer:

- **Modular gameplay architecture**
- Typical layering: `Commands + Events + Hooks + Modules + Workers + Services + Models`

### If It Is an Infra / Manager / System / Global-Capability Plugin

Prefer:

- **DI / service architecture**
- Typical layering: `ServiceCollection + interface / implementation + install / uninstall`

### If It Has Characteristics of Both

It may be classified as:

- **Hybrid architecture**

## Special Experience That Must Be Extracted

If the task touches the following areas, the plan must explicitly state the handling principles:

### 1. Async and Concurrency
- Which logic must stay on the main thread
- Which logic may run in the background
- Whether queue / flush / cancel / generation validation is needed
- Whether map unload / plugin unload needs draining
- Whether `lock`, blocking waits, or main-thread wait risks exist

### 2. High-Frequency Hooks
- Does the target belong to `Core.Event`, `Core.GameEvent`, `Core.GameHooks`, or raw `Core.Memory`? Record the selection rationale.
- If GameHooks, what are the exact category / hook / Pre-or-Post / allowed `HookResult` values?
- If dynamically registered, who owns the `+=` / `-=` or `Guid` / `Unhook` pair?
- Are `ref struct` contexts, temporary events / accessors / netmessages used only inside the callback?
- Should `swiftlys2-performance-optimization-playbook.md` be consulted first for hotspot classification?
- Is a high-frequency hook truly needed, or can a low-frequency scheduler / state diff / coarser movement stage replace it?
- Is early filtering for humans / bots / dead state needed?
- Is allocation and logging reduction needed?
- Should producer / consumer separation be adopted?
- Which stage samples, and which stage computes or writes back?
- Are `Span` / `stackalloc`, ring buffers, bounded queues, generation tokens, Profiler segments, or other concrete optimization boundaries needed?

### 3. Schema Read / Write
- Whether the matching `Updated()` / native sync method is needed for the field (do not keep the CSS `SetStateChanged()` path)
- Whether a snapshot should first be taken on the main thread before async consumption

### 4. Protobuf / NetMessages
- Whether main-thread read / write is mandatory
- Whether messages should be converted to plain models immediately before async handling
- Whether typed protobuf / hook / send / create / dispose is involved
- Whether callback wrappers / `Accessor` objects are only read inside the callback with plain values copied out

### 5. IPlayer Lifecycle
- How connect / disconnect / map-change / player-state rebuild is closed
- Which identity key manages the feature state
- If bots / fake clients are involved, is `SessionId` explicitly used as the runtime lookup key?
- Is bot `SteamID` incorrectly depended upon?
- Are detach / cleanup / generation guards needed against cross-writes?
- Will delayed code reference an already-destroyed `IPlayer`?

## Output Format

### 1. Task Classification
- Task type: create / modify / optimize / refactor / migrate / audit
- Target plugin
- Recommended architecture: modular gameplay / DI-service / hybrid

### 2. Key Constraints
- Player-visible behavior requirements
- Thread-safety requirements
- Lifecycle-closure requirements
- Historical-implementation alignment requirements (if any)
- 64-tick performance-budget requirements
- Safe-use boundaries for `Span` / `ReadOnlySpan` / `stackalloc` / `ref` (if relevant)
- Comment and code-style requirements

### 3. Method-Level Implementation Plan
For each gap / subtask output:
- **Gap**
- **Impact**
- **Reference source** (docs / repository / method)
- **Target file**
- **Target method**
- **Concrete change steps**
- **Thread / lifecycle boundaries to watch**
- **Performance-optimization boundaries to watch**
- **Regression verification points**

### 4. Verification Matrix
Cover at minimum:
- build
- map load / unload
- connect / disconnect
- Critical state-transition chains (if relevant)
- Bots / long-lived runtime state (if relevant)
- Persistence / state restore / cross-module sync (if relevant)

### 5. Verification Language System
- If direct verification evidence already exists, express it as "**Check item / Actual execution / Observed result / Conclusion**".
- `PASS`: direct evidence supports the check.
- `FAIL`: direct evidence shows the check is not satisfied.
- `PARTIAL`: direct verification is impossible only because of environment limits, missing dependencies, or unavailable tooling; always describe the gap plus substitute evidence.
- If this is still the planning stage with no verification executed yet, explicitly write "not directly verified / pending implementation verification" and never disguise it as passed.

## If the Plan Needs to Be Saved to Disk

- Create a file only when the user explicitly asks to save the plan, and prefer the user-specified path.
- When the user gives no path, use `plans/<task-name>.md`; `<task-name>` uses a short, stable, readable kebab-case identifier.
- The plan file must be self-contained, including execution order, target files / methods, verification commands, and completion criteria; do not depend on hidden chat context or UI navigation state.

## Example Usage

- "Generate a method-level plan for adding a DI-based state-sync module to a SwiftlyS2 plugin."
- "Audit a SwiftlyS2 plugin's RuntimeLoop and hook hot paths and produce an optimization plan."
- "Migrate behavioral experience from a historical SwiftlyS2 plugin into the new architecture, requiring all core features to be non-deferrable."
- "Choose between modular gameplay and DI/service architecture for a new plugin and produce a landing plan."

## See Also

- [workflow-audit](workflow-audit.md)
- [workflow-edit](workflow-edit.md)
