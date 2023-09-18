---
title: Device
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Device
        article: "a"
        description: >-
          A type of a manufactured item that is used in the provision of healthcare without being substantially changed through that activity. The device may be a medical or non-medical device.<br><br>
          [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-implantable-device.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-implantable-device.html)<br><br>
          For information about creating Device resources for a patient, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4413855312147-Implantable-Device-List). Devices are not currently used by the Canvas UI, but any devices that are created can be accessed with the Device read and search endpoints, In order to generate the type attribute, a device code must be created and linked to the device via the admin settings on Canvas.

        attributes:
          - name: id
            description: The identifier of the Device
            type: string
          - name: udiCarrier
            description: Unique Device Identifier (UDI) Barcode string
            type: array[json]
          - name: status
            description: Status of the Device availability
            type: string
          - name: distinctIdentifier
            description: The distinct identification string
            type: string
          - name: manufacturer
            description: Name of device manufacturer
            type: string
          - name: manufactureDate
            description: Date when the device was made
            type: date
          - name: expirationDate
            description: Date of expiry of this device (if applicable)
            type: date
          - name: lotNumber
            description: Lot number of manufacture
            type: string
          - name: serialNumber
            description: Serial number assigned by the manufacturer
            type: string
          - name: modelNumber
            description: The model number for the device
            type: string
          - name: type
            description: The kind or type of device
            type: json
          - name: patient
            description: Patient to whom Device is affixed
            type: json
        search_parameters:
          - name: _id
            type: string
            description: The identifier of the Device
          - name: patient
            type: string
            description: Patient information, if the resource is affixed to a person
        endpoints: [read, search]
        read:
          description: 
          responses: [200, 401, 403, 404]
          example_request: device-read-request
          example_response: device-read-response
        search:
          description: 
          responses: [200, 400, 401, 403]
          example_request: device-search-request
          example_response: device-search-response
---

<div id="device-read-request">
{% include read_request.html resource_type="Device" %}
</div>

<div id="device-read-response">

  {% tabs device-read-response %}

    {% tab device-read-response 200 %}
```json
{
    "resourceType": "Device",
    "id": "c6bf6efc-1fe1-4221-9821-e60acb53becc",
    "udiCarrier":
    [
        {
            "deviceIdentifier": "08717648200274",
            "carrierHRF": "=/08717648200274=,000025=A99971312345600=>014032=}013032&,1000000000000XYZ123"
        }
    ],
    "status": "active",
    "distinctIdentifier": "A99971312345600",
    "manufacturer": "ACME Biomedical",
    "manufactureDate": "2021-02-15",
    "expirationDate": "2021-09-15",
    "lotNumber": "234234",
    "serialNumber": "13213123123123",
    "modelNumber": "1.0",
    "type":
    {
        "coding":
        [
            {
                "system": "http://snomed.info/sct",
                "code": "2478003",
                "display": "Ocular prosthesis"
            }
        ]
    },
    "patient":
    {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
        "type": "Patient"
    }
}
```
    {% endtab %}

    {% tab device-read-response 401 %}
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

    {% tab device-read-response 403 %}
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

    {% tab device-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Device resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="device-search-request">

  {% tabs device-search-request %}

    {% tab device-search-request curl %}
```sh
curl --request GET \
     --url https://fumage-example.canvasmedical.com/Device/?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0 \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json'
```
    {% endtab %}

    {% tab device-search-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Device/?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}

</div>

<div id="device-search-response">

  {% tabs device-search-response %}

    {% tab device-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Device/?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Device/?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Device/?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Device",
                "id": "c6bf6efc-1fe1-4221-9821-e60acb53becc",
                "udiCarrier":
                [
                    {
                        "deviceIdentifier": "08717648200274",
                        "carrierHRF": "=/08717648200274=,000025=A99971312345600=>014032=}013032&,1000000000000XYZ123"
                    }
                ],
                "status": "active",
                "distinctIdentifier": "A99971312345600",
                "manufacturer": "ACME Biomedical",
                "manufactureDate": "2021-02-15",
                "expirationDate": "2021-09-15",
                "lotNumber": "234234",
                "serialNumber": "13213123123123",
                "modelNumber": "1.0",
                "type":
                {
                    "coding":
                    [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "2478003",
                            "display": "Ocular prosthesis"
                        }
                    ]
                },
                "patient":
                {
                    "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0",
                    "type": "Patient"
                }
            }
        }
    ]
}
```
    {% endtab %}

    {% tab device-search-response 400 %}
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

    {% tab device-search-response 401 %}
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

    {% tab device-search-response 403 %}
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
