---
title: FHIR Practitioner
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        description: >-
          At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.
        attributes:
          - name: _id
            description: >-
              A Canvas-issued unique identifier.
            type: string
            required: true
          - name: name
            type: string
        example_payload: example-payload-code
        endpoints:
          - summary: Practitioner read
            method: get
            url: '/Practitioner/{_id}'
            description: >-
              Get information about a particular practitioner
            parameters:
              - name: _id
                description: A Canvas-issued unique identifier.
                type: string
                required: true
            responses:
              - response: 200
              - response: 400
            example_request: example-read-request
            example_response: example-read-response
          - summary: Practitioner search
            method: get
            url: '/Practitioner'
            description: >-
              Search for practitioners
            parameters:
              - name: name
                description: Look up practitioner by name. Partial search is supported. If the practitioner you are looking for is inactive, you still need to use the include-non-scheduleable-practitioners = True
                type: string
              - name: include-non-scheduleable-practitioners
                description: By default we only display schedule-able staff, marking this as True will return all active staff
                type: boolean
            responses:
              - response: 200
              - response: 400
            example_request: example-search-request
            example_response: example-search-response
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
