---
title: Resolves Default Reason for Visit (RFV) and Note Type Issue on the FHIR Update Payload
date: 2024-04-19
layout: productupdates
tags:  api bugfix
---

We have resolved an issue in our logic that would update appointmentType and RFV to the associated instance’s default values if these values were omitted from the FHIR update payload. Now, if appointmentType or RFV is omitted from the FHIR Update payload, they are ignored in the message consumer to keep the appointment values as is.