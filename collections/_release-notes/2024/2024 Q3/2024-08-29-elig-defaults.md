---
title: Set Default Location or Provider for Eligibility Requests. 
date: 2024-08-29
layout: productupdates
tags:  api config ui

---

Eligibility requests currently use your organization's details (name and npi); however, eligibility and benefits may be tied to regional or provider specific enrollment data. You can now set patient defaults that will be used for eligibility purposes from both the patient profile or using the API. [Read more](/api/patient/#create).  

- Eligibility requests will use the organization’s information by default
- If a default location is set, the request will use the location’s information
- Some payers require the provider’s NPI be sent. You can now update the insurer in admin to use the default provider’s information. If the insurer has this setting enabled, and a default provider is not set, you will receive an error when trying to run the eligibility request.

