---
title: Update to FHIR Appointment Endpoint
date: 2024-01-05 20:30:00
tags: api 
layout: productupdates
---

The [FHIR Appointment](/api/appointment) endpoint now uses a reference from the Location Read/Search endpoint for the Location in supportingInformation.  We will continue to support using the integer value when creating or updating appointment for a set period before the current functionality is deprecated. Updates on the end of life for the existing functionality can be tracked [here](/product-updates/upcoming-changes). 