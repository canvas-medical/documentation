---
title: DiagnosticReport now contains the associated PDF
layout: productupdates
date: 2023-12-14
tags: api 
---

Previously, for lab reports and imaging reports, there was a DocumentReference resource which contained the PDF, and separately a DiagnosticReport resource which contained other information including codings. There was no way to link the two together. This made it difficult for developers to identify what a given DocumentReference PDF contained. Now, we have added the PDF for the report to the DiagnosticReport in the presentedForm attribute. The PDF will also continue to be surfaced as a DocumentReference per FHIR guidance. [Read more.](/api/diagnosticreport/)