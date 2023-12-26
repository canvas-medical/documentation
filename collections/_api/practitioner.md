---
title: Practitioner
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        description: >-
         A person who is directly or indirectly involved in the provisioning of healthcare.<br><br>[https://hl7.org/fhir/R4/practitioner.html](https://hl7.org/fhir/R4/practitioner.html)<br><br>To create a new staff member in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360058232193-Add-a-new-staff-member).<br><br>

         **Supported Extensions**
          <br><br>

          Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match. Extensions are all `json` types and should be included in the `extension` array field as shown in the request/response examples on this page. The following extensions are supported:<br><br>

          **`practitioner-personal-meeting-room-link`**
          <br><br>

          **`practitioner-primary-practice-location`**
          <br><br>

          **`signature`**
          <br><br>

          **`role`**
          <br><br>

        attributes:
          - name: id
            description: >-
              The identifier of the practitioner
            type: string
          - name: extension
            type: array[json]
            description: >-
              Reference the information at the top of this page to see the possible extensions contained in this resource.
          - name: identifier
            type: array[json]
            description: An identifier for the person as this agent
          - name: name
            type: array[json]
            description: The name(s) associated with the practitioner
          - name: telecom
            type: array[json]
            description: A contact detail for the practitioner
          - name: address
            type: array[json]
            description: Address(es) of the practitioner entered in Canvas
          - name: gender
            type: string
            description: >-
              A enum value that maps to the gender identity attribute in the Canvas UI. Supported values are **male**, **female**, **other** and **unknown**.
          - name: birthDate
            type: date
            description: >-
              The date of birth for the individual, formatted as YYYY-MM-DD.
          - name: photo
            type: array[json]
            description: 	Image of the person
          - name: qualification
            type: array[json]
            description: >-
               Certification, licenses, or training pertaining to the provision of care<br>
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: name
            type: string
            description: A search that may match any of the string fields in the name, including family, given, prefix, suffix, and/or text. Partial search is supported. If the practitioner you are looking for is inactive, you will still need to pass `include-non-scheduleable-practitioners=true`.
          - name: include-non-scheduleable-practitioners
            type: boolean
            description: By default, only scheduleable staff are displayed. Passing this parameter as **true** will return all active staff.
        endpoints: [create, read, update, search]

        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: practitioner-create-request
          example_response: practitioner-create-response
          description: Create Practitioner
        read:
          responses: [200, 401, 403, 404]
          example_request: practitioner-read-request
          example_response: practitioner-read-response
          description: Read a Practitioner resource
        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: practitioner-update-request
          example_response: practitioner-update-response
          description: Update Practitioner
        search:
          responses: [200, 400, 401, 403]
          example_request: practitioner-search-request
          example_response: practitioner-search-response
          description: Search for Practitioner resources
---

<div id="practitioner-create-request">
{% tabs practitioner-create-request %}
{% tab practitioner-create-request curl %}
```sh
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Practitioner' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Practitioner",
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ]
        }
    ],
    "name": [
        {
            "use": "official",
            "family": "Jones",
            "given": [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given": [
                "Sammy"
            ]
        }
    ],
    "telecom": [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        },
        {
            "use": "work",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ]
            }
        }
    ],
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mNk+M9Qz0AEYBxVSF+FAAhKDveksOjmAAAAAElFTkSuQmCC"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"
        }
    ]
}
'
```
{% endtab %}

{% tab practitioner-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Practitioner",
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ]
        }
    ],
    "name": [
        {
            "use": "official",
            "family": "Jones",
            "given": [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given": [
                "Sammy"
            ]
        }
    ],
    "telecom": [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        },
        {
            "use": "work",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ]
            }
        }
    ],
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mNk+M9Qz0AEYBxVSF+FAAhKDveksOjmAAAAAElFTkSuQmCC"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-create-response">
{% include create-response-practitioner.html %}
</div>

<div id="practitioner-read-request">
{%  include read-request.html resource_type="Practitioner" %}
</div>

<div id="practitioner-read-response">
{% tabs practitioner-read-response %}
{% tab practitioner-read-response 200 %}
```json
 {
    "resourceType": "Practitioner",
    "id": "55096fbcdfb240fd8c999c325304de03",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "extension": [
                {
                    "valueAttachment": {
                        "url": "https://canvas-vicert-test.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=Uh0EByy4Ie9cpGwYZF3bCYAn6sE%3D&Expires=1703597910"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature"
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "name": [
        {
            "use": "usual",
            "text": "Samantha Jones",
            "family": "Jones",
            "given": [
                "Samantha"
            ]
        }
    ],
    "telecom": [
        {
            "system": "PHONE",
            "value": "5554320555",
            "use": "MOBILE"
        },
        {
            "system": "PHONE",
            "value": "333555",
            "use": "WORK"
        },
        {
            "system": "EMAIL",
            "value": "samantha.jones@example.com",
            "use": "WORK"
        }
    ],
    "address": [
        {
            "use": "work",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "use": "work",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Samantha Jones: pk=21"
        },
        {
            "url": "https://canvas-vicert-test.s3.us-west-2.amazonaws.com/canvas-vicert-test/local/20231226_125820_48ce0458c73a46a087cee4a0a0c38d64.png",
            "title": "Samantha Jones: pk=22"
        },
        {
            "url": "https://canvas-vicert-test.s3.us-west-2.amazonaws.com/canvas-vicert-test/local/20231226_125821_35a2160829ec496e8baa280704dfa0e3.png",
            "title": "Samantha Jones: pk=23"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ],
                "display": "MD University Los Angeles"
            }
        }
    ]
}
```
{% endtab %}
{% tab practitioner-read-response 401 %}
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
{% tab practitioner-read-response 403 %}
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
{% tab practitioner-read-response 404 %}
```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "not-found",
            "details": {
                "text": "Unknown Practitioner resource '7d1ce256fcd7408193b0459650937a07'"
            }
        }
    ]
}

```
{% endtab %}
{% endtabs %}
</div>

<div id="practitioner-update-request">
{% tabs practitioner-update-request %}

{% tab practitioner-update-request curl %}
```sh
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Practitioner/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Practitioner",
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ]
        }
    ],
    "name": [
        {
            "use": "official",
            "family": "Jones",
            "given": [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given": [
                "Sammy"
            ]
        }
    ],
    "telecom": [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        },
        {
            "use": "work",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ]
            }
        }
    ],
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mNk+M9Qz0AEYBxVSF+FAAhKDveksOjmAAAAAElFTkSuQmCC"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"
        }
    ]
}
'
```
{% endtab %}

{% tab practitioner-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Practitioner",
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ]
        }
    ],
    "name": [
        {
            "use": "official",
            "family": "Jones",
            "given": [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given": [
                "Sammy"
            ]
        }
    ],
    "telecom": [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        },
        {
            "use": "work",
            "type": "both",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ]
            }
        }
    ],
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mNk+M9Qz0AEYBxVSF+FAAhKDveksOjmAAAAAElFTkSuQmCC"
        },
        {
            "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8/5+hnoEIwDiqkL4KAcT9GO0U4BxoAAAAAElFTkSuQmCC"
        }
    ]
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-update-response">
{% include update-response-practitioner.html %}
</div>

<div id="practitioner-search-request">
{% include search-request.html resource_type="Practitioner" search_string="name=Samantha" %}
</div>

<div id="practitioner-search-response">
{% tabs practitioner-search-response %}
{% tab practitioner-search-response 200 %}
```json
{
    "resourceType": "Practitioner",
    "id": "55096fbcdfb240fd8c999c325304de03",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueString": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueString": "1"
        },
        {
            "extension": [
                {
                    "valueAttachment": {
                        "url": "https://canvas-vicert-test.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=ljyujvD4fkgOG7b3SxlIokdDIlQ%3D&Expires=1703596102"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature"
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCode": "CC"
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "id": "test123456789test3",
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "name": [
        {
            "use": "usual",
            "text": "Samantha Jones",
            "family": "Jones",
            "given": [
                "Samantha"
            ]
        }
    ],
    "telecom": [
        {
            "system": "PHONE",
            "value": "5554320555",
            "use": "MOBILE"
        },
        {
            "system": "PHONE",
            "value": "333555",
            "use": "WORK"
        },
        {
            "system": "EMAIL",
            "value": "samantha.jones@example.com",
            "use": "WORK"
        }
    ],
    "address": [
        {
            "use": "work",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "use": "work",
            "line": [
                "1234 Main St., Los Angeles, CA 94107"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        }
    ],
    "gender": "F",
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Samantha Jones: pk=21"
        },
        {
            "url": "https://canvas-vicert-test.s3.us-west-2.amazonaws.com/canvas-vicert-test/local/20231226_125820_48ce0458c73a46a087cee4a0a0c38d64.png",
            "title": "Samantha Jones: pk=22"
        },
        {
            "url": "https://canvas-vicert-test.s3.us-west-2.amazonaws.com/canvas-vicert-test/local/20231226_125821_35a2160829ec496e8baa280704dfa0e3.png",
            "title": "Samantha Jones: pk=23"
        }
    ],
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "PRT-01"
                }
            ],
            "code": {
                "text": "License"
            },
            "period": {
                "start": "2020-01-01",
                "end": "2024-05-05"
            },
            "issuer": {
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDUB2"
                    }
                ],
                "display": "MD University Los Angeles"
            }
        }
    ]
}
```
{% endtab %}
{% tab practitioner-search-response 400 %}
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
{% tab practitioner-search-response 401 %}
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
{% tab practitioner-search-response 403 %}
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
