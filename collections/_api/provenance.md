---
title: FHIR Provenance
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Provenance
        article: "a"
        description: >-
         Provenance of a resource is a record that describes entities and processes involved in producing and delivering or otherwise influencing that resource. Provenance provides a critical foundation for assessing authenticity, enabling trust, and allowing reproducibility. Provenance assertions are a form of contextual metadata and can themselves become important records with their own provenance. Provenance statement indicates clinical significance in terms of confidence in authenticity, reliability, and trustworthiness, integrity, and stage in lifecycle (e.g. Document Completion - has the artifact been legally authenticated), all of which may impact security, privacy, and trust policies.
        attributes:
          - name: id
            description: >-
              The identifier of the patient
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: recorded 
            description: >-
              When the activity occurred
            type: string
          - name: target
            description: >-
              The target resource that was created
            type: array
          - name: location
            description: >-
              Where the activity occurred, if relevant
            type: string
          - name: activity
            description: >-
              The activity that occurred
            type: string
          - name: agent
            description: >-
              The agent that created the provenance
            type: array      
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
            description: The patient associated with the provenance
          - name: target
            type: string
            description: The target resource that was created
          - name: agent
            type: string
            description: The agent that created the provenance
        endpoints: [read, search]
        read:
          responses: [200, 400]
          example_response: provenance-read-response
          example_request: provenance-read-request
        search:
          responses: [200, 400]
          example_response: provenance-search-response
          example_request: provenance-search-request
---
<div id="provenance-read-request">
{% tabs read-request %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Provenance/_id \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="provenance-read-response">
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

<div id="provenance-search-request">
{% tabs search-request %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Provenance \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="provenance-search-response">
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

