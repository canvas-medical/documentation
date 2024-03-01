---
title: Immunization
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Immunization
        article: "a"
        description: >-
          Describes the event of a patient being administered a vaccine or a record of an immunization as reported by a patient, a clinician or another party.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-immunization.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-immunization.html)<br><br>

          In Canvas, Immunization records can be created using either the [Immunization Statement Commmand](https://canvas-medical.zendesk.com/hc/en-us/articles/360057140293) or the [Immunize Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360057139673).
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            description: The Canvas identifier of the immunization.
          - name: status
            type: enum [ completed | entered-in-error | not-done ]
            description: The status of the immunization.
          - name: statusReason
            type: json
            description: A coding for reason not given, if recorded - ommitted otherwise.
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://terminology.hl7.org/CodeSystem/v3-ActReaso
                  - name: code
                    description: The code.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: vaccineCode
            type: json
            description: Coding for the administered vaccine.
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://hl7.org/fhir/sid/cvx
                      - value: http://www.ama-assn.org/go/cpt
                      - value: unstructured
                  - name: code
                    description: The code.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
          - name: patient
            type: json
            description: The patient who received the immunization.
            attributes:
              - name: reference
                type: string
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: occurrenceDateTime
            type: date
            description: The date or datetime the immunization was administered or reported to have been administered.
          - name: primarySource
            type: boolean
            description: >-
              Whether the immunization was administered by a primary source.<br><br>
              - **true** indicates that the immunization was administered within the clinic. To document immunizations like these, use a [Immunize Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360057140293).<br><br>
              - **false** indicates that the immunization was administered outside the clinic. To document this immunizations like these, use a [Immunization Statement Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360057139673).
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier for a specific immunization.
          - name: patient
            description: The patient for the vaccination record in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
            type: string
        endpoints: [read, search]
        read:
          responses: [200, 401, 403, 404]
          example_request: immunization-read-request
          example_response: immunization-read-response
        search:
          responses: [200, 400, 401, 403]
          example_response: immunization-search-response
          example_request: immunization-search-request
---

<div id="immunization-read-request">
{% include read-request.html resource_type="Immunization" %}
</div>

<div id="immunization-read-response">
  {% tabs immunization-read-response %}
    {% tab immunization-read-response 200 %}
```json
{
  "resourceType": "Immunization",
  "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
  "status": "completed",
  "vaccineCode": {
      "coding": [
        {
          "system": "http://hl7.org/fhir/sid/cvx",
          "code": "207",
          "display": "Moderna Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
        }
      ]
  },
  "patient": {
      "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
      "type": "Patient"
  },
  "occurrenceDateTime": "2022-05-26T18:55:34.629659+00:00",
  "primarySource": false
}
```
    {% endtab %}
    {% tab immunization-read-response 401 %}
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

    {% tab immunization-read-response 403 %}
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

    {% tab immunization-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Immunization resource 'd9aefede-da05-4bef-bbf9-63bcf83c806b'"
      }
    }
  ]
}
```
    {% endtab %}
  {% endtabs %}
</div>

<div id="immunization-search-request">
{% include search-request.html resource_type="Immunization" search_string="patient=Patient/4d9c4a797b8c4a58872017e7a19a474e" %}
</div>

<div id="immunization-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
      {
        "relation": "self",
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      },
      {
        "relation": "first",
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      },
      {
        "relation": "last",
        "url": "/Immunization?patient=Patient%2F4d9c4a797b8c4a58872017e7a19a474e&_count=10&_offset=0"
      }
    ],
    "entry": [
      {
        "resource": {
          "resourceType": "Immunization",
          "id": "d9aefede-da05-4bef-bbf9-63bcf83c806a",
          "status": "completed",
          "vaccineCode": {
            "coding": [
              {
                "system": "http://hl7.org/fhir/sid/cvx",
                "code": "207",
                "display": "Moderna Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2) (coronavirus disease [COVID-19]) vaccine, mRNA-LNP, spike protein, preservative free, 50 mcg/0.25 mL dosage, for intramuscular use"
              }
            ]
          },
          "patient": {
              "reference": "Patient/4d9c4a797b8c4a58872017e7a19a474e",
              "type": "Patient"
          },
          "occurrenceDateTime": "2021-12-01",
          "primarySource": false
        }
      }
    ]
}
```
{% endtab %}
{% tab immunization-search-response 400 %}
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

    {% tab immunization-search-response 401 %}
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

    {% tab immunization-search-response 403 %}
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

