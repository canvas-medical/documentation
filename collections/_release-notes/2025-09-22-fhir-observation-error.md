---
title: 09.22.2025
date: 2025-09-22
layout: productupdates
tags: bugfix api
---

Today’s release includes the following updates:
- Fix the FHIR Observation create endpoint so that it returns a 4XX response with a descriptive error message when the `effectiveDateTime` attribute is not a valid datetime.
