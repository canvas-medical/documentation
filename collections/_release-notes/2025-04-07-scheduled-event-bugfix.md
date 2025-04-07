---
title: Fix Scheduled Events created via FHIR from making a timeline chart entry
tags: api
layout: productupdates
date: 2025-04-07
---

Previously when creating a FHIR Appointment using a scheduled event type, if a patient was supplied it was creating a note on the patient’s timeline. This fix will make the scheduled events created via FHIR behave similarly to events created directly in the Canvas UI and not create a timeline note. 