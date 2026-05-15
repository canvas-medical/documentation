---
title: Upcoming Breaking Change - Phase 1 of Changes to the FHIR Task Update Endpoint
date: 2025-09-05
layout: productupdates
tags: breaking-change
---

The FHIR Task update endpoint is moving from appending notes to replacing them, to align with RESTful behavior. To support the transition, we introduced a note header with a default of `note-append`. The default will change to `note-replace` on 9/16/25.

**Action required:** Prior to 9/16/25 client code must be updated to send all task notes, or ensure the header is set to note-append to avoid accidental deletion. The `note-append` option will be available until 9/30, at which time support for this behavior will be removed.  

Read more about this change and keep track of upcoming breaking changes [here.](/product-updates/important-dates/)
