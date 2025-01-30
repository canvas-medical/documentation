---
title: Updates Character Limits
tags: ui sdk bugfix
layout: productupdates
date: 2024-07-23
---

- Autocomplete fields within command headers of SDK commands (instruct, immunization statement, etc.) now have a character limit of 1000. The limit is enforced when adding free text without causing an error. 
- `Comment` within the instruct command now has a character limit of 4000 characters.
- `Medication` and `Sig` within medication statement has been limited to 255 characters to prevent downstream errors in refills.