---
title: FHIR Patient 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
        article: "a"
        description: >-
          At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.
        attributes:
          - name: _id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
          - name: extension
            type: json
            required: true
          - name: identifier
            type: json
            required: false
          - name: active
            type: boolean
            required: false
          - name: name
            type: json
            required: true
          - name: telecom
            type: json
            required: false
          - name: gender
            description: >-
              Default: male
            type: string
            required: false
          - name: deceased
            type: boolean
            required: false
          - name: address
            type: json
            required: false
          - name: photo
            type: json
            required: false
          - name: contact
            type: json
            required: false
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: identifier
            type: string
            description: The Canvas-issued MRN or a saved identifier from an external system  
          - name: name
            type: string
            description: Part of a first or last name
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: birthdate
            type: date
            description: The patient's birthdate
          - name: gender
            type: string
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: email
            type: string
            description: Patient email address
          - name: phone
            type: string
            description: Patient phone number, expected to be 10 digits
          - name: active
            type: boolean
            description: By default, both active and inactive patients are returned. Use this parameter to only return active (true) or inactive (false)
        example_payload: example-payload-code
        endpoints: [read, search, create, update]
        read:
          responses: [200, 400]
          example_response: example-payload-code
        search:
          responses: [200, 400]
          example_response: example-search-response
        create:
          example_request: example-create-request
        update:
          example_request: example-update-request
---
<div id="example-payload-code">
{% tabs payload %}
{% tab payload json %}
```json
some data here
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-read-request">
{% tabs read-request %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-request">
{% tabs search-request %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab search-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-create-request">
{% tabs create-request %}
{% tab create-request curl %}
```sh
curl --request POST \
     --url https://fhir-example.canvasmedical.com/Patient \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Patient",
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Isabella",
        "Robel"
      ],
      "prefix": "Mrs.",
      "suffix": "Jr."
    },
    {
      "use": "nickname",
      "given": [
        "Izzy"
      ]
    },
    {
      "use": "maiden",
      "family": "Smith"
    }
  ],
  "birthDate": "1980-11-13"
}
'
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-create-response">
{% tabs create-response %}
{% tab create-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab create-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="example-update-request">
{% tabs update-request %}
{% tab update-request curl %}
```sh
curl --request PUT \
     --url https://fhir-example.canvasmedical.com/Patient/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Patient",
  "id": "c9491183c38b4fe793db70c60046db3f",
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
      "valueCode": "M"
    },
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
      "extension": [
        {
          "url": "text",
          "valueString": "UNK"
        }
      ]
    },
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2106-3",
            "display": "White"
          }
        }
      ]
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
      "extension": [
        {
          "url": "ncpdp-id",
          "valueIdentifier": {
            "value": "1123152",
            "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
          }
        }
      ]
    },
    {
      "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
      "valueCode": "America/New_York"
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
      "valueString": "I am a clinical caption from a Create message"
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
      "valueString": "I am an administrative caption from a Create message"
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Mark",
      "given": [
        "Jade",
        "Robel"
      ]
    },
    {
      "use": "nickname",
      "given": [
        "Nick Name"
      ]
    }
  ],
  "birthDate": "1980-11-13"
}
'

```
{% endtab %}
{% endtabs %}
</div>

<div id="example-update-response">
{% tabs update-response %}
{% tab update-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab update-response 400 %}
```json
400 {
  ...
}
```
{% endtab %}
{% endtabs %}
</div>

