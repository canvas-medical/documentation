---
title: Updates Resource Attachment File URLs
tags: api breaking-change
layout: productupdates
date: 2024-12-05
---

The FHIR spec does not allow expiring pre-signed URLs for resource attachments. Going forward, HTTP clients that request resource attachment files will need to provide a bearer token in the request. The affected resources are Consent, DocumentReference, DiagnosticReport, Media, Patient, and Practitioner. Unless otherwise specified, the responses for these requests will be a temporary redirect to the pre-signed URLs. We have added a temporary extension to the Attachment attribute in each resource that includes the pre-signed URLs to support the transition. [Stay up to date on breaking changes.](/product-updates/important-dates/)