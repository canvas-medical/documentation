---
title: Practitioner
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        description: >-
         A person who is directly or indirectly involved in the provisioning of healthcare.<br><br>[https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-practitioner.html](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-practitioner.html)<br><br>To create a new staff member in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360058232193-Add-a-new-staff-member).<br><br>

         **Supported Extensions**
          <br><br>

          Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match. Extensions are all `json` types and should be included in the `extension` array field as shown in the request/response examples on this page. The following custom extensions are supported:<br><br>

          **`username`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/username](http://schemas.canvasmedical.com/fhir/extensions/username)
          <br><br>
          A username is a unique and often personalized identifier that an individual or entity uses to access a computer system, online platform, or any other service that requires user authentication. Expected value is string.
          <br><br>

          **`practitioner-personal-meeting-room-link`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link](http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link)
          <br><br>
          Practitioner meeting room link for online chat or meetings. Expected value is the meeting room link.
          <br><br>

          **`practitioner-primary-practice-location`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location](http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location)
          <br><br>
          The practitioner's primary practice location, where they spend most of their time. Expected value is reference to the Location model.
          <br><br>

          **`practitioner-signature`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature](http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature)
          <br><br>
          Attachment of the practitioner's real handwritten signature file. Expected value is a base64-encoded file.
          <br><br>

          **`roles`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/roles](http://schemas.canvasmedical.com/fhir/extensions/roles)
          <br><br>
          An array of roles with internal role codes as values. Examples of expected values include RN, CA, MA, etc.
          <br><br>



        attributes:
          - name: id
            description: >-
              Unique Canvas identifier for this resource.
            type: string
          - name: extension
            type: array[json]
            description: >-
              Reference the information at the top of this page to see the possible extensions contained in this resource.
          - name: identifier
            type: array[json]
            description: An identifier for the practitioner as this agent.
          - name: active
            type: boolean
            description: A boolean to specify if the practitioner is active in the healthcare system. If this value is not set, Canvas will default this to true.
          - name: name
            type: array[json]
            description: The name(s) associated with the practitioner.
          - name: telecom
            type: array[json]
            required: true
            description: >- 
                Practitioner contact point(s) (email / phone / fax). At least one contact field with the specifications 'system': 'phone' and 'use': 'work' is designated as the primary phone for staff or users. There must be exactly one contact field with the specifications 'system': 'email' and 'rank': 1. An error will be triggered if there is more than one email with rank 1, however, multiple emails with other ranks (e.g., rank 2, 3, 4, etc.) are allowed. Updating email contact fields is not permitted, during updates, the values must remain unchanged from the original creation or retrieval.
          - name: address
            type: array[json]
            required: true
            description: Address(es) of the practitioner entered in Canvas. Country will be "United States" by default.
          - name: birthDate
            type: date
            description: >-
              Practitioner date of birth for the individual, formatted as YYYY-MM-DD.
          - name: photo
            type: array[json]
            description: 	Practitioner photo(s).
          - name: qualification
            type: array[json]
            description: >-
               Practitioner license(s).<br>
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: include-non-scheduleable-practitioners
            type: boolean
            description: By default, only scheduleable practitioners are displayed. Passing this parameter as **true** will return all active practitioners.
          - name: active
            type: string
            description: Search by active status ("true" or "false" - case insensitive). By default if this param is not present, it will return practitioners with active set to True ("true").
          - name: name
            type: string
            description: A search that may match any of the string fields in the name, including family, given, prefix, suffix, and/or text. Partial search is supported. If the practitioner you are looking for is inactive, you will still need to pass `include-non-scheduleable-practitioners=true`.
          - name: email
            type: string
            description: Practitioner user email.
          - name: npiNumber
            type: string
            description: Practitioner NPI number.
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
          description: >-
            During the update (PUT) of 'addresses' and 'contacts' for practitioner, it is now expected that an 'id' is provided in the object of each 'address' or 'telecom' entity being updated. If 'id' is not provided, a new field will be created during the update, and any existing fields that are missing in comparison to those in the database (if not sent with an 'id') will be deleted. During an update, if a 'url' for the signature is provided, it will be ignored, and no action will be taken. For all other fields, if omitted from the (PUT) request, their values will be deleted in the database, including extensions. This applies to 'signature', 'primary practice location', 'meeting room link', 'photo', 'roles', and 'address' all of those entries will be erased. However, 'username' remains unchanged. If, for example, 'signature' or 'primary practice location' is omitted or 'meeting room link' is excluded, the values will be nullified. The same applies to 'photo', 'roles', and 'address' all of those entries will be deleted. Only for contact points, an empty array cannot be sent, nor can the field be omitted, as API validation will require the presence of required fields.
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
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-user-username",
            "valueString": "username123"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "active": true,
    "name": [
        {
            "use": "usual",
            "family": "Jones",
            "given": [
                "Samantha"
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
        },
        {
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-user-username",
            "valueString": "username123"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "valueAttachment": {
                "data": "data:application/pdf;base64,JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "extension": [
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "1920301155"
        }
    ],
    "active": True,
    "name": [
        {
            "use": "usual",
            "family": "Jones",
            "given": [
                "Samantha"
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
        },
        {
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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
    ]
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-create-response">
{% include create-response.html %}
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
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-user-username",
            "valueString": "username123"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location",
                "display": "Canvas Clinic San Francisco"
            }
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
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN",
                                "display": "Nurse"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA",
                                "display": "Medical Assistant"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC",
                                "display": "Care Coordinator"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "active": true,
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
            "id": "4fb49223-3d48-4bd6-8125-2ac62208efd6",
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "1a7f5403-2d9e-4156-a6e0-16c816e873fd",
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "id": "2d9490aa-ed57-46ef-8eec-ed5f22c38844",
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        },
        {
            "id": "4b8369cf-67e7-404d-8abe-51ff6e9ac835",
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "id": "5e76df8f-36c1-489a-8034-0916c7e8829f",
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "id": "33fe0a8f-1140-4ee3-b703-1afe42e8a3d6",
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location"
            }
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
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN",
                                "display": "Nurse"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA",
                                "display": "Medical Assistant"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC",
                                "display": "Care Coordinator"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "active": true,
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
            "id": "4fb49223-3d48-4bd6-8125-2ac62208efd6",
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "1a7f5403-2d9e-4156-a6e0-16c816e873fd",
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "id": "2d9490aa-ed57-46ef-8eec-ed5f22c38844",
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        },
        {
            "id": "4b8369cf-67e7-404d-8abe-51ff6e9ac835",
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "id": "5e76df8f-36c1-489a-8034-0916c7e8829f",
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "id": "33fe0a8f-1140-4ee3-b703-1afe42e8a3d6",
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location"
            }
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
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN",
                                "display": "Nurse"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA",
                                "display": "Medical Assistant"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC",
                                "display": "Care Coordinator"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "active": True,
    "name": [
        {
            "use": "usual",
            "family": "Jones",
            "given": [
                "Samantha"
            ]
        }
    ],
    "telecom": [
        {
            "id": "4fb49223-3d48-4bd6-8125-2ac62208efd6",
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "1a7f5403-2d9e-4156-a6e0-16c816e873fd",
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "id": "2d9490aa-ed57-46ef-8eec-ed5f22c38844",
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        },
        {
            "id": "4b8369cf-67e7-404d-8abe-51ff6e9ac835",
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "id": "5e76df8f-36c1-489a-8034-0916c7e8829f",
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "id": "33fe0a8f-1140-4ee3-b703-1afe42e8a3d6",
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}

{% endtabs %}
</div>

<div id="practitioner-update-response">
{% include update-response.html %}
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
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-user-username",
            "valueString": "username123"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link",
            "valueUrl": "https://meet.google.com/room-001"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location",
            "valueReference": {
                "reference": "Location/95b9ac2d-e963-4d7a-b165-7901870f1663",
                "type": "Location",
                "display": "Canvas Clinic San Francisco"
            }
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
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "RN",
                                "display": "Nurse"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "MA",
                                "display": "Medical Assistant"
                            }
                        ]
                    }
                },
                {
                    "url": "code",
                    "valueCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://schemas.canvasmedical.com/fhir/roles",
                                "code": "CC",
                                "display": "Care Coordinator"
                            }
                        ]
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi ",
            "value": "1920301155"
        }
    ],
    "active": true,
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
            "id": "4fb49223-3d48-4bd6-8125-2ac62208efd6",
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "1a7f5403-2d9e-4156-a6e0-16c816e873fd",
            "system": "phone",
            "value": "333555",
            "use": "work",
            "rank": 1
        },
        {
            "id": "2d9490aa-ed57-46ef-8eec-ed5f22c38844",
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        },
        {
            "id": "4b8369cf-67e7-404d-8abe-51ff6e9ac835",
            "system": "email",
            "value": "samantha.jones2@example.com",
            "use": "work",
            "rank": 2
        }
    ],
    "address": [
        {
            "id": "5e76df8f-36c1-489a-8034-0916c7e8829f",
            "use": "work",
            "line": [
                "1234 Main St"
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        },
        {
            "id": "33fe0a8f-1140-4ee3-b703-1afe42e8a3d6",
            "use": "work",
            "line": [
                "12 Cesar Chavez St"
            ],
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94110",
            "country": "United States"
        }
    ],
    "birthDate": "1988-10-10",
    "photo": [
        {
            "url": "https://fastly.picsum.photos/id/1064/200/300.jpg?hmac=Joir_QEJYjd2_bmYco64ek_C2TSsfReMcWWcXYsObKI",
            "title": "Profile photo 1 -- sample title"
        },
        {
            "url": "https://fastly.picsum.photos/id/674/200/300.jpg?hmac=kS3VQkm7AuZdYJGUABZGmnNj_3KtZ6Twgb5Qb9ITssY"
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
