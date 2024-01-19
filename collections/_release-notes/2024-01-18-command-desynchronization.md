---
title: Fix Desynchronization Issues Affecting the Plan Command
date: 2024-01-18
tags: bugfix ui
layout: productupdates
---

Our recent work to migrate the plan command introduced an issue where the models relating to the command were out of sync. To end users, this looked like a gray loading box in the note that never rendered. We have included a fix we expect to prevent these issues going forward. 