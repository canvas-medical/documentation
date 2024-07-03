---
title: Adds Temporary Extensions to all FHIR Attachments
date: 2024-04-29
layout: productupdates
tags: api
---
We have added a temporary extension to the Attachment attributes for the following resources: Consent, DocumentReference, DiagnosticReport, Media, Patient, and Practitioner. The `url` attribute on Attachments will require bearer authentication in the near future. The temporary extension is meant to support the transition. We encourage you to update your workflow to use the temporary extension as soon as possible. We will then release the change to the existing attribute and give a window of time to move off of the temporary extension. [Read more](/product-updates/important-dates)