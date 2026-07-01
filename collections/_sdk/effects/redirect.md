---
title: "Redirect"
slug: "redirect-effect"
excerpt: "Effect for navigating the Canvas frontend to an internal path or external URL"
hidden: false
---

## Overview

The `RedirectEffect` navigates the Canvas frontend to a URL. Return it from a plugin handler to send the user to another location — either an internal Canvas path or an external site — in the same browser tab or a new one.

Your plugin builds the full target string in Python, so it can include patient or note identifiers. The target can be an internal Canvas path (for example, `/panel` or `/patient/{key}?...`) or an external URL (for example, `https://example.com`).

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
| `url`     | `str`        | The target to navigate to. Required and must be non-empty. An internal Canvas path or external URL. |
| `target`  | `TargetType` | Where to open the target. Defaults to `SAME_TAB`.                                                 |

<br/>

## Allowing target URLs

For security, target URLs are validated against your plugin's `url_permissions` allowlist on the server before the browser navigates. Any target that is not covered by the allowlist is blocked. External URLs you redirect to must be listed in the `url_permissions` section of your plugin's `CANVAS_MANIFEST.json`.

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

<br/>
<br/>
<br/>
