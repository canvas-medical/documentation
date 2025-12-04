---
title: Use self.event.target.id and self.event.context as Replacements for Deprecated Methods
tags: plugins
layout: product updates
date: 2025-01-06
---

Plugin Developers should now use `self.event.target.id` and `self.event.context` instead of `self.target`  and `self.context` . Those methods are deprecated and they will be removed in a future major release. `self.event.target`  now allows to access the targeted instance via `self.event.target.instance` if the model is already supported in the SDK
