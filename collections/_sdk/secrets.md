---
title: "Managing Secrets"
slug: "secrets"
hidden: false
---

Canvas provides a secure key-value secret store that allows your plugins to access sensitive information (such as API tokens) without hardcoding them into source files. 
This guide explains how to define, configure, and access secrets within your plugins.


### Declaring Secrets in `CANVAS_MANIFEST.json`

Secrets are declared in your plugin's `CANVAS_MANIFEST.json` file under the top-level `secrets` field. 
These declared secrets become available for configuration in the Canvas Admin UI when the plugin is installed.

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "live_notifications",
  "description": "Edit the description in CANVAS_MANIFEST.json",
  "components": {
    "handlers": [
      {
        "class": "live_notifications.handlers.my_protocol:Protocol",
        "description": "A handler that does xyz..."
      }
    ]
  },
  "secrets": ["API_TOKEN"],
  "tags": {}
}
```

### Configuring Secrets in the Admin UI

Once your plugin is installed, you can update secret values through the Admin interface:

Navigation path:
`Home` › `Plugin_IO` › `Plugins` › `(your plugin)`

Or, go directly to:
```generic
https://<your_canvas_instance>/admin/plugin_io/plugin/<plugin_id>/change/
```
On this page, you will find input fields for each secret defined in your manifest. 

<div style="text-align:center;">
  <img src="/assets/images/sdk/secrets/plugins_secrets_settings_with_permissions.png" alt="Setting plugin secrets" width="100%">
</div>

Plugin secrets can be protected by managing user permissions. Only users explicitly assigned as "managing users" for a plugin can view or modify its secrets (as well as other sensitive settings like the plugin package file download link). Other users can see basic plugin details and enable or disable plugins, but they will not be able to access or change secret values. To add or remove managing users for a plugin, use the "Managing users" section on the plugin detail page in the Admin UI. This ensures that sensitive configuration, such as API tokens, remains visible only to authorized personnel.


### Configuring Secrets in the CLI

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

```python
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.effects import Effect

class MyHandler(BaseHandler):
    def compute(self) -> list[Effect]:
        api_token = self.secrets["API_TOKEN"]
        ...
```
