---
title: "Applications"
slug: "handlers-applications"
excerpt: "Launch external content within the EHR from the app drawer."
hidden: false
---

Applications are accessible in the app drawer and launch your content when
clicked. Applications can be patient specific, or global.

## Implementing an Application

To add an application, your handler class should inherit from  the
`Application` class.

Your class must implement the `on_open()` method. In most cases, you will
return a `LaunchModalEffect`, with either a URL you wish to iframe into the
Canvas UI or HTML to be rendered in that iframe directly.

Here is an example of an implemented application class:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.application import Application


class IFrameApp(Application):
    def on_open(self) -> Effect:
        return LaunchModalEffect(url=f"https://www.canvasmedical.com/extensions",
            target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE).apply()
```

In addition, your `CANVAS_MANIFEST.json` file must provide some information
about your application. You reference your class in the "applications"
section of the components so your application is registered in the app drawer
on plugin installation.

This is also where you can define the title and icon that displays your
app in the app drawer. The icon will be rendered at 48px by 48px, so should be
square and simple enough to not lose detail at that size.

Other information you can define about your application is the `scope`
(`"patient_specific"` or `"global"`), which determines if the application is
visible only in a patient chart or outside of charts, and `origins`, which
is what give the browser permission to load the content of your iframe. You
must list the domains that will be loaded within the iframe, or they will not be
rendered.

Here's what your `CANVAS_MANIFEST.json` might look like:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "my_application",
    "description": "This is a very nice application",
    "components": {
        "protocols": [],
        "applications": [
            {
                "class": "my_application.apps.iframe:IFrameApp",
                "name": "My Application",
                "description": "Test App for patients",
                "icon" : "/assets/cappuccino.png",
                "scope": "patient_specific",
                "origins": ["http://example.com"]
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```


<br/>
<br/>
<br/>
<br/>
