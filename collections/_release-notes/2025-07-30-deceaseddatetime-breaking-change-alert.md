---
title: Upcoming Breaking Change - Support for deceasedDateTime Field in FHIR Patient Resource
date: 2025-07-30
layout: productupdates
tags: breaking-change
---

To meet **USCDI v3** requirements, Canvas will begin populating the `deceasedDateTime` field in the FHIR Patient resource starting **August 22, 2025**.

- If `deceasedDateTime` is available, it will be returned.
- If not, the existing `deceasedBoolean` field will continue to be returned.
- Per the FHIR specification, **only one of these fields will be present at a time**.

**Action required:** Clients should ensure their systems can consume either `deceasedDateTime` or `deceasedBoolean`.

Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)
