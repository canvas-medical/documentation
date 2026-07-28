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
| `application_id` | `str \| None` | The identifier of a [Canvas application](/sdk/handlers-applications/) to open (the `<module path>:<ClassName>` identifier, for example `my_plugin.apps:MyApp`); mutually exclusive with `url`. The application must exist, or `apply()` raises a validation error. |
| `target`  | `TargetType` | Where to open the target. Defaults to `SAME_TAB`.                                                 |

{% include alert.html type="warning" content="Exactly one of <code>url</code> or <code>application_id</code> must be provided. Providing neither or both raises a validation error at <code>apply()</code> time." %}

<br/>

## Allowing target URLs

For security, every target is validated against your plugin's `url_permissions` allowlist on the server before the browser navigates, and any target that isn't permitted is blocked.

Internal Canvas paths — relative, same-origin paths that begin with `/`, such as `/panel` or `/patient/{key}` — are always allowed and don't need an allowlist entry. Protocol-relative (`//host`) and backslash-prefixed (`/\host`) targets are rejected, because a browser can resolve them to a different origin.

External absolute URLs must match one of the entries in the `url_permissions` section of your plugin's `CANVAS_MANIFEST.json`. A match is only counted at an origin or path boundary, so an entry of `https://app.example.com` permits `https://app.example.com/orders` but not `https://app.example.com.evil.com`.

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "my_plugin",
  "description": "...",
  "url_permissions": [
    {
      "url": "https://example.com",
      "permissions": ["ALLOW_SAME_ORIGIN"]
    }
  ]
}
```

A redirect only requires that the target URL be allowlisted. The `permissions` values (such as `ALLOW_SAME_ORIGIN` or `SCRIPTS`) apply to embedded content like `LaunchModalEffect` iframes, not to redirects.

<br/>
<br/>
<br/>
