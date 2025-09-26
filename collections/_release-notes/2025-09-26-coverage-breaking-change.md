---
title: Upcoming Breaking Change - Coverage | Member vs Subscriber ID
date: 2025-09-26 08:00:00
layout: productupdates
tags: breaking-change
---

## Breaking Change: Coverage Subscriber ID

On **October 14**, the `subscriberId` field in the FHIR Coverage resource will change meaning:

- **Member IDs** are now stored in the `identifier` attribute (live as of 9/25/25)
- The `subscriberId` attribute will represent the **subscriber’s ID** instead, and will be an optional field in Canvas.  If "The patient is the subsciber" radial button is selected the `identifier` (member ID) will equal the `subscriberId` (subscriber ID). 
- The `subscriberId` search parameter will return subscriber IDs.  
- The new `identifier` search parameter will return member IDs.  

**Action required:** Update your API client code to use `identifier` for member IDs before the release date to avoid disruption.  

Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)

