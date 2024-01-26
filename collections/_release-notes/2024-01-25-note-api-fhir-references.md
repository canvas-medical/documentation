---
title: Reference Note Objects in our FHIR API
tags: beta api
date: 2024-01-25
---

Some of our endpoints allow you to insert commands into notes by including an encounter reference; however, some of our note types do not create encounters (e.g. data import). A note object reference, surfaced by the new [Note API](/product-updates/note-api), has been added to those same endpoints to facilitate adding the commands to additional note types. The reference has also been added to support capturing the associated note ID for encounters, appointments, documents associated with notes, and resources that have been added to a note. 




