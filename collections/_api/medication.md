---
title: Medication
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Medication
        article: "a"
        description: >-
         This resource is primarily used for the identification and definition of a medication for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.
        attributes:
          - name: id
            description: >-
              The identifier of the medication
            type: string
            required: true
          - name: resourceType
            description: >-
              The type of resource
            type: string
            required: true
          - name: code
            description: >-
              A code that identifies the medication
            type: string
            attributes:
              - name: coding
                description: >-
                  A code that identifies the medication
                type: array
                attributes:
                  - name: system
                    description: >-
                      The system that defines the code
                    type: string
                  - name: code
                    description: >-
                      The code that identifies the medication
                    type: string
                  - name: display
                    description: >-
                      The display name of the medication
                    type: string
              - name: text
                description: >-
                  The display name of the medication
                type: string
        endpoints: [read]
        read:
          responses: [200, 400]
          example_response: medication-read-response
          example_request: medication-read-request

---
<div id="medication-read-request">
{% tabs medication-read-request %}
{% tab medication-read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Medication/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab medication-read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Medication/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="medication-read-response">
{% tabs medication-read-response %}
{% tab medication-read-response 200 %}
```json
{
    "resourceType": "Medication",
    "id": "fdb-297274",
    "code": {
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "541892",
                "display": "Adderall 10 mg tablet"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "541894",
                "display": "Adderall 10 mg tablet"
            }
        ],
        "text": "Adderall 10 mg tablet"
    }
}
```
{% endtab %}
{% tab medication-read-response 404 %}
```json
{
    "detail": "Not Found"
}
```
{% endtab %}
{% endtabs %}
</div>

