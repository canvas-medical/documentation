---
title: "Managing Variables"
slug: "secrets"
hidden: false
---

Canvas provides a key-value store that lets your plugins access configuration without hardcoding values into source files. Variables can be sensitive (like API tokens, which are write-only) or non-sensitive (for regular configuration). This guide covers how to define, configure, and access variables in your plugins.


### Declaring Variables in `CANVAS_MANIFEST.json`

Variables are declared in your plugin's `CANVAS_MANIFEST.json` file under the top-level `variables` field. Each variable is an object with a `name` and an optional `sensitive` flag. Variables marked as `sensitive: true` are write-only and behave like secrets. These declared variables become available for configuration in the Canvas Admin UI when the plugin is installed.

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "live_notifications",
  "description": "Edit the description in CANVAS_MANIFEST.json",
  "components": {
    "handlers": [
      {
        "class": "live_notifications.handlers.my_handler:Handler",
        "description": "A handler that does xyz..."
      }
    ]
  },
  "variables": [
    {"name": "API_TOKEN", "sensitive": true},
    {"name": "WEBHOOK_URL"}
  ],
  "tags": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The variable name used in your plugin code |
| `sensitive` | boolean | No | When `true`, the variable is write-only (default: `false`) |

{% include alert.html type="warning" content="<b>Deprecation Notice:</b> The legacy <code>secrets</code> array format is deprecated. Use the <code>variables</code> format shown above instead. The legacy format will continue to work but displays a deprecation warning during <code>canvas validate-manifest</code>." %}

### Configuring Variables in the Admin UI

Once your plugin is installed, you can update variable values through the Admin interface:

Navigation path:
`Home` › `Plugin_IO` › `Plugins` › `(your plugin)`

Or, go directly to:
```generic
https://<your_canvas_instance>/admin/plugin_io/plugin/<plugin_id>/change/
```
On this page, you will find input fields for each variable defined in your manifest.

<div style="text-align:center;">
  <img src="/assets/images/sdk/secrets/plugins_secrets_settings_with_permissions.png" alt="Setting plugin variables" width="100%">
</div>

Sensitive variables can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its sensitive variables (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change sensitive variable values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI. This ensures that sensitive configuration, such as API tokens, remains visible only to authorized personnel.


### Configuring Variables in the CLI

You can set variable values either after a plugin is installed or during install.
Variables must be listed under the `variables` field in the plugin’s `CANVAS_MANIFEST.json`.

**Set (or update) variables on an installed plugin:**
```console
$ canvas config set <plugin_name> API_TOKEN=your_api_token_value WEBHOOK_URL=https://example.com
```

**Provide variable values during install:**

Use `--variable` for non-sensitive variables and `--secret` for sensitive variables:
```console
$ canvas install <plugin_name> \
  --secret API_TOKEN=abc123 \
  --variable WEBHOOK_URL=https://example.com
```

You can also use `--secret` for all variables if you prefer a single flag—values passed with `--secret` are treated as sensitive.

**List configured variables:**
```console
$ canvas config list <plugin_name>
  API_TOKEN = [set]  (sensitive)
  WEBHOOK_URL = https://example.com
```

Sensitive variables display as `[set]` or `[not set]` without revealing their values. Non-sensitive variables display their actual values.

### Accessing Variables in Your Plugin

Variables defined in your manifest and configured in the admin UI are exposed to your plugin code through `self.secrets`.
This is a Python dictionary containing all variable values, including both sensitive and non-sensitive variables.

```python
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect

class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        api_token = self.secrets["API_TOKEN"]
        webhook_url = self.secrets["WEBHOOK_URL"]
        ...
```
