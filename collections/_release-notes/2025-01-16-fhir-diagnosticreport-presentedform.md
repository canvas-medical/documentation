---
title: Fixes FHIR DiagnosticReport resources that do not have attachments
date: 2025-01-16
tags: bugfix api
layout: productupdates
---

We've fixed a recent change that caused FHIR DiagnosticReport resources to have a URL in `presentedForm` even when there
is no document available.
