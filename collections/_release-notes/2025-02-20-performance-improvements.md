---
title: Performance Upgrades  
layout: productupdates  
tags: ui api plugins sdk  
date: 2025-02-20  
---

This release includes performance improvements for users of the EMR UI, the Fumage FHIR API, and the SDK:
* Eliminates extraneous database queries slowing down Fumage GET requests for QuestionnaireResponses
* Optimizes detection of data changes which trigger plugin events
* Speeds load time of automations, which will result in a faster initial page load time, especially for heavy users of automations
* Improves runtime performance of automations, which will result in faster execution of automations
