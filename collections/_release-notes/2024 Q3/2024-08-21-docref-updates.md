---
title: Updates FHIR DocumentReference Create
date: 2024-08-21
layout: productupdates
tags: api bugfix
---
The following updates have been made to the FHIR DocumentReference Create interaction:
- Added support for the Uncategorized Clinical Document `type` (34109-9).
- Added logic to default the priority extenstion to false, if not explicitly set.
- Fixed a bug that caused the review workflow to not be triggered in Canvas when review mode was set to review required (`rr`).

[Read more.](/api/documentreference/#create)

