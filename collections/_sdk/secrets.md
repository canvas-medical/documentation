---
title: "Managing Variables"
slug: "secrets"
hidden: false
---

Canvas provides a secure key-value store that lets your plugins access configuration data — including sensitive secrets such as API tokens — without hardcoding values into source files. Configuration values are declared in your plugin's `CANVAS_MANIFEST.json` as **variables**, set at install time or through the Admin UI, and read from `self.secrets` at runtime.

Each variable can be marked **sensitive** (treated like a secret: not displayed in admin or CLI listings) or **non-sensitive** (a regular configuration value, displayed in plaintext for verification). All variable values are write-only through the CLI and API.


### Declaring Variables in `CANVAS_MANIFEST.json`

Variables are declared in your plugin's `CANVAS_MANIFEST.json` file under the top-level `variables` field. Each variable is an object with a `name` and an optional `sensitive` flag (defaults to `false`). Variables marked as `sensitive: true` are write-only and behave like secrets. These declared variables become available for configuration in the Canvas Admin UI when the plugin is installed.

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
    {"name": "WEBHOOK_URL"},
    {"name": "LOG_LEVEL", "sensitive": false}
  ],
  "tags": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The variable name used in your plugin code |
| `sensitive` | boolean | No | When `true`, marks the variable as sensitive for display purposes (default: `false`) |

#### Legacy `secrets` array (deprecated)

The flat `secrets` array is still accepted for backwards compatibility:

```json
"secrets": ["API_TOKEN"]
```

It emits a deprecation warning during `canvas validate-manifest` and is mapped internally to `variables` entries with `sensitive: false`. To preserve sensitive treatment, migrate to the `variables` schema with `sensitive: true` and re-install the plugin.

{% include alert.html type="warning" content="<b>Deprecation Notice:</b> The legacy <code>secrets</code> array format is deprecated. Use the <code>variables</code> format shown above instead. The legacy format will continue to work but displays a deprecation warning during <code>canvas validate-manifest</code>." %}

> ⚠️ **Pre-existing values default to non-sensitive.** Any plugin secret that existed before Canvas 1.305.0 — or any value configured via the legacy `secrets:` array — is stored with `sensitive: false`. It will appear in plain text in the Admin UI until the owning plugin is migrated to the `variables` schema with `sensitive: true` and re-installed.


### Configuring Variables from the CLI

Set values during install or update them later. Use `--variable` for non-sensitive values and `--secret` for sensitive values; both flags accept `KEY=value` pairs.

Provide values during install:

```console
$ canvas install <plugin_name> --secret API_TOKEN=your_api_token_value --variable LOG_LEVEL=info
```

Update values on an installed plugin:

```console
$ canvas config set <plugin_name> API_TOKEN=abc123 LOG_LEVEL=warn
```

Pass multiple values by repeating the flag:

```console
$ canvas install <plugin_name> \
  --secret API_TOKEN=abc123 \
  --secret WEBHOOK_SECRET=xyz \
  --variable LOG_LEVEL=info
```

#### Listing configured values

Run `canvas config list <plugin_name>` to see which variables are configured for a plugin. Each variable is rendered as `[set]` or `[not set]`, with a `(sensitive)` annotation for sensitive variables. Values themselves are never displayed in the listing.

```console
$ canvas config list my_plugin
  API_TOKEN  [set]  (sensitive)
  LOG_LEVEL  [not set]
```

To read a value, use the Django Admin UI (access is gated by managing-user permissions).

> _The `--variable` flag, `canvas config list` sensitive marking, and Admin UI masking require Canvas CLI 0.146.0 or newer. Upgrade with `pip install --upgrade canvas`._


### Configuring Variables in the Admin UI

After install you can also set values through the Admin interface.

Navigation path:
`Home` › `Plugin_IO` › `Plugins` › `(your plugin)`

Or, go directly to:

```generic
https://<your_canvas_instance>/admin/plugin_io/plugin/<plugin_id>/change/
```
On this page, you will find input fields for each variable defined in your manifest. Sensitive values display as `SENSITIVE` and are no longer rendered in the form HTML — submit a new value to overwrite, or leave the field blank to keep the existing value. Non-sensitive values display their current value and can be edited inline.

<div style="text-align:center;">
  <img src="/assets/images/sdk/secrets/plugins_secrets_settings_with_permissions.png" alt="Setting plugin variables" width="100%">
</div>

Sensitive variables can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its sensitive variables (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change sensitive variable values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI. This ensures that sensitive configuration, such as API tokens, remains visible only to authorized personnel.


### Accessing Variables in Your Plugin

All variables — sensitive and non-sensitive alike — are exposed to your plugin code through `self.secrets`, a Python dictionary keyed by variable name:

```python
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect

class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        api_token = self.secrets["API_TOKEN"]
        webhook_url = self.secrets["WEBHOOK_URL"]
        log_level = self.secrets["LOG_LEVEL"]
        ...
```

This access pattern is unchanged from earlier Canvas versions, so migrating a plugin from the legacy `secrets:` array to the new `variables:` schema requires no handler code changes.
