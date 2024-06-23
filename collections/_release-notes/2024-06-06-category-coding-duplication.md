---
title: Prevents Duplication of Category when Saving Diagnostic Reports
layout: productupdates
tags: bugfix api
date: 2024-06-06
---

CategoryCoding objects for diagnostic reports were being created on every save, causing duplication apparent within the FHIR DiagnosticReport search interaction. This has been fixed. 