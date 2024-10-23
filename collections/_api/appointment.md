---
title: Appointment
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Appointment
        article: "a"
        description: >-
          A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).<br><br>
          [https://hl7.org/fhir/R4/appointment.html](https://hl7.org/fhir/R4/appointment.html)
          <br><br>
          This may result in one or more [Encounters](/api/encounter).<br><br>
          The appointment resource maps to both [patient appointments](https://canvas-medical.zendesk.com/hc/en-us/articles/11714510225427-Multi-provider-Scheduling) as well as [other events](https://canvas-medical.zendesk.com/hc/en-us/articles/15704289792659-Scheduling-Other-Events-) in Canvas. Instructions for configuring appointment and note types can be found [here](/documentation/appointment-and-note-types).
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            required_in: update
            exclude_in: create
            description: The identifier of the appointment.
          - name: contained
            type: array[json]
            description_for_all_endpoints: >-
              Contained, inline Resources. Used to store links for telehealth appointments. 
            read_and_search_description: There will be a reference in the `supportingInformation` attribute with a `type` of `Endpoint` and a reference` of `#appointment-meeting-endpoint-0` that will match the `contained[0].id`.
            create_and_update_description:
              This endpoint allows one custom video meeting link to be passed in that will be utilized on the UI over the default provider's meeting link if the appointment is a telemedicine. You can specify a telehealth meeting link by adding an element in the `SupportingInformation` attribute where the `SupportingInformation.reference` is `#appointment-meeting-endpoint-0` and matches the `contained[0].id` attribute of `appointment-meeting-endpoint-0`. See examples for help.
            attributes:
              - name: resourceType
                required_in: create, update
                type: enum [ Endpoint ]
              - name: id
                required_in: create, update
                type: string
                description: The `id` of the contained entry. This needs to be `appointment-meeting-endpoint-0` and the SupportingInformation.reference will be `#appointment-meeting-endpoint-0`.
              - name: status
                type: enum [ active ]
                exclude_in: create, update
              - name: connectionType
                type: json
                exclude_in: create, update
                attributes: 
                  - name: code
                    type: string
                    description: Protocol/Profile/Standard to be used with this endpoint connection
              - name: payloadType
                type: array[json]
                exclude_in: create, update
                attributes:
                  - name: coding
                    type: array[json]
                    attributes:
                      - name: code
                        type: enum [ video-call ]
              - name: address
                type: string
                required_in: create, update
                description: The technical base address for connecting to this endpoint.
          - name: extension
            type: array[json]
            exclude_in: create, update
            read_and_search_description: Canvas supports a note identifier extension on this resource for read and search interactions. The note identifier can be used with the [Canvas Note API](/api/note).
            attributes:
                - name: url
                  type: string
                  description: Reference that defines the content of this object.
                  enum_options:
                    - value: http://schemas.canvasmedical.com/fhir/extensions/note-id
                - name: valueId
                  type: string
                  description: The valueId field is used for the Note extension and will be the note's unique identifier.
          - name: identifier
            type: array[json]
            description_for_all_endpoints: >-
              External Ids for this item. <br><br>
              The identifier list defines additional identifiers that are able to be stored for an appointment.<br><br>These identifiers will not be surfaced on the Patient's chart, but they may help you identify the patient in your system by associating your identifier with the resource's `id`.
            update_description: >-
              To update an existing `identifier`, include the `id` in the `identifier[x].id` field returned from Read/Search.<br><br>
              The `identifier` section sent in an update will entirely replace existing identifiers currently within the period.start and period.end dates.<br><br>
              If an `identifier` already exists in the Canvas database and is not included in the Update message, it will be deleted if and only if the period.end date is in the future.
            attributes:
              - name: id
                type: string
                exclude_in: create
                description: Unique id for inter-element referencing
              - name: use
                type: enum [ usual | official | temp | secondary | old ]
                description: The purpose of this identifier. If this is omitted, it will default to `usual`.
              - name: system
                type: string
                description: The namespace for the identifier value.
              - name: value
                type: string
                description: The value that is unique
              - name: assigner
                type: json
                exclude_in: read, search
                description: Text representing Organization that issued id. If ommitted it will default to the system of the identifier.
                attributes:
                  - name: display
                    type: string
              - name: period
                type: json
                description: Time period when id is/was valid for use.
                attributes: 
                  - name: start
                    type: datetime
                    description: Starting time with inclusive boundary. If omitted this will default to `1970-01-01`.
                  - name: end
                    type: datetime
                    description: End time with inclusive boundary, if not ongoing. If ommitted this will default to `2100-12-31`.
          - name: status
            type: enum [ arrived | booked | cancelled | checked-in | fulfilled | noshow | pending | proposed | entered-in-error ]
            required_in: create,update
            description_for_all_endpoints: >-
              The status of the appointment. <br><br> 

              This table shows the mappings of statuses/states an appointment is in within Canvas to the FHIR status attribute. <br>


                | FHIR Status      | Canvas Status |
                | ---------------- | :------------ |
                | proposed         | unconfirmed   |
                | pending          | attempted     |
                | booked           | confirmed     |
                | arrived          | arrived       |
                | checked-in       | roomed        |
                | fulfilled        | exited        |
                | noshow           | no-showed     |
                | cancelled        | cancelled     |
                | entered-in-error | deleted       |


            read_and_search_description: >-
              The first 7 statuses come from the dropdown on the Appointment Card in the Schedule view. A `cancelled` status comes from a patient appointment or an other event being cancelled. The `deleted/entered-in-error` status is when a checked-in appointment note has been deleted in Canvas.
            create_description: >-
              If any of the first 7 FHIR statuses are used, the appointment will appear on the schedule  from the dropdown on the Appointment Card in the Schedule view with one of those statuses. <br><br>An appointment can be created as `cancelled` for historical purposes, but it will not appear on the schedule view and will be a restorable note on the patient's timeline. <br><br>
              The Create endpoint does NOT accept a status of `entered-in-error`.
            update_description: >-
              If any of the first 7 FHIR statuses are used, the appointment will appear on the schedule  from the dropdown on the Appointment Card in the Schedule view with one of those statuses. <br><br>An appointment can be updated to `cancelled` and as a result it will disappear from the schedule view and/or will be a restorable note on the patient's timeline. Once an appointment is in a cancelled state, it should not be updated to a different status via FHIR, instead the note should be reverted directly in the Patient's chart before it can be updated via FHIR again. <br><br>
              The Update endpoint does NOT accept a status of `entered-in-error`. 
          - name: appointmentType
            type: json
            description_for_all_endpoints: >-
              The style of appointment or patient that has been booked in the slot (not service type). Canvas supports configurable [apppointment and note types](/documentation/appointment-and-note-types/).
            create_description: >-
              There are a few things to note with this attribute: <br><br>

                1.If the `appointmentType` attribute is omitted from the body completely, the note type that has `Is default appointment type` will be used (usually Office Visit if unchanged)<br><br>
                2.If the code / system pair does not exist, you will see a 422 error status with error message `Appointment Type does not exist with code: {code} and system: {system}` <br><br>
                3.If the code / system pair passed is not marked as `Is Scheduleable` in Canvas, you will get a 422 error status with error message `Note type: {name} is not scheduleable`.
            update_description: >-
              There are a few things to note with this attribute: <br><br>

                1. If the `appointmentType` is an Other Event that does not require a patient, you must provide the `appointmentType` in the upload payload to pass validation. <br><br>
                2. For all appointments that require a patient, if the `appointmentType` attribute is omitted from the body completely on an update, the note type will stay as it already is in Canvas.<br><br>
                3. If the code / system pair does not exist, you will see a 422 error status with error message `Appointment Type does not exist with code: {code} and system: {system}` <br><br>
                4. If the code / system pair passed is not marked as `Is Scheduleable` in Canvas, you will get a 422 error status with error message `Note type: {name} is not scheduleable`.
            attributes:
              - name: coding
                type: array[json]
                description: >-
                  The type of appointment
                attributes:
                  - name: system
                    description: >-
                      The system of the appointment
                    type: string
                  - name: code
                    description: >-
                      The code of the appointment. <br><br>
                      This needs to match a coding in the Appointment and Note Types Canvas Settings and be deemed as Is Scheduleable. 
                    type: string
                  - name: display
                    exclude_in: create, update
                    description: >-
                      The display of the appointment
                    type: string
          - name: reasonCode
            type: array[json]
            description_for_all_endpoints: >-
              Coded reason this appointment is scheduled. <br><br>Canvas supports two ways to specify the reason for vist (RFV): [structured](/documentation/reason-for-visit-setting-codings) and unstructured. Both the `coding` and `text` attributes are used for Structured RFVs, whereas unstructured RFVs only leverage the `text` attribute.
            create_description:
              Canvas only accepts the first item in the reasonCode list.<br><br>

              If you are taking advantage of our [structured reason for visit](/documentation/reason-for-visit-setting-codings) feature, you can provide a `coding` that Canvas can use to look up the `code` value in configured in settings and display the structured RFV matching that code. If `Appointment.reasonCode[0].coding[0].code` is not a valid ReasonForVisitSettingCoding you will get the error "structured reason for visit with code {code} does not exist". You will also receive an error if the RFV code in Canvas' setting's page is not unique. <br><br> 

              The `text` attribute maps to the free text Reason For Visit command.  If you are using the structured reason for visit feature, this text will display as the `comment` in the command.  If you are not using the structured reason for visit feature, then only `Appointment.reasonCode[0].text` needs to be populated in your message and `coding` should be omitted. <br><br>

              If this field is omitted (along with the deprecated `description` field), the RFV command in the appointment note will be defaulted to `No description given`.
            update_description:
              On an update, if the reasonCode has changed from what is already saved in Canvas, it will create a new RFV command on that appointment. The old reason for visit will be marked as entered-in-error, and the text will no longer display. Below is an example of what an appointment's note will look like after changing the description multiple times. The originator and entered-in-error will be set to Canvas Bot, which can be seen if you click on the crossed off "Reason for Visit".<br><br>![api-update-rfv](/assets/images/api-update-rfv.png){:width="90%"}<br><br>
              If this field is omitted (along with the deprecated `description` field), the RFV command in the appointment note will stay as it currently is.
            attributes:
              - name: coding
                type: array[json]
                description: Code defined by a terminology system.
                attributes: 
                  - name: system
                    exclude_in: create, update
                    description: The system of the coding.
                    type: string
                  - name: code
                    description: The code of the reason for visit.  
                    type: string
                  - name: display
                    exclude_in: create, update
                    description: The display name of the coding.
                    type: string
                  - name: userSelected
                    exclude_in: create, update
                    description: If this coding was chosen directly by the user. In Canvas this indicates if the coding is currently active or not.
                    type: boolean
              - name: text
                type: string
          - name: description [deprecated]
            type: string
            description: >-
              Shown on a subject line in a meeting request, or appointment list.<br><br>
              **Note:** This field is being deprecated in favor of `reasonCode`. The text in `reasonCode` and this description attribute will always match.
          - name: supportingInformation
            required_in: create,update
            type: array[json]
            description: >-
              Additional information to support the appointment. Currently, Canvas supports different types of references in this list: <br>

                1. `Location`: A reference to a Location captures what Practice Location in Canvas the appointment will take place at.<br>
                2. `Meeting Link`: For appointments that are telehealth in Canvas, there will be a reference to an endpoint in this list. The reference attribute will match an `id` in the `Appointment.contained` attribute list. That element will display the url address of the virtual meeting link. <br>
                3. `Appointment`: If an appointment has been rescheduled, this list could display an associated Appointment reference. If you see a display of `Previously Rescheduled Appointment`, it means that the appointment you are currently looking at was created after rescheduling the appointment in that Reference. If you see a display of `Rescheduled Replacement Appointment`, it means that the appointment you are currently looking at is now outdated by a new appointment. If you see a display of `Co-scheduled Appointment`, it means that the appointment you are currently looking at was scheduled with other additional associated appointments for which the appointment reference ID is noted. <br>
                4. `Encounter`: If there is any encounter associated with the appointment made in Canvas, the reference will appear in this list.
            create_and_update_description: >-
              Additional information to support the appointment. Currently, Canvas supports the ability to write 2 different types of references: <br>

                1. `Location`: A reference to a Location captures what Practice Location in Canvas the appointment will take place at.<br>
                2. `Meeting Link`: For appointments that are telehealth in Canvas, there can be a reference to an endpoint in this list. The reference attribute will need to match an `id` in the `Appointment.contained` attribute list, but will need to have a `#` in front of the reference string. See examples for help. For telehealth appointments where no meeting link reference is supplied, it will default to the practitioner's personal meeting room link as defined in Canvas Settings.
            attributes:
              - name: reference
                required_in: create,update
                type: string
                description_for_all_endpoints: The reference string of the supporting information.
                create_and_update_description:
                  If the entry is for a Location the format will be `"Location/9d3a079f-22c0-4918-96d7-72eb567563ec"`. You can retrieve this information for a [Location Search](/api/location#search).<br><br>

                  If the entry is for a virtual meeting link, the reference should be `#appointment-meeting-endpoint-0`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Location", "Endpoint", "Encounter", "Appointment").
              - name: display
                exclude_in: create, update
                type: string
                description: Display name of the reference
                enum_options:
                  - value: Previously Rescheduled Appointment
                  - value: Rescheduled Replacement Appointment
                  - value: Co-scheduled Appointment
          - name: start
            type: datetime
            required_in: create,update
            description_for_all_endpoints: When appointment is to take place.
            create_and_update_description:
              The `start` attribute determines the start timestamp of the appointment. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required.
          - name: end
            type: datetime
            required_in: create,update
            description_for_all_endpoints: When appointment is to conclude.
            create_description:
              The end attribute is used with the start timestamp to determine the duration in minutes of the appointment. The duration of the appointment must be greater than 0 minutes. It is written in [instant format for FHIR](https://www.hl7.org/fhir/datatypes.html#instant). Seconds and milliseconds can be omitted, but YYYY-MM-DDTHH:MM are required.
          - name: participant
            required_in: create,update
            read_and_search_description: >-
               Participants involved in appointment. There will be at least one entry for a practitioner. An optional 2nd entry will display if the appointment involves a specific patient. This will be dictated by the `appointmentType` and if it relates to a generic event or a patient's appointment. 
            create_and_update_description:
              Participants involved in appointment. At least one object needs to be supplied that corresponds to the practitioner, there will always be a practitioner involved in every appointment type. An optional 2nd object corresponding to the patient reference will be accepted if the `appointmentType` allows/requires a patient participant. 
            type: array[json]
            attributes:
              - name: actor
                required_in: create,update
                type: json
                description: Reference to person involved in appointment.
                attributes:
                  - name: reference
                    required_in: create,update
                    type: string
                    description: The reference string of the practitioner or patient in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
                    enum_options:
                      - value: Practitioner/id
                      - value: Patient/id
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Patient", "Practitioner").
                    enum_options:
                      - value: Practitioner
                      - value: Patient
              - name: status
                required_in: create,update
                type: enum [ accepted ]
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for the Appointment.
          - name: appointment-type
            type: string
            description: Filters by the code and/or system under `appointmentType.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g `http://snomed.info/sct|308335008`).
          - name: location
            type: string
            description: The location of the appointment in the format `Location/9d3a079f-22c0-4918-96d7-72eb567563ec`.
          - name: patient
            type: string
            description: The patient the appointment is for in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
          - name: practitioner
            type: string
            description: The practitioner involoved in the appointment in the format `Practitioner/3a9cafb9d1b445be95a2e2548e12a787`.
          - name: date
            type: string
            description: Filter by start time. See [Date Filtering](/api/date-filtering) for more information.
          - name: status
            type: string
            description: The status of the appointment.
            search_options:
              - value: proposed
              - value: pending
              - value: booked
              - value: arrived
              - value: checked-in
              - value: fulfilled
              - value: noshow
              - value: cancelled
          - name: _sort
            type: string
            description: Triggers sorting of the results by a specific criteria. Adding a `-` will sort in descending order while the default sorts in ascending order.
            search_options: 
              - value: date
              - value: patient
              - value: practitioner
              - value: -date
              - value: -patient
              - value: -practitioner
        endpoints: [create, read, update, search]
        create:
          description: Create an **Appointment**<br><br> 
            It is recommended to utilize the [FHIR Slot Search](/api/slot#search) to find appointment times for a specific practitioner.<br><br>
            **Prevent Double Booking** By default, Canvas does not prevent appointments from being created if there is already an existing appointment for that provider. However, Canvas has a config setting to disable double booking. If double booking is not allowed and the Appointment Create or Appointment Update request is trying to book an appointment for a given Provider that already has a scheduled appointment at that time, you will see a 422 error status with the following error message returned `This appointment time is no longer available.`
          responses: [201, 400, 401, 403, 405, 422]
          example_request: appointment-create-request
          example_response: appointment-create-response
        read:
          description: Read an Appointment
          responses: [200, 401, 403, 404]
          example_request: appointment-read-request
          example_response: appointment-read-response
        update:
          description: Update an **Appointment** This is almost identical to the [Appointment Create](/api/appointment/#create). The update will only affect fields that are passed in to the body, if any fields are omitted they will be ignored and kept as they are currently set in the Canvas database. <br><br>A FHIR Appointment update interaction behaves differently than a rescheduling workflow in the Canvas UI. FHIR updates will directly modify the Appointment referred to by the `id` rather than creating a new appointment.
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: appointment-update-request
          example_response: appointment-update-response
        search:
          description: Search for an Appointment
          responses: [200, 400, 401, 403]
          example_request: appointment-search-request
          example_response: appointment-search-response
---

<div id="appointment-read-request">
{%  include read-request.html resource_type="Appointment" %}
</div>

<div id="appointment-read-response">
{% tabs appointment-read-response %}

{% tab appointment-read-response 200 %}
```json
{
    "resourceType": "Appointment",
    "id": "621a66fc-9d5c-4de0-97fb-935d611ac176",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint-0",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
            "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
        }
    ],
    "identifier": [
        {
            "id": "97b28298-f618-4972-9a6b-d095785587d6",
            "use": "usual",
            "system": "AssigningSystem",
            "value": "test123",
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31"
            }
        }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "description": "Initial 30 Minute Visit",
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060",
            "type": "Location"
        },
        {
            "reference": "#appointment-meeting-endpoint-0",
            "type": "Endpoint"
        },
        {
            "reference": "Encounter/23668e1a-e914-4eac-885c-1a2a27244ab7",
            "type": "Encounter"
        },
        {
            "reference": "Appointment/7fa2874e-73c8-418d-bb25-eea0ccac651c",
            "type": "Appointment",
            "display": "Co-scheduled appointment"
        } 
    ],
    "start": "2023-10-24T13:30:00+00:00",
    "end": "2023-10-24T14:00:00+00:00",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                "type": "Practitioner"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d",
                "type": "Patient"
            },
            "status": "accepted"
        }
    ]
}
```
{% endtab %}

{% tab appointment-read-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authentication failed"
      }
    }
  ]
}
```
{% endtab %}

{% tab appointment-read-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
{% endtab %}

{% tab appointment-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Appointment resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
{% endtab %}

{% endtabs %}
</div>

<div id="appointment-search-request">
{% include search-request.html resource_type="Appointment" search_string="patient=Patient/a031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner/4150cd20de8a470aa570a852859ac87e" %}
</div>

<div id="appointment-search-response">
{% tabs appointment-search-response %}
{% tab appointment-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Appointment?patient=Patient%2Fa031d1ba40d74aebb8ed716716da05c2&practitioner=Practitioner%2F4150cd20de8a470aa570a852859ac87e&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Appointment",
                "id": "f7bb6d7e-1cab-42cd-b3d2-40229e1bede7",
                "contained":
                [
                    {
                        "resourceType": "Endpoint",
                        "id": "appointment-meeting-endpoint-0",
                        "status": "active",
                        "connectionType":
                        {
                            "code": "https"
                        },
                        "payloadType":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "code": "video-call"
                                    }
                                ]
                            }
                        ],
                        "address": "https://url-for-video-chat.example.com?meeting=abc123"
                    }
                ],
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/note-id",
                        "valueId": "2a8154d8-9420-4ab5-97f8-c2dae5a10af5",
                    }
                ],
                "identifier": [
                  {
                      "id": "97b28298-f618-4972-9a6b-d095785587d6",
                      "use": "usual",
                      "system": "AssigningSystem",
                      "value": "test123",
                      "period": {
                          "start": "2024-01-01",
                          "end": "2024-12-31"
                      }
                  }
                ],
                "status": "proposed",
                "appointmentType":
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "448337001",
                            "display": "Telemedicine"
                        }
                    ]
                },
                "reasonCode":
                [
                    {
                        "coding":
                        [
                            {
                                "system": "INTERNAL",
                                "code": "INIV",
                                "display": "Initial Visit",
                                "userSelected": false
                            }
                        ],
                        "text": "Initial 30 Minute Visit"
                    }
                ],
                "description": "Initial 30 Minute Visit",
                "supportingInformation":
                [
                    {
                        "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060",
                        "type": "Location"
                    },
                    {
                        "reference": "#appointment-meeting-endpoint-0",
                        "type": "Endpoint"
                    },
                    {
                        "reference": "Encounter/797ccaae-2939-4e8a-9d91-5e9574a11a4e",
                        "type": "Encounter"
                    }
                ],
                "start": "2023-10-24T13:30:00+00:00",
                "end": "2023-10-24T14:00:00+00:00",
                "participant":
                [
                    {
                        "actor":
                        {
                            "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e",
                            "type": "Practitioner"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor":
                        {
                            "reference": "Patient/a031d1ba40d74aebb8ed716716da05c2",
                            "type": "Patient"
                        },
                        "status": "accepted"
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab appointment-search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "details": {
        "text": "Bad request"
      }
    }
  ]
}
```
{% endtab %}
{% tab appointment-search-response 401 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authentication failed"
      }
    }
  ]
}
```
{% endtab %}

{% tab appointment-search-response 403 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-create-request">
{% tabs appointment-create-request %}

{% tab appointment-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Appointment' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
        {
            "use": "usual",
            "system": "AssigningSystem",
            "value": "test123",
            "period": {
                "start": "2024-01-01",
                "end": "2024-12-31"
            }
        }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}
'
```
{% endtab %}

{% tab appointment-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Appointment"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "proposed",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": False
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-create-response">
{% include create-response.html %}
</div>

<div id="appointment-update-request">
{% tabs appointment-update-request %}

{% tab appointment-update-request curl %}
```shell
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Appointment/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "id": "97b28298-f618-4972-9a6b-d095785587d6",
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "cancelled",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": false
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}
'
```
{% endtab %}
{% tab appointment-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Appointment/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Appointment",
    "contained":
    [
        {
            "resourceType": "Endpoint",
            "id": "appointment-meeting-endpoint",
            "status": "active",
            "connectionType":
            {
                "code": "https"
            },
            "payloadType":
            [
                {
                    "coding":
                    [
                        {
                            "code": "video-call"
                        }
                    ]
                }
            ],
            "address": "https://url-for-video-chat.example.com?meeting=abc123"
        }
    ],
    "identifier": [
      {
          "id": "97b28298-f618-4972-9a6b-d095785587d6",
          "use": "usual",
          "system": "AssigningSystem",
          "value": "test123",
          "period": {
              "start": "2024-01-01",
              "end": "2024-12-31"
          }
      }
    ],
    "status": "cancelled",
    "appointmentType":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "reasonCode":
    [
        {
            "coding":
            [
                {
                    "system": "INTERNAL",
                    "code": "INIV",
                    "display": "Initial Visit",
                    "userSelected": False
                }
            ],
            "text": "Initial 30 Minute Visit"
        }
    ],
    "supportingInformation":
    [
        {
            "reference": "Location/b3476a18-3f63-422d-87e7-b3dc0cd55060"
        },
        {
            "reference": "#appointment-meeting-endpoint",
            "type": "Endpoint"
        }
    ],
    "start": "2023-10-24T13:30:00.000Z",
    "end": "2023-10-24T14:00:00.000Z",
    "participant":
    [
        {
            "actor":
            {
                "reference": "Patient/ee1c7803325b47b492008f3e7c9d7a3d"
            },
            "status": "accepted"
        },
        {
            "actor":
            {
                "reference": "Practitioner/4150cd20de8a470aa570a852859ac87e"
            },
            "status": "accepted"
        }
    ]
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
{% endtabs %}
</div>

<div id="appointment-update-response">
{% include update-response.html resource_type="Appointment" %}
</div>
