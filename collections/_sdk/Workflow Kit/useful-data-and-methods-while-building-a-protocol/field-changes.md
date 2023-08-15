---
title: "Field Changes"
slug: "field-changes"
hidden: false
createdAt: "2022-09-09T20:14:24.252Z"
updatedAt: "2022-09-09T20:14:24.252Z"
---
In a protocol you have access to a field `self.field_changes`. This field will give you information about the record that triggered this protocol to run. 

You will see something these fields

- `model_name` will tell you the specific model that corresponds to the change type you selected for your protocol. (For example, if you selected CHANGE_TYPE.APPOINTMENT, you might see `appointment` and `notestatechangeevent` models depending on the action you took for that appointment. 

- `created` is a boolean field to tell you if this record is being created for the first time (true) or if it updating an already existing record (false)

- `deleted` is a boolean field to tell you if this protocol is being triggered by a record being deleted. This currently can happen when you delete a Patient's care team member, address, phone number, email, consent, contact, or address. 

- `fields` is an object showing all the fields that were updated. If the record is being created for the first time it will show the fields going from null to the correct value. 

- `canvas_id` is the ID of the record that might correspond to the object in the `self.patient` recordset

- `external_id` is the UUID of the record that corresponds to the ID you use in our FHIR endpoints to read that record

- `external_identifiers` might display any patient external identifiers
[block:code]
{
  "codes": [
    {
      "code": "{\n    \"model_name\": \"appointment\",\n    \"created\": true,\n    \"deleted\": false,\n    \"fields\": {\n      \"id\": [\n        null,\n        14\n      ],\n      \"externally_exposable_id\": [\n        null,\n        \"00ccf34f-b501-4a36-877b-6a64856c413a\"\n      ],\n      \"patient_id\": [\n        null,\n        3\n      ],\n      \"provider_id\": [\n        null,\n        13\n      ],\n      \"start_time\": [\n        null,\n        \"2022-09-09T23:00:00+00:00\"\n      ],\n      \"duration_minutes\": [\n        null,\n        20\n      ],\n      \"note_id\": [\n        null,\n        26\n      ],\n      \"note_type_id\": [\n        null,\n        1\n      ]\n    },\n    \"canvas_id\": 14,\n    \"external_id\": \"00ccf34f-b501-4a36-877b-6a64856c413a\",\n    \"external_identifiers\": null\n  }",
      "language": "text"
    }
  ]
}
[/block]