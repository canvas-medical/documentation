---
title: Requires Patient References in FHIR MedicationRequest Search/Read
date: 2024-04-19
layout: productupdates
tags: api bugfix
---

FHIR Medication Request Search/Read will now exclude prescription records without a patient. These are created via Surecripts as refill requests for patient who are not registered. 