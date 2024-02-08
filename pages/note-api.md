---
permalink: /product-updates/note-api/
title: "Beta | Note API"
layout: betas
date: 2024-01-22
---

{% include alert.html type="warning" content= "<b>Beta Participation:</b> This beta is open to all users of Canvas. The documentation is linked below. Please direct questions or feedback to product@canvasmedical.com."  %}

## Overview

The new [Note API](/api/note) allows customers to create and update notes. The effect of creating a note is the same as creating a note in the user interface (for example for a note with category “encounter” will create an encounter, a note that is billable will create a claim). Not all note attributes can be modified on update. For example, note type cannot be changed after note creation.

_Why a custom API, why not a FHIR API?_

The primary purpose of FHIR is to achieve interoperability. The Note API, however, does not focus on interoperability. Instead, it provides you with precise control over the Canvas system through an API. Canvas notes are unique due to our use of narrative charting and commands. They are not intended to be generic concepts that can be transferred between EMRs. You might argue that notes should be interoperable, and we agree. That's why we make note PDFs available through our DocumentReference endpoint. The Note API is designed for aspects of notes that we don't expect to be interoperable, but that we want to offer more specific API control over.

## Expected Use Cases

- Create notes via API, including encounter-category notes like Office visits, Chart reviews, and Data import notes.
- Read/search the list of notes associated with a patient, and obtain the permalinks to those notes, to better integrate external systems with the Canvas timeline.
- Edit metadata associated with notes, including titles.
- Reference notes as part of FHIR API write operations to land the associated commands into the note of your choosing.

### Patient Intake Example

Let’s say you want to add two medications (Lisinopril, Hydrochlorothiazide) and a condition (Hypertension) to a patient chart based on intake forms. Here is an elegant way to do this taking advantage of this new functionality:

1. Create a data import note (using POST Note)
2. Change the title of the data import note (using PATCH Note) to something informative like: “Added lisinopril, hydrochlorothiazide, and hypertension”
3. Add the data to that note using (POST MedicationStatement and POST Condition, both referencing the note in the new note extension).

The net result is that you have a well-named Data Import note with all of the new data consolidated in it. A big improvement from three separate un-named Data import notes, which was prior state.

