---
title: Fix issue preventing note locking due to uncommitted commands that are not in the note body
date: 2024-01-04
tags: bugfix
layout: productupdates
---

Canvas offers a config `RESTRICT_SIGNING_NOTE_WITH_UNCOMMITTED_COMMANDS`, which will prevent users from locking notes with uncommitted commands. We have fixed a bug that blocked users from locking notes with the message “To lock this note please commit all uncommitted commands”, in the absence of any visible uncommitted commands in the note. This was caused by a recent update to the logic checking for uncommitted commands in the note. That update is now being rolled back.