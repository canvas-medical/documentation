---
title: Fixes Deadlock and Race Condition in Plugin Deletion
layout: productupdates
date: 2025-03-04
tags: bugfix plugins sdk

---

We've resolved a deadlock and race condition that occurred when deleting plugins in admin. Previously, a timing issue caused the system to attempt reloading a deleted plugin, leading to installation failures and an indefinite wait state. This fix ensures plugin deletions occur without conflicts.