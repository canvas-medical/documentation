---
title: "Redirect"
slug: "redirect-effect"
excerpt: "Effect for navigating the Canvas frontend to an internal path or external URL"
hidden: false
---

## Overview

The `RedirectEffect` navigates the Canvas frontend to a destination. Return it from a plugin handler to send the user to another location in the same browser tab or a new one. The destination is either a `url` — an internal Canvas path or an external URL — or an `application_id` — the identifier of a Canvas application to open. Provide exactly one of the two.

Your plugin builds the full `url` string in Python, so it can include patient or note identifiers. A `url` can be an internal Canvas path (for example, `/panel` or `/patient/{key}?...`) or an external URL (for example, `https://example.com`), and must be non-empty when provided.

A redirect only navigates the browser of the user who triggered the handler. It is scoped to that acting user and never affects anyone else's session. Redirects are also surface-independent: any handler that returns a `RedirectEffect` — a note sign or lock, an action button, an application, and so on — triggers the navigation.

```python
from canvas_sdk.effects.redirect import RedirectEffect
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        return [RedirectEffect(url="/panel").apply()]
```

To open an external URL in a new tab, set `target` to `NEW_TAB`:

```python
from canvas_sdk.effects.redirect import RedirectEffect

RedirectEffect(
    url="https://example.com",
    target=RedirectEffect.TargetType.NEW_TAB,
).apply()
```

Instead of a URL, you can open a Canvas application by its identifier with `application_id`:

```python
from canvas_sdk.effects.redirect import RedirectEffect

RedirectEffect(application_id="my_plugin.apps:MyApp").apply()
```

## Structure

### **TargetType**

An enumeration of the tab targets a redirect can use:

| Value       | Description                              |
|-------------|------------------------------------------|
| `SAME_TAB`  | Navigate in the current tab (default).   |
| `NEW_TAB`   | Open the target in a new browser tab.    |

### **RedirectEffect**

A RedirectEffect consists of the following properties:

#### Attributes

| Attribute | Type         | Description                                                                                       |
|-----------|--------------|---------------------------------------------------------------------------------------------------|
| `url`     | `str \| None` | The destination to navigate to — an internal Canvas path or external URL. Must be non-empty when provided; mutually exclusive with `application_id`. |
| `application_id` | `str \| None` | The identifier of a [Canvas application](/sdk/handlers-applications/) to open (the `<module path>:<ClassName>` identifier, for example `my_plugin.apps:MyApp`); mutually exclusive with `url`. The application must exist, or `apply()` raises a validation error. Server-side, the `application_id` must also be listed in the plugin's `REDIRECT_ALLOWLIST_APPLICATION` variable and resolve to an application whose plugin is enabled. Unlike the `apply()` existence error, this check fails silently: the redirect simply doesn't happen, with a warning written to the plugin's `canvas logs`. |
| `target`  | `TargetType` | Where to open the target. Defaults to `SAME_TAB`.                                                 |

{% include alert.html type="warning" content="Exactly one of <code>url</code> or <code>application_id</code> must be provided. Providing neither or both raises a validation error at <code>apply()</code> time." %}

<br/>

## Allowing redirect targets

For security, every redirect target is validated on the server before the browser navigates, and any target that isn't permitted is blocked. This allowlist is separate from the `url_permissions` field, which allow-lists iframe and script domains (see [Layout Effects: Additional Configuration](/sdk/layout-effect/#additional-configuration)) — the two are unrelated. The allowlist comes from three admin-managed plugin **variables**. They are declared under the `variables` field in your plugin's `CANVAS_MANIFEST.json` using the same mechanism documented on the [Managing Variables](/sdk/secrets/) page, with values set at install time or through the Admin UI:

- `REDIRECT_ALLOWLIST_INTERNAL` — permitted internal Canvas paths
- `REDIRECT_ALLOWLIST_EXTERNAL` — permitted external URL prefixes
- `REDIRECT_ALLOWLIST_APPLICATION` — permitted application identifiers

Each variable's value is a newline-delimited list — one entry per line. It is not comma-separated and not a JSON array.

An internal Canvas path — one that begins with `/`, such as `/panel` or `/patient/{key}` — must match an entry in `REDIRECT_ALLOWLIST_INTERNAL` at a path boundary (an entry of `/panel` permits `/panel/123` but not `/panels`). Nothing is implicitly permitted: an empty or unset allowlist denies everything. Protocol-relative (`//host`) and backslash-prefixed (`/\host`) targets are rejected, because a browser can resolve them to a different origin.

External absolute URLs must match an entry in `REDIRECT_ALLOWLIST_EXTERNAL`. Matching is at an origin or path boundary and is case-insensitive, so an entry of `https://app.example.com` permits `https://app.example.com/orders` but not `https://app.example.com.evil.com`. A differing port, such as `https://app.example.com:8443/...`, is not permitted either.

An `application_id` must exactly match an entry in `REDIRECT_ALLOWLIST_APPLICATION` — the full `<module path>:<ClassName>` identifier, compared case-sensitively — and the application's plugin must be enabled. Otherwise the redirect is blocked.

Declare the three variables in your `CANVAS_MANIFEST.json` (they are non-sensitive, so no `sensitive` flag is needed):

```json
"variables": [
  {"name": "REDIRECT_ALLOWLIST_INTERNAL"},
  {"name": "REDIRECT_ALLOWLIST_EXTERNAL"},
  {"name": "REDIRECT_ALLOWLIST_APPLICATION"}
]
```

Set a value with one entry per line. For example, to allow two internal paths, use bash ANSI-C quoting so the newline between entries is preserved on a single command line:

```console
$ canvas config set my_plugin $'REDIRECT_ALLOWLIST_INTERNAL=/panel\n/patient'
```

The same one-entry-per-line format and quoting technique applies to all three variables — `REDIRECT_ALLOWLIST_EXTERNAL` and `REDIRECT_ALLOWLIST_APPLICATION` are set the same way. Run `canvas config list <plugin_name>` (see the [Managing Variables](/sdk/secrets/) page) to confirm a value is set.

You can also enter the value one entry per line through the Admin UI.

{% include alert.html type="info" content="When a target is blocked it is silently not navigated — the block is never broadcast to the browser. A warning is written to the plugin's <code>canvas logs</code> naming which allowlist variable to populate." %}

<br/>
<br/>
<br/>
