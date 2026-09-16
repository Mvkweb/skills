# hud-custom-hud

> Custom HUD layout, dialog vars, and input capture rules

<!-- source: SwiftlyS2-Toolkit-EN:swiftlys2-custom-hud.md — body verbatim, header only added -->

> Official docs: <https://swiftlys2.net/docs/development/custom-hud/>
> Official warning: Custom HUD is a **new and unstable** feature. Valve may introduce breaking API changes in the future; when actual behavior disagrees with the docs, trust live testing and report upstream.
> Scope split: this file covers only the server-side C# entity and state management; Panorama XML / CSS layout authoring is client-asset work.

## 1. Model Overview

- Use the `custom_hud_layout` entity to create custom HUDs for players.
- The UI is built with Panorama XML + CSS; the server updates state through methods on `CCSCustomHudLayout`.
- An XML element's `id` is the `panelId` in server-side methods; the `dynamic` part of a `{s:dynamic}` dynamic string is the `variableName`.

## 2. Creating the Entity

```csharp
var hud = Core.EntitySystem.CreateEntity<CCSCustomHudLayout>();
hud.StrLayout = "panorama/layout/custom_game/example.xml";
hud.StrLayoutUpdated();
hud.DispatchSpawn();
```

- Set the layout path first and notify the engine that the field changed via `StrLayoutUpdated()`, then `DispatchSpawn()`.
- Entity lifetime follows the general entity rules: clean up on map unload / plugin unload. Do not leave orphaned HUD entities behind.

## 3. Dynamic Strings (Dialog Variables)

Global values (shared by all players):

```csharp
hud.SetDialogVariableString("text1", "dynamic", "Global text");
string? globalValue = hud.GetDialogVariableString("text1", "dynamic");
```

Per-player overrides:

```csharp
hud.SetDialogVariableStringForPlayer(playerId, "text1", "dynamic", "Only this player");
string? playerValue = hud.GetDialogVariableStringForPlayer(playerId, "text1", "dynamic");
hud.RemoveDialogVariableStringForPlayer(playerId, "text1", "dynamic");
```

Key semantics:

- `GetDialogVariableStringForPlayer` **reads only the per-player override and never falls back to the global value**; it returns `null` when unset (even if a global value exists).
- After `RemoveDialogVariableStringForPlayer`, that player renders using the global setting again.
- For high-frequency updates (every tick / every sample), do not blindly set everything; read-then-compare and write only on change to avoid needless sync overhead.

## 4. Dynamic CSS Classes

`EHudPanelClassStatus_t` tri-state:

| State | Meaning |
| --- | --- |
| `k_eHudPanelClassStatus_HasClass` | Element has the class |
| `k_eHudPanelClassStatus_DoesNotHaveClass` | Element does not have the class |
| `k_eHudPanelClassStatus_Undefined` | Undefined (also returned when reading a nonexistent panelId / className / state) |

```csharp
hud.SetHasClass("main_panel", "highlight", EHudPanelClassStatus_t.k_eHudPanelClassStatus_HasClass);
EHudPanelClassStatus_t global = hud.GetHasClass("main_panel", "highlight");

hud.SetHasClassForPlayer(playerId, "main_panel", "highlight", EHudPanelClassStatus_t.k_eHudPanelClassStatus_DoesNotHaveClass);
EHudPanelClassStatus_t perPlayer = hud.GetHasClassForPlayer(playerId, "main_panel", "highlight");
```

`className` must be a class already defined in Panorama CSS.

## 5. Input Capture and Button Clicks

After input capture is enabled, players can freely move the mouse cursor and click buttons inside the HUD:

```csharp
hud.SetInputCaptureEnabled(true);                     // Global
bool g = hud.IsInputCaptureEnabled();
hud.SetInputCaptureEnabledForPlayer(playerId, true);  // Per player
bool p = hud.IsInputCaptureEnabledForPlayer(playerId);
```

Click events (subscribe on Load / unsubscribe on Unload):

```csharp
public override void Load(bool hotReload)
{
    Core.Event.OnCustomHudClicked += OnCustomHudClicked;
}

public override void Unload(bool hotReload)
{
    Core.Event.OnCustomHudClicked -= OnCustomHudClicked;
}

private void OnCustomHudClicked(IOnCustomHudClickedEvent @event)
{
    if (@event.ButtonId != "action_button") return;
    // @event.PlayerId / @event.CustomHudLayout
}
```

`IOnCustomHudClickedEvent` properties:

| Property | Description |
| --- | --- |
| `PlayerId` | Player who clicked |
| `ButtonId` | The clicked button's `id` in XML |
| `CustomHudLayout` | The `CCSCustomHudLayout` entity containing the clicked button |

- `OnCustomHudClicked` receives clicks from **all** Custom HUD layouts; when the plugin creates multiple layouts, compare against the held layout entity before handling a ButtonId.
- Input capture changes player input behavior (cursor is released). Disable it per player promptly once done (e.g. when interaction ends).

## 6. Thread Safety and Async Variants

- All state-mutating synchronous methods above are thread-unsafe (i.e. `[ThreadUnsafe]` semantics).
- Every thread-unsafe method has a matching `Async` variant (`SetDialogVariableStringAsync`, `SetDialogVariableStringForPlayerAsync`, `RemoveDialogVariableStringForPlayerAsync`, `SetHasClassAsync`, `SetHasClassForPlayerAsync`, `SetInputCaptureEnabledAsync`, `SetInputCaptureEnabledForPlayerAsync`); they execute immediately on the game thread and are otherwise scheduled onto the game thread.
- **Background tasks must always `await` the Async variants** and never call the synchronous methods directly.
- Getters stay synchronous.

## 7. Method Quick Reference

| Method | Description |
| --- | --- |
| `SetDialogVariableString` / `GetDialogVariableString` | Global dynamic-string write / read (`null` when unset) |
| `SetDialogVariableStringForPlayer` / `GetDialogVariableStringForPlayer` / `RemoveDialogVariableStringForPlayer` | Per-player override set / read (no global fallback) / remove |
| `SetHasClass` / `GetHasClass` | Global CSS-class state |
| `SetHasClassForPlayer` / `GetHasClassForPlayer` | Per-player CSS-class state |
| `SetInputCaptureEnabled` / `IsInputCaptureEnabled` | Global input capture |
| `SetInputCaptureEnabledForPlayer` / `IsInputCaptureEnabledForPlayer` | Per-player input capture |

## 8. Lifecycle and Review Checklist

- Entities: fallback path when creation fails / platform is unsupported; entity cleanup on map unload and plugin unload.
- Events: paired subscribe / unsubscribe for `OnCustomHudClicked` (covering Load / Unload and hot reload).
- Input capture: paired enable / disable timing; per-player override state after disconnect must not depend on a stale `IPlayer` reference.
- Hot paths: dirty-check dialog-variable / class-state updates; use Async variants from background tasks.
- Compatibility: the feature is unstable, so accept possible Valve breaking changes; centralize layout XML and panel-`id` conventions so API changes converge to a small edit surface.

Related API pages: `CCSCustomHudLayout` (SchemaDefinitions), `EHudPanelClassStatus_t`, `IOnCustomHudClickedEvent` (Events), `EventDelegates.OnCustomHudClicked`.

## See Also

- [playbook-plugin-playbook](playbook-plugin-playbook.md)
