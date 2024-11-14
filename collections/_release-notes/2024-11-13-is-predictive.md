---
title: Adds `Is Predictive` Attribute
date: 2024-11-13
tags: beta plugins sdk
layout: productupdates
---
When implementing plugins, the ClinicalQualityMeasures base class is what determines what gets registered in the protocols, protocoluploads, protocoluploadversions, and protocolsused tables. We added a new attribute that can be set when using this class that allows developers to indicate that a protocol contains predictive decision support interventions. 