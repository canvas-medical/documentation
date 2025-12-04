---
title: Fixes Firing of NOTE_STATE_CHANGE_EVENT_CREATED  
layout: productupdates  
tags: bugfix plugins sdk  
date: 2025-02-27  
---

Fixed an issue where we were failing to emit the `NOTE_STATE_CHANGE_EVENT_CREATED` event.  These events now fire with the note_id, patient_id, and new note state in the event context.  
