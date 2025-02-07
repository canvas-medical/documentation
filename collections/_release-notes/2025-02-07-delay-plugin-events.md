---
title: Adds Delay Before Emitting PLUGIN_CREATED and PLUGIN_UPDATED Events  
layout: productupdates  
tags: bugfix plugins  
date: 2025-02-07  
---

When a plugin is created or updated, we emit the `PLUGIN_CREATED` and `PLUGIN_UPDATED` events. These events were firing immediately, which means the plugin likely wasn’t installed at the time the event was emitted. This change introduces a delay before emitting these specific events, which should make this problem appear less frequently. A more durable fix will be implemented in the future.



