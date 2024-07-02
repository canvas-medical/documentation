---
title: Implements FHIR API Breaking Changes
date: 2024-07-02
tags: api
layout: productupdates
---

This release implements the following changes outlined [here](/product-updates/important-dates) and previously communicated via email: 

- For DiagnosticReport read/search, the FHIR API previously returned `entered_in_error` for status. Per the FHIR spec, we now return `entered-in-error`. 
- The FHIR API previously returned the string `null` in the response body for successful create and update interactions. Create and update endpoints now return empty response bodies on successful interactions.
- The FHIR API previously included the version number in the location header of create interaction responses. The version number should only be included by servers that support versioning, which our API does not.The location header now only includes the base URL, the resource type, and the identifier, i.e. `[base]/[type]/[id]`. The `/_history/[vid]` suffix on the location header value is no longer included.