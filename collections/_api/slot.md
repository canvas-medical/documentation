---
title: Slot 
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Slot
        article: "a"
        description: >-
         This will give you a list of location/practitioner combinations that is necessary for identifying open slots when booking appointments.
        attributes:
          - name: _id
            description: >-
              The identifier of the slot
            type: string
            required: true
          - name: resourceType
            type: string
            required: true
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: identifier
            type: string
            description: The Canvas-issued MRN or a saved identifier from an external system  
        endpoints: [search]
        search:
          responses: [200, 400]
          example_request: slot-search-request
          example_response: slot-search-response
---

<div id="slot-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Slot?schedule=Schedule%2FLocation.1-Staff.c2ff4546548e46ab8959af887b563eab&start=2022-03-10&duration=20&end=2022-03-30"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)

```
{% endtab %}
{% tab search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Slot \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="slot-search-response">
{% tabs search-response %}
{% tab search-response 200 %}
```json
200 {
  {
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 8,
    "entry": [
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.1-Staff.e766816672f34a5b866771c773e38f3c",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Youta Priti MD at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/e766816672f34a5b866771c773e38f3c",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Youta Priti MD at California"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.1-Staff.77bd177f81b14c9f943e1e30ed3dd989",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Breanna Heller LMFT at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/77bd177f81b14c9f943e1e30ed3dd989",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Breanna Heller LMFT at California"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.1-Staff.f65c2bed0d8643cc808e25d5cfcf5070",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Patrick van Nieuwenhuizen MD at California</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/f65c2bed0d8643cc808e25d5cfcf5070",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Patrick van Nieuwenhuizen MD at California"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.2-Staff.e766816672f34a5b866771c773e38f3c",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Youta Priti MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/e766816672f34a5b866771c773e38f3c",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Youta Priti MD at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.2-Staff.3a182f42885645e0bc3d608e7c02aad8",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Nikhil Krishnan MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/3a182f42885645e0bc3d608e7c02aad8",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Nikhil Krishnan MD at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.2-Staff.77bd177f81b14c9f943e1e30ed3dd989",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Breanna Heller LMFT at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/77bd177f81b14c9f943e1e30ed3dd989",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Breanna Heller LMFT at Tennessee"
            }
        },
        {
            "resource": {
                "resourceType": "Slot",
                "id": "Location.2-Staff.f65c2bed0d8643cc808e25d5cfcf5070",
                "text": {
                    "status": "generated",
                    "div": "<div>Slot for Patrick van Nieuwenhuizen MD at Tennessee</div>"
                },
                "actor": [
                    {
                        "reference": "Practitioner/f65c2bed0d8643cc808e25d5cfcf5070",
                        "type": "Practitioner"
                    }
                ],
                "comment": "Slot for Patrick van Nieuwenhuizen MD at Tennessee"
            }
        }
    ]
}
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

