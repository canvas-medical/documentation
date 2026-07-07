---
title: "Redirect"
slug: "effect-redirect"
excerpt: "Navigate the Canvas frontend to an allowlisted URL, page, or application."
hidden: false
---

The `RedirectEffect` tells the Canvas frontend to navigate the browser to a destination. The plugin returns the effect from a handler and the frontend performs a full-page navigation. The headline use case is sending a user onward after a note is signed — for example, navigating back to a work queue to pick up the next patient.

The effect is general-purpose: it can be returned from **any** handler that produces effects, including a note state-change (sign/lock) handler, an action-button handler, or an application handler. Wherever the handler runs, returning a `RedirectEffect` navigates the acting user's browser (and only that user's).

Provide **exactly one** destination:

* `url` — a full URL string the plugin composes in Python (it may include patient/note ids). Either an external URL (`https://...`) or an internal Canvas path (`/panel`, `/patient/{key}?noteId=...`).
* `application_id` — the identifier of a Canvas application to open.

By default the navigation replaces the current tab. Set `target` to `RedirectEffect.TargetType.NEW_TAB` to open a `url` destination in a new tab instead.

## Attributes

| Name             | Type                          | Required | Description                                                                                                   |
|------------------|-------------------------------|----------|---------------------------------------------------------------------------------------------------------------|
| `url`            | `str`                         | Yes\*    | A full external URL or internal Canvas path composed by the plugin. Non-empty.                                |
| `application_id` | `str`                         | Yes\*    | The identifier of a Canvas application to open. Must exist and be enabled.                                     |
| `target`         | [`TargetType`](#targettype)   | No       | Where to open a `url` destination. Defaults to `TargetType.SAME_TAB`.                                          |

**\*** Provide **exactly one** of `url` or `application_id` — they are mutually exclusive.

## `TargetType`

A `StrEnum` of the supported navigation targets. You can also pass the string value.

| Member                               | Value         | Behavior                                                            |
|--------------------------------------|---------------|---------------------------------------------------------------------|
| `RedirectEffect.TargetType.SAME_TAB` | `"same_tab"`  | Replaces the current EHR view (full-page navigation). The default.  |
| `RedirectEffect.TargetType.NEW_TAB`  | `"new_tab"`   | Opens the destination in a new browser tab.                         |

## Security & Allowlist

Every destination is validated **on the server** before the browser navigates — the frontend is never trusted to decide whether a target is allowed. This blocks open-redirect abuse and accidental leakage of PHI through query parameters. **Targets are denied by default.**

The allowlist governs only *where a plugin may send a user* — it does **not** change what that user is allowed to see, and cannot be used to bypass their permissions. A redirect performs an ordinary browser navigation, so the destination still enforces the user's own access: redirecting a user to a page or application they lack permission for behaves exactly as if they navigated there themselves (they're denied by that destination), and never elevates their access.

The allowlist is configured **per instance by an administrator** via three plugin secrets. Your plugin declares the keys in its manifest `variables`; the admin sets each value on the Plugin admin page. Each value is a **comma-separated** list:

| Secret key                       | Value example                       | Permits                                                                                          |
|----------------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------|
| `REDIRECT_ALLOWLIST_INTERNAL`    | `/patients, /panel, /patient`       | those path roots and anything the plugin composes under them, matched at a path boundary (`/patient/{key}?noteId=...`). |
| `REDIRECT_ALLOWLIST_EXTERNAL`    | `https://app.example.com`           | those origins/prefixes, matched at an origin/path boundary — so it does **not** match `https://app.example.com.evil.com`. |
| `REDIRECT_ALLOWLIST_APPLICATION` | `my_plugin.applications.app:MyApp`  | redirecting to those applications by id (matched exactly; the app must exist and be enabled).     |

Declare the keys in your manifest so the admin can fill them:

```json
{
  "variables": [
    { "name": "REDIRECT_ALLOWLIST_INTERNAL" },
    { "name": "REDIRECT_ALLOWLIST_EXTERNAL" },
    { "name": "REDIRECT_ALLOWLIST_APPLICATION" }
  ]
}
```

Both steps are required, and both default to "blocked": if you don't **declare** a key in the manifest, the admin has no field to fill; if the admin doesn't **set** a value, that key's allowlist is empty. An empty or absent secret allows nothing — so each redirect category (internal / external / application) only works once its key is declared *and* an admin has given it a value. A freshly installed plugin can therefore redirect nowhere until an admin opts it in.

Non-allowlisted destinations are dropped, and the platform logs only the plugin name and the blocked host (never the full URL/path). Protocol-relative (`//host`) and backslash (`/\host`) targets are always rejected.

## Example Usage

### Redirect to a work queue after a note is signed

Requires `/panel` in the plugin's `REDIRECT_ALLOWLIST_INTERNAL` secret.

```python
from canvas_sdk.effects.redirect import RedirectEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.note import CurrentNoteStateEvent, NoteStates


class RedirectAfterSign(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)

    def compute(self):
        state = CurrentNoteStateEvent.objects.values_list("state", flat=True).get(
            id=self.event.target.id
        )
        if state != NoteStates.LOCKED:
            return []

        # Send the provider back to their work queue to grab the next patient.
        return [RedirectEffect(url="/panel").apply()]
```

### Open an external URL in a new tab from an action button

Requires `https://app.example.com` in the plugin's `REDIRECT_ALLOWLIST_EXTERNAL` secret.

```python?partial=True
return [
    RedirectEffect(
        url="https://app.example.com/orders/next",
        target=RedirectEffect.TargetType.NEW_TAB,
    ).apply()
]
```

### Redirect to an application by id

Requires the identifier in the plugin's `REDIRECT_ALLOWLIST_APPLICATION` secret.

```python?partial=True
return [RedirectEffect(application_id="my_plugin.applications.app:MyApp").apply()]
```

### Redirect from an application iframe

An application iframe can't return an effect directly. The clean pattern is to expose a [SimpleAPI](/sdk/handlers-simple-api/) endpoint on your plugin that returns a `RedirectEffect`, and have the iframe `fetch()` it. Because a SimpleAPI request is authenticated as the acting user, the returned effect is validated and delivered through the **exact same** interpreter → allowlist → per-user path as an action-button or note-sign redirect — there is no iframe-specific code path to reason about.

> **Why an API call and not `postMessage`?** An iframe could `postMessage` its parent window to request a redirect (the way the close-modal workflow does), but we recommend against it here. A redirect already has to make a server round-trip for allowlist validation, so routing the request through the parent window and a dedicated mutation would add a second mechanism that buys nothing. Having the iframe call your own API that returns the effect is cleaner:
>
> - **One mechanism, one mental model.** The iframe reuses the same effect pipeline as every other redirect — no separate frontend bridge, no dedicated mutation, and target validation lives in exactly one place (the interpreter).
> - **Secure by construction.** The plugin whose allowlist is checked is *intrinsic*: it's the plugin that owns the API endpoint. Nothing frontend-supplied has to be trusted or proven un-spoofable — a `postMessage` bridge would first have to attribute the message to an owning application before it could even pick which allowlist to apply.
> - **Composable.** Your endpoint can do real work first — persist state, branch on the patient/note, decide *where* to send the user — and then return the redirect alongside a normal JSON response.

**The endpoint** returns the `RedirectEffect` (optionally with a response body for the `fetch`):

```python?partial=True
from canvas_sdk.effects import Effect
from canvas_sdk.effects.redirect import RedirectEffect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api


class MyAppAPI(StaffSessionAuthMixin, SimpleAPI):
    @api.post("/redirect")
    def redirect(self) -> list[Response | Effect]:
        # ...optionally do work first (persist data, decide the destination)...
        return [
            RedirectEffect(url="/panel").apply(),  # or application_id="my_plugin.applications.app:MyApp"
            JSONResponse({"ok": True}),
        ]
```

**The iframe** calls it with a credentialed, same-origin request:

```js
// inside the plugin application iframe
fetch('/plugin-io/api/my_plugin/redirect', {
  method: 'POST',
  credentials: 'same-origin',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ destination: 'panel' })
});
```

**How the redirect arrives.** The navigation does **not** come back in the `fetch()` response body. The effect is broadcast to the acting user and applied by the frontend's redirect subscription, exactly as for any other `RedirectEffect` — so the `fetch` response is just your endpoint's acknowledgement, and the browser navigates a moment later when the effect is delivered.

**Requirements & gotchas**

- The request must be **same-origin and credentialed** (`credentials: 'same-origin'`) so the server can identify the acting user. Plugin-served iframes — rendered from `LaunchModalEffect` content or a plugin-served URL — are same-origin. An **unauthenticated** request has no acting user, so the redirect is silently dropped.
- The target still has to be **allowlisted** (see [Security & Allowlist](#security--allowlist)); the API path enforces the identical gate.
- `target` (new tab) applies only to `url` destinations; an `application_id` always opens in-app.

## Validation

Construction is validated by Pydantic and will raise a `ValidationError` for:

- Providing neither `url` nor `application_id`, or providing both.
- An empty `url`.
- A `target` that is not a member of `TargetType`.
- An `application_id` that does not resolve to an existing application.

<br/>
<br/>
<br/>
