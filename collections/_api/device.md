---
title: Device
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Device
        article: "a"
        description: >-
          Implantable devices
        attributes:
          - name: id
            type: string
            description: A Canvas-issued unique identifier
            required: true
          - name: resourceType
            type: string
            required: true
          - name: udiCarrier
            type: string
          - name: status
            type: string 
          - name: distinctIdentifier
            type: string
          - name: manufacturer
            type: string 
          - name: manufactureDate
            type: date
          - name: expirationDate
            type: date
          - name: lotNumber
            type: string
          - name: serialNumber
            type: string
          - name: modelNumber
            type: string
          - name: type
            type: json
          - name: patient
            type: string
            description: >-
              The patient
            required: true
        search_parameters:
          - name: id
            type: string
            description: A Canvas-issued unique identifier
          - name: patient
            type: string
            description: >-
              The patient
        endpoints: [read, search]
        read:
          responses: [200, 404]
          example_response: device-read-response
          example_request: device-read-request
        search:
          responses: [200, 400]
          example_response: device-search-response
          example_request: device-search-request

---
<div id="device-read-request">
{% tabs read-request %}
{% tab read-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/Device/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
{% endtab %}
{% tab read-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Patient/<id> \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="device-read-response">
{% tabs read-response %}
{% tab read-response 200 %}
```json
{
    "resourceType": "Device",
    "id": "105c679e-02e3-46ca-85c5-d8a158a42839",
    "udiCarrier": [
        {
            "deviceIdentifier": "08717648200274",
            "carrierHRF": "=/08717648200274=,000025=A99971312345600=>014032=}013032&,1000000000000XYZ123"
        }
    ],
    "status": "active",
    "distinctIdentifier": "A99971312345600",
    "manufactureDate": "2021-02-15",
    "expirationDate": "2021-09-15",
    "lotNumber": "234234",
    "serialNumber": "13213123123123",
    "type": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "2478003",
                "display": "Ocular prosthesis"
            }
        ]
    },
    "patient": {
        "reference": "Patient/ff6fd298ab8d4b5a819197f43c936c7c",
        "type": "Patient",
        "display": "Giant Cube"
    }
}
```
{% endtab %}
{% tab read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Device resource 'abc'"
            }
        }
    ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="device-search-request">
{% tabs search-request %}
{% tab search-request python %}
```sh
import requests

url = "https://fumage-example.canvasmedical.com/DeviceSearch"

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
     --url https://fumage-example.canvasmedical.com/Device \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
{% endtab %}
{% endtabs %}
</div>

<div id="device-search-response">
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
            "url": "/Device?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Device?_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Device?_count=10&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Device",
                "id": "105c679e-02e3-46ca-85c5-d8a158a42839",
                "udiCarrier": [
                    {
                        "deviceIdentifier": "08717648200274",
                        "carrierHRF": "=/08717648200274=,000025=A99971312345600=>014032=}013032&,1000000000000XYZ123"
                    }
                ],
                "status": "active",
                "distinctIdentifier": "A99971312345600",
                "manufactureDate": "2021-02-15",
                "expirationDate": "2021-09-15",
                "lotNumber": "234234",
                "serialNumber": "13213123123123",
                "type": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "2478003",
                            "display": "Ocular prosthesis"
                        }
                    ]
                },
                "patient": {
                    "reference": "Patient/ff6fd298ab8d4b5a819197f43c936c7c",
                    "type": "Patient",
                    "display": "Giant Cube"
                }
            }
        }
    ]
}
```
{% endtab %}
{% tab search-response 400 %}
```json
{
  "resourceType": "OperationOutcome",
  "id": "101",
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
{% endtabs %}
</div>


