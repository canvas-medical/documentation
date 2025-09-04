---
title: Upcoming Breaking Change - Phase 1 of changes to the FHIR Task update endpoint
date: 2025-09-04 08:00:00
layout: productupdates
tags: breaking-change
---

The FHIR Task update endpoint is moving from appending notes to replacing them, to align with RESTful behavior. To support the transition, we will be introducing a Prefer header (note-append or note-replace), with the default set to note-replace.

**Action required:** Client code must be updated to send all Task notes, or update the header to note-append to avoid accidental deletion.

Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)
