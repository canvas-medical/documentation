---
title: Upcoming Breaking Change - Condition Category Code
date: 2025-11-03
layout: productupdates
tags: breaking-change api
---

The FHIR Condition endpoint is transitioning from using <code>encounter-diagnosis</code> to <code>problem-list-item</code> as the category code, to align with FHIR US Core standards.

Validators have been relaxed to accept <code>problem-list-item</code> as a valid category code. Support for <code>encounter-diagnosis</code> will be discontinued in a future release.

**Action required:** Begin migrating your Condition API calls to use <code>problem-list-item</code> as the category code.

See the [Condition API documentation](/api/condition/) for examples and details. Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)

