---
title: Updates Default Country on Patient Create/Update
date: 2024-08-15
layout: productupdates
tags: api
---
When writing or updating patients via FHIR, we were previously setting a patient's country to United States, which did not map to the dropdown in the patient's registration. We have changed the behavior to default to US to match our UI. 