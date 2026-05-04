---
title: Adds Option to Install Plugins in Disabled State
layout: productupdates
tags: plugins sdk cli
date: 2026-05-04
---

Plugins can now be installed in a disabled state. The package uploads but handlers do not run until the plugin is enabled. Both methods default to enabled, preserving existing behavior.

**Admin UI:** The plugin upload page now includes an "Is enabled" checkbox. Uncheck it to install the plugin disabled; enable it later from the Plugins admin page.

**CLI:** The `canvas install` command now supports an `--enable/--disable` flag. Use `--disable` to install a plugin without activating it:

```console
$ canvas install ./my-plugin --disable
```
