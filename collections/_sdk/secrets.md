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
    "protocols": [
      {
        "class": "live_notifications.protocols.my_protocol:Protocol",
        "description": "A protocol that does xyz...",
        "data_access": {
          "event": "",
          "read": [],
          "write": []
        }
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
```
https://<your_canvas_instance>/admin/plugin_io/plugin/<plugin_id>/change/
```
On this page, you will find input fields for each secret defined in your manifest. 

<div style="text-align:center;">
  <img src="/assets/images/sdk/secrets/plugins_secrets_setting.png" alt="Setting plugin secrets" width="100%">
</div>


### Accessing Secrets in Your Plugin

Secrets defined in your manifest and configured in the admin UI are exposed to your plugin code through the `self.secrets`. 
This is a Python dictionary containing all secret values.

```python
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects import Effect

class Protocol(BaseProtocol):
    def compute(self) -> list[Effect]:
        api_token = self.secrets["API_TOKEN"]
        ...
```
