---
title: Plugins can know what instance they are executing on
tags: sdk
layout: productupdates
date: 2025-04-08
---

Plugins can now know which instance they are being executed on via the
`self.environment` dictionary available in event handlers. As an example, if a
plugin is being executed on the `canvas-test.canvasmedical.com` instance,
`self.environment` would look like:

```python
{
    "CUSTOMER_IDENTIFIER": "canvas-test"
}
```

But if the same plugin was executed on the `canvas-staging.canvasmedical.com`
instance, `self.environment` would look like:

```python
{
    "CUSTOMER_IDENTIFIER": "canvas-staging"
}
```
