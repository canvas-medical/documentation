---
title: Fixes to SDK Commands 
layout: productupdates
tags: bugfix ui sdk beta 
date: 2024-04-03
---


We have made update to several SDK commands to address various bugs.  The fixes include:

**Questionnaire**
- The most recent version of the questionnaire will now be used in automations
- Keyboard navigation improvements
- Values entered in the questionnaire loader are now accurately represented in the command upon origination. 
- Blank free text responses will no longer print with the question name  (i.e ~TXT~)
- The click target on multiline single select and free text responses has been expanded.
- Automations created before the carry forward setting is enabled now respect the setting after its enabled.

**Reason for Visit**
- The SDK Reason for Visit Command is now compatible with FHIR Appointment Create/Update

**Assess**
- The background field will carry forward as it should when originating the assess command within a note.