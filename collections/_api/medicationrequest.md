---
title: MedicationRequest
sections:
  - type: section
    blocks:
      - type: apidoc
        name: MedicationRequest
        article: "a"
        description: >-
          An order or request for both supply of the medication and the instructions for administration of the medication to a patient. The resource is called "MedicationRequest" rather than "MedicationPrescription" or "MedicationOrder" to generalize the use across inpatient and outpatient settings, including care plans, etc., and to harmonize with workflow patterns.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medicationrequest.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medicationrequest.html)
        attributes:
          - name: id
            description: The identifier of the MedicationRequest
            type: string
          - name: status
            description: A code specifying the current state of the order. Generally, this will be active or completed state
            type: string
          - name: intent
            description: Whether the request is a proposal, plan, or an original order
            type: string
          - name: reportedBoolean
            description: Indicates if this record was captured as a secondary 'reported' record rather than as an original primary source-of-truth record
            type: boolean
          - name: medicationCodeableConcept
            description: Identifies the medication being requested. This is simply an attribute carrying a code that identifies the medication from a known list of medications.
            type: json
          - name: subject
            description: Who or group medication request is for
            type: json
          - name: encounter
            description: Encounter created as part of encounter/admission/stay
            type: json
          - name: authoredOn
            description: When request was initially authored
            type: datetime
          - name: requester
            description: Who/What requested the Request
            type: json
          - name: performer
            description: Intended performer of administration
            type: json
          - name: reasonCode
            description: Reason or indication for ordering or not ordering the medication
            type: array[json]
          - name: note
            description: Information about the prescription
            type: array[json]
          - name: dosageInstruction
            description: How the medication should be taken
            type: array[json]
          - name: dispenseRequest
            description: Medication supply authorization
            type: json
          - name: substitution
            description: Any restrictions on medication substitution
            type: json
        search_parameters:
          - name: _id
            description: The identifier of the MedicationRequest
            type: string
          - name: intent
            description: Returns prescriptions with different intents	
            type: string
          - name: patient
            description: Returns prescriptions for a specific patient	
            type: string
          - name: status
            description: Status of the prescription
            type: string
        endpoints: [read, search]
        read:
          description: Read a MedicationRequest resource.
          responses: [200, 401, 403, 404]
          example_request: medicationrequest-read-request
          example_response: medicationrequest-read-response
        search:
          description: Search for MedicationRequest resources.
          responses: [200, 400, 401, 403]
          example_request: medicationrequest-search-request
          example_response: medicationrequest-search-response
---

<div id="medicationrequest-read-request">
{%  include read-request.html resource_type="MedicationRequest" %}
</div>

<div id="medicationrequest-read-response">

  {% tabs medicationrequest-read-response %}

    {% tab medicationrequest-read-response 200 %}
```json
```
    {% endtab %}

    {% tab medicationrequest-read-response 401 %}
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

    {% tab medicationrequest-read-response 403 %}
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

    {% tab medicationrequest-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown MedicationRequest resource 'a47c7b0e-bbb4-42cd-bc4a-df259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medicationrequest-search-request">
{% include search-request.html resource_type="AllergyIntolerance" search_string="patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0" %}
</div>

<div id="medicationrequest-search-response">

  {% tabs medicationrequest-search-response %}

    {% tab medicationrequest-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/MedicationRequest?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/MedicationRequest?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/MedicationRequest?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource": {}
        }
    ]
}
```
    {% endtab %}

    {% tab medicationrequest-search-response 400 %}
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

    {% tab medicationrequest-search-response 401 %}
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

    {% tab medicationrequest-search-response 403 %}
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
