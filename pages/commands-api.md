---
permalink: /product-updates/commands-api/
layout: betas
title: "Beta | Commands API"
date: 2024-02-07
---

{% include alert.html type="warning" content= "<b>Beta Participation: </b>This is a closed beta at this time."  %}

## Overview

Many customers have needs to manage the contents of the timeline via the API - either to pre-chart for clinicians or to add content from external sources. Our Commands API is an externally-facing API that will provide a leap towards that world by allowing you to read, search, create, and update all of our commands via API.

- Fully or partially filled out commands can be added to [notes](/product-updates/note-api/){:target="_blank"} in either a committed or uncommitted state. 
- Commands can be added to [encounter, review, or data import notes](/documentation/appointment-and-note-types){:target="_blank"}. It is important to note that encounter and review notes must be unlocked and should not be deleted.
- Existing commands can be read by UUID or searched for using extensive query params. 
- The content of existing uncommitted commands can be updated. 
- Uncommitted commands can be committed or deleted. 
- Committed commands can be entered-in-error. 

The commands API will be available for commands that have been [migrated to the commands module](/product-updates/commands-module/#progress){:target="_blank"} of the SDK. We will update the tracker with progress, as new commands are released and available. 


## Expected Use Cases
- Write commands that are not currently availble via our FHIR endpoints to a note, like family history, surgical history, HPI, plan. 
- Read commands and surface the content in your patient experience. (e.g. Patient Instructions) 
- Support seamless integrations with AI scribes
