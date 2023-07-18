---
title: FHIR Patient 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
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
        example_payload: example-payload-code
        endpoints:
          - summary: Patient read
            method: get
            url: '/Patient/{_id}'
            description: >-
              Get information about a particular patient
            parameters:
              - name: _id
                description: A Canvas-issued unique identifier. This is not an MRN.
                required: true
                type: string
            responses:
              - response: 200
              - response: 400
            example_request: example-read-request
            example_response: example-read-response
          - summary: Patient search
            method: get
            url: '/Patient'
            description: >-
              Search for patients
            parameters:
              - name: id
                description: Logical id of this artifact
                required: true
                type: string
              - name: _format
                description: >-
                  Override the HTTP content negotiation to specify JSON or XML
                  response format
                required: false
                type: string
              - name: _pretty
                description: Ask for a pretty printed response for human convenience
                required: false
                type: string
            responses:
              - response: 200
              - response: 400
            example_request: example-search-request
            example_response: example-search-response
          - summary: Patient create
            method: post
            url: '/Patient'
            description: >-
              Create a patient
            parameters:
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
            responses:
              - response: 200
              - response: 400
            example_request: example-create-request
            example_response: example-create-response
          - summary: Patient update
            method: put
            url: '/Patient/{_id}'
            description: >-
              Update a patient
            parameters:
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
            responses:
              - response: 200
              - response: 400
            example_request: example-create-request
            example_response: example-create-response
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

<div id="example-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
200 {
  ...
}
```
{% endtab %}
{% tab read-response 400 %}
```json
400 {
  ...
}
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

