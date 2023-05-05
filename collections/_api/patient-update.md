---
title: "Patient Update"
slug: "patient-update"
excerpt: "Update a patient"
hidden: false
createdAt: "2022-06-24T20:10:09.002Z"
updatedAt: "2022-06-28T15:42:46.781Z"
---
# Attributes that are pulled into Canvas:

This is the exact same schema that is used in the [Patient Create](ref:patient-create). Please refer to that documentation for Patient Update. The only difference is addition of the `id` field used to identify the patient we are updating. 

# How we handle updates/deletions to the identifier, telecom, address, and contact fields:

- Patient Search/Read will include an `id` value for these fields.  
- If the `id` field is included in the iteration, then we will attempt to match to an existing value for that field.
- If the `id` field is **not** included in the iteration, then we will attempt to create a new entry in the database for that field.

- If a `telecom`, `address`, or 'contact' iteration returned via Search/Read  is **not** included in the Update message, then it will be deleted.

## identifier

If an `identifier` already exists in the Canvas database and is **not** included in the Update message, it will be deleted if and only if the `period.end` date is in the future. 

## communication

`communication.language` is an object that contains a coding and a text description. Currently, Canvas only supports the language being set to English. If no language is added, it will default to English. Currently, it cannot be updated. 

## Other fields

If a field is required according to [Patient Create](ref:patient-create), it is also required in the update. If the field is not required and is not added to the update request, the saved data will not be changed.