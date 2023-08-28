---
title: Plugins
---

# Plugins

The Plugins API is responsible for managing plugins in the system.

## Events

The following events are emitted:

1.  `canvas_core.plugins.PluginInitialized`{.interpreted-text
    role="py:class"}
2.  `canvas_core.plugins.PluginInitializationFailed`{.interpreted-text
    role="py:class"}

## Plugins Structure

Every plugin should follow the following structure:

``` 
plugin-name/
├── plugin_name/
│   ├── __init__.py
│   └── plugin.py           # Add your plugin code here.
├── pyproject.toml
├── poetry.lock
└── README.md
```

::: note
::: title
Note
:::

Only `sdist` (`.zip` or `.tar.gz` ) and `wheel` (`.whl`) distribution
formats are supported.
:::

## API Reference

::: {.automodule members=""}
canvas_core.plugins
:::
