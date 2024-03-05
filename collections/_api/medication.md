---
title: Medication
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Medication
        article: "a"
        description: >-
         This resource is primarily used for the identification and definition of a medication for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.<br><br>
         [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medication.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-medication.html)<br><br>
         Best practices is to utilize this endpoint to find codings to feed the [Medication Statement Create/Update](/api/medicationstatement/#create). These medications come directly from our integration with FDB.
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            description: The identifier of the Medication.
            type: string
          - name: text
            description: Text summary of the Medication, for human interpretation.
            type: json
            attributes:
              - name: status
                description: All medications returned from this endpoint will show a status of `generated` since this resource is generated from FDB.
              - name: div
                description: Limited xhtml content that contains the human readable text of the Medication.
          - name: code
            description: Code that identifies the medication.
            type: json
            attributes: 
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    enum_options: 
                      - value: http://www.nlm.nih.gov/research/umls/rxnorm
                      - value: http://www.fdbhealth.com/
                    type: string
                  - name: code
                    description: The code of the medication.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
        endpoints: [read, search]
        search_requirements_description: A Medication Search requires either a code or _text search parameter to perform. 
        search_parameters:
          - name: _text
            description: Performs a case insensitive partial search on the narrative of the Medication.
            type: string
          - name: code
            description: System url and code that identifies the medication formatted like <br> `system_url|code`.<br><br>
              Currently a search for an RxNorm code will return both branded and generic medications associated with the RxNorm code regardless of whether the RxNorm code is branded or generic.<br><br>
              For example, a search for the RxNorm code that represents the branded version of metformin will return a search bundle that contains at least two Medication resources -- one for the branded version and one for the generic version. The branded and generic Medication resources in the search bundle can be differentiated by the presence or absence of the RxNorm code for the branded version in the list of codings.
            search_options:
              - value: http://www.nlm.nih.gov/research/umls/rxnorm|code
        read:
          description: Read a Medication resource.
          responses: [200, 401, 403, 404]
          example_request: medication-read-request
          example_response: medication-read-response
        search:
          description: Search for Medication resources.
          responses: [200, 400, 401, 403]
          example_request: medication-search-request
          example_response: medication-search-response
---

<div id="medication-read-request">
{%  include read-request.html resource_type="Medication" %}
</div>

<div id="medication-read-response">

  {% tabs medication-read-response %}

    {% tab medication-read-response 200 %}
```json
{
    "resourceType": "Medication",
    "id": "fdb-449732",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Tylenol PM Extra Strength 25 mg-500 mg tablet</div>"
    },
    "code": {
        "coding": [
            {
                "system": "http://www.fdbhealth.com/",
                "code": "449732",
                "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1092189",
                "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1092378",
                "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
            }
        ],
        "text": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
    }
}
```
    {% endtab %}

    {% tab medication-read-response 401 %}
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

    {% tab medication-read-response 403 %}
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

    {% tab medication-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Medication resource 'fdb-399234'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="medication-search-request">
{% include search-request.html resource_type="Medication" search_string="code=http://www.nlm.nih.gov/research/umls/rxnorm|1092189&_text=tylenol" %}
</div>

<div id="medication-search-response">

  {% tabs medication-search-response %}

    {% tab medication-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link": [
        {
            "relation": "self",
            "url": "/Medication?code=http://www.nlm.nih.gov/research/umls/rxnorm|1092189&_text=tylenol&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Medication?code=http://www.nlm.nih.gov/research/umls/rxnorm|1092189&_text=tylenol&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Medication?code=http://www.nlm.nih.gov/research/umls/rxnorm|1092189&_text=tylenol&_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Medication",
                "id": "fdb-449732",
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Tylenol PM Extra Strength 25 mg-500 mg tablet</div>"
                },
                "code": {
                    "coding": [
                        {
                            "system": "http://www.fdbhealth.com/",
                            "code": "449732",
                            "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
                        },
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "1092189",
                            "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
                        },
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "1092378",
                            "display": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
                        }
                    ],
                    "text": "Tylenol PM Extra Strength 25 mg-500 mg tablet"
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab medication-search-response 400 %}
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

    {% tab medication-search-response 401 %}
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

    {% tab medication-search-response 403 %}
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
