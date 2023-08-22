---
title: FHIR Practitioner 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        attributes:
          - name: _id
            description: >-
              The identifier of the practitioner
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
            description: The practitioner's birthdate
          - name: gender
            type: string
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: email
            type: string
            description: Practitioner email address
          - name: phone
            type: string
            description: Practitioner phone number, expected to be 10 digits
          - name: active
            type: boolean
            description: By default, both active and inactive practitioners are returned. Use this parameter to only return active (true) or inactive (false)
        example_payload: example-payload-code
        endpoints: [read, search]
        read:
          responses: [200, 400]
          example_response: example-payload-code
        search:
          responses: [200, 400]
          example_response: example-search-response
  
---
### Adding a New Practitioner in Canvas

To create a new staff member in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360058232193-Add-a-new-staff-member).

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
     --url https://fhir-example.canvasmedical.com/Practitioner/_id \
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
     --url https://fhir-example.canvasmedical.com/Practitioner \
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
