---
title: "Managing Variables"
slug: "secrets"
hidden: false
---

<<<<<<< HEAD
Canvas provides a key-value store that lets your plugins access configuration without hardcoding values into source files. Variables can be marked as sensitive (for values like API tokens) or non-sensitive (for regular configuration). All variable values are write-only through the CLI and API. This guide covers how to define, configure, and access variables in your plugins.
||||||| 49203add
Canvas provides a secure key-value secret store that allows your plugins to access sensitive information (such as API tokens) without hardcoding them into source files. 
This guide explains how to define, configure, and access secrets within your plugins.
=======
Canvas provides a secure key-value store that lets your plugins access configuration data — including sensitive secrets such as API tokens — without hardcoding values into source files. Configuration values are declared in your plugin's `CANVAS_MANIFEST.json` as **variables**, set at install time or through the Admin UI, and read from `self.secrets` at runtime.

Each variable can be marked **sensitive** (treated like a secret: not displayed in admin or CLI listings) or **non-sensitive** (a regular configuration value, displayed in plaintext for verification).
>>>>>>> main


<<<<<<< HEAD
### Declaring Variables in `CANVAS_MANIFEST.json`
||||||| 49203add
### Declaring Secrets in `CANVAS_MANIFEST.json`
=======
### Declaring variables in `CANVAS_MANIFEST.json`
>>>>>>> main

<<<<<<< HEAD
Variables are declared in your plugin's `CANVAS_MANIFEST.json` file under the top-level `variables` field. Each variable is an object with a `name` and an optional `sensitive` flag. Variables marked as `sensitive: true` are write-only and behave like secrets. These declared variables become available for configuration in the Canvas Admin UI when the plugin is installed.
||||||| 49203add
Secrets are declared in your plugin's `CANVAS_MANIFEST.json` file under the top-level `secrets` field. 
These declared secrets become available for configuration in the Canvas Admin UI when the plugin is installed.
=======
Declare each variable as an object with a `name` and an optional `sensitive` flag (defaults to `false`):
>>>>>>> main

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
<<<<<<< HEAD
  "variables": [
    {"name": "API_TOKEN", "sensitive": true},
    {"name": "WEBHOOK_URL"}
  ],
||||||| 49203add
  "secrets": ["API_TOKEN"],
=======
  "variables": [
    {"name": "API_TOKEN", "sensitive": true},
    {"name": "LOG_LEVEL", "sensitive": false}
  ],
>>>>>>> main
  "tags": {}
}
```

<<<<<<< HEAD
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The variable name used in your plugin code |
| `sensitive` | boolean | No | When `true`, marks the variable as sensitive for display purposes (default: `false`) |
||||||| 49203add
### Configuring Secrets in the Admin UI
=======
#### Legacy `secrets` array (deprecated)
>>>>>>> main

<<<<<<< HEAD
{% include alert.html type="warning" content="<b>Deprecation Notice:</b> The legacy <code>secrets</code> array format is deprecated. Use the <code>variables</code> format shown above instead. The legacy format will continue to work but displays a deprecation warning during <code>canvas validate-manifest</code>." %}

### Configuring Variables in the Admin UI

Once your plugin is installed, you can update variable values through the Admin interface:
||||||| 49203add
Once your plugin is installed, you can update secret values through the Admin interface:
=======
The flat `secrets` array is still accepted for backwards compatibility:

```json
"secrets": ["API_TOKEN"]
```

It emits a deprecation warning during `canvas validate-manifest` and is mapped internally to `variables` entries with `sensitive: false`. To preserve sensitive treatment, migrate to the `variables` schema with `sensitive: true` and re-install the plugin.

> ⚠️ **Pre-existing values default to non-sensitive.** Any plugin secret that existed before Canvas 1.305.0 — or any value configured via the legacy `secrets:` array — is stored with `sensitive: false`. It will appear in plain text in the Admin UI until the owning plugin is migrated to the `variables` schema with `sensitive: true` and re-installed.


### Configuring values from the CLI

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


### Configuring values in the Admin UI

After install you can also set values through the Admin interface.
>>>>>>> main

Navigation path:
`Home` › `Plugin_IO` › `Plugins` › `(your plugin)`

Or, go directly to:

```generic
https://<your_canvas_instance>/admin/plugin_io/plugin/<plugin_id>/change/
```
<<<<<<< HEAD
On this page, you will find input fields for each variable defined in your manifest.
||||||| 49203add
On this page, you will find input fields for each secret defined in your manifest. 
=======

On this page, you will find input fields for each variable declared in your manifest. Sensitive values display as `SENSITIVE` and are no longer rendered in the form HTML — submit a new value to overwrite, or leave the field blank to keep the existing value. Non-sensitive values display their current value and can be edited inline.
>>>>>>> main

<div style="text-align:center;">
  <img src="/assets/images/sdk/secrets/plugins_secrets_settings_with_permissions.png" alt="Setting plugin variables" width="100%">
</div>

<<<<<<< HEAD
Sensitive variables can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its sensitive variables (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change sensitive variable values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI. This ensures that sensitive configuration, such as API tokens, remains visible only to authorized personnel.
||||||| 49203add
Plugin secrets can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its secrets (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change secret values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI. This ensures that sensitive configuration, such as API tokens, remains visible only to authorized personnel.
=======
Plugin secret access can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its values (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI.
>>>>>>> main


<<<<<<< HEAD
### Configuring Variables in the CLI
||||||| 49203add
### Configuring Secrets in the CLI
=======
### Accessing values in your plugin
>>>>>>> main

<<<<<<< HEAD
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
  WEBHOOK_URL = [set]
```

All variables display as `[set]` or `[not set]` to indicate whether a value has been configured. Actual values are never returned through the CLI or API for security reasons. To view variable values, use the Django admin interface (requires managing user permissions).

### Accessing Variables in Your Plugin

Variables defined in your manifest and configured in the admin UI are exposed to your plugin code through `self.secrets`.
This is a Python dictionary containing all variable values, including both sensitive and non-sensitive variables.
||||||| 49203add
You can set secrets either after a plugin is installed or as part of the install.
Secrets must be listed under the secrets field in the plugin’s `CANVAS_MANIFEST.json`.

Set (or update) secrets on an installed plugin:
```console
$ canvas config set <plugin_name> API_TOKEN=your_api_token_value
```

Provide secrets during install:
```console
$ canvas install <plugin_name> --secret API_TOKEN=your_api_token_value
```

Set multiple secrets:

```console
# Pass multiple key=value pairs. 
$ canvas config set <plugin_name> API_TOKEN=abc123 OTHER_KEY=xyz

# For installs, repeat --secret
$ canvas install <plugin_name> \
  --secret API_TOKEN=abc123 \
  --secret OTHER_KEY=xyz
```

### Accessing Secrets in Your Plugin

Secrets defined in your manifest and configured in the admin UI are exposed to your plugin code through the `self.secrets`. 
This is a Python dictionary containing all secret values.
=======
All variables and secrets — sensitive and non-sensitive alike — are exposed to your plugin code through `self.secrets`, a Python dictionary keyed by variable name:
>>>>>>> main

```python
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect

class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        api_token = self.secrets["API_TOKEN"]
<<<<<<< HEAD
        webhook_url = self.secrets["WEBHOOK_URL"]
||||||| 49203add
=======
        log_level = self.secrets["LOG_LEVEL"]
>>>>>>> main
        ...
```

This access pattern is unchanged from earlier Canvas versions, so migrating a plugin from the legacy `secrets:` array to the new `variables:` schema requires no handler code changes.
