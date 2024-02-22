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
          Attachment of the practitioner's real handwritten signature file. Expected value is a base64-encoded file during Practitioner create. More info on updating signatures can be found below in the Practitioner update section.
          <br><br>

          **`roles`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/roles](http://schemas.canvasmedical.com/fhir/extensions/roles)
          <br><br>
          An array of roles with internal role codes as values. Examples of expected values include RN, CA, MA, etc. For more detailed information, look into the payload examples or read the instructions below.
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
            description: 
              An identifier for the practitioner as this agent.
              <br><br>
              This is the NPI number of Staff in Canvas database.
              <br><br>
              It accepts only one array item. That signle item must have **system** set to "http://hl7.org/fhir/sid/us-npi" and the **value** must be a 10 digit number.
          - name: active
            type: boolean
            description: A boolean to specify if the practitioner is active in the healthcare system. If this value is not set, Canvas will default this to true.
          - name: name
            type: array[json]
            required: true
            description: The name(s) associated with the practitioner.
            create_description: >-
              The name(s) associated with the practitioner. Value for "use" must be set to "usual". At this point, this API is accepting only "family" (last) name and only one "given" name. See the payload examples for concrete details.
            update_description: >-
              The name(s) associated with the practitioner. Value for "use" must be set to "usual". At this point, this API is accepting only "family" (last) name and only one "given" name. See the payload examples for concrete details.
          - name: telecom
            type: array[json]
            description: >- 
              Practitioner contact point(s) (email / phone / fax). 
              <br><br>
              At least one contact field with the specifications **'system'**: **'phone'** and **'use'**: **'work'** is designated as the primary phone for staff or users.
              <br><br>
              There must be exactly one contact field with the specifications **'system'**: **'email'** and **'rank'**: **1**. An error will be triggered if there is more than one email with rank 1, however, multiple emails with other ranks (e.g., rank 2, 3, 4, etc.) are allowed.
              <br><br>
              **IMPORTANT**: Updating email contact fields is not permitted, during updates, the values must remain unchanged from the original creation or retrieval.
            attributes:
              - name: id
                type: string
                description: The identifier (ID) of the telecom (contact point) record in Canvas database.
                create_description:
                  The identifier (ID) of the telecom (contact point) record in Canvas database. <br><br>
                  This "id" property is only needed during updates. For more info on that, check the update part of these docs.
                update_description:
                  The identifier (ID) of the telecom (contact point) record in Canvas database. <br><br>
                  If you want to update specific telecom record in Canvas database, you are going to use this property to target that record. <br><br>
                  If you omit "id" during update, a new telecom record will be created.
              - name: system
                type: string
                required: true
                description: Supported values are **phone**, **fax**, **email**, **pager**, and **other**.
              - name: value
                type: string
                required: true
                description: Free text string of the value for this contact point.
                create_description: 
                  Free text string of the value for this contact point.<br><br>
                  Values for phone numbers (where "system" is set to "phone") must be only digits, with no sign characters or spaces.
                update_description:
                  Free text string of the value for this contact point.<br><br>
                  Values for phone numbers (where "system" is set to "phone") must be only digits, with no sign characters or spaces.
              - name: use
                type: string
                required: true
                description: Supported values are  **home**, **work**, **temp**, **old** and **mobile**.
              - name: rank
                type: integer
                required: true
                description: An integer representing the preferred order of contact points per system.
          - name: address
            type: array[json]
            required: true
            description: Address(es) of the practitioner entered in Canvas database. No default values will be set.
            attributes:
              - name: id
                type: string
                description: The identifier (ID) of the address record in Canvas database.
                create_description:
                  The identifier (ID) of the address record in Canvas database. <br><br>
                  This "id" property is only needed during updates. For more info on that, check the update part of these docs.
                update_description:
                  The identifier (ID) of the address record in Canvas database. <br><br>
                  If you want to update specific address record in Canvas database, you are going to use this property to target that record. <br><br>
                  If you omit "id" during update, a new address record will be created.
              - name: use
                type: string
                required: true
                description: Supported values are **home**, **work**, **temp**, **old** and **billing**.
              - name: type
                type: string
                required: true
                description: Supported values are **both**, **physical** and **postal**.
              - name: line
                type: string
                description: List of strings. The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be address line 2.
              - name: city
                type: string
                description: String representing the city of the address.
              - name: state
                type: string
                description: 2 letter state abbreviation of the address.
              - name: postalCode
                type: string
                description: The 5 digit postal code of the address.
              - name: country
                type: string
          - name: birthDate
            type: date
            description: >-
              Practitioner date of birth for the individual, formatted as YYYY-MM-DD.
          - name: photo
            type: array[json]
            description: Practitioner photo(s).
            create_description: >-
              Practitioner photo(s). <br><br>
              Apart from setting "title" to each photo, on create this API is accepting only "url" values for now. Titles are optional.
            update_description: >-
              Practitioner photo(s). <br><br>
              You cannot directly update any photo during update. You can only remove certain photos by ommiting them form the payload and add new ones with which you want to replace them. Titles are optional.
          - name: qualification
            type: array[json]
            description: >-
              Practitioner license(s)
            create_description: >-
              Practitioner license(s). <br><br>
              See the payload examples for more details.
            create_description: >-
              Practitioner license(s). <br><br>
              See the payload examples for more details.

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
          description: >-
            Create Practitioner with provided fields and values.
            <br><br>
            **IMPORTANT**: You cannot send an empty list for "telecom", nor omit the telecom field from the payload. The required fields in telecom are email and phone. Only one email with rank 1 and at least one "work" phone number. For detailed information on this, check the telecom attributes description.

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
            Update Practitioner with provided fields and values.
            <br><br>
            During the update (PUT) of 'addresses' and 'contacts' for practitioner, it is expected that an **'id'** is provided in the object of each 'address' or 'telecom' entity being updated. If 'id' is not provided, a new field will be created during the update, and any existing fields that are missing in comparison to those in the database (if not sent with an 'id') will be deleted. 
            <br><br>
            During an update, if a **'url'** for the signature is provided, it will be ignored, and no action will be taken.
            <br><br>
            For all other fields, if omitted from the (PUT) request, their values will be deleted in the database, including extensions. This applies to 'signature', 'primary practice location', 'meeting room link', 'photo', 'roles', and 'address' all of those entries will be erased if their respective extensions are excluded from the payload during update (PUT HTTP method call). However, only the 'username' remains unchanged and this API will return error if the PUT payload is trying to change the Practitioner's (Staff) username. The same applies to 'photo' and to the list of role codes in 'roles' extension, all of those entries will be deleted if they are ommited from the payload during the update.
            <br><br>
            **IMPORTANT**: You cannot send an empty list for "telecom", nor omit the telecom field from the payload. The required fields in telecom are email and phone. Only one email with rank 1 and at least one "work" phone number. For detailed information on this, check the telecom attributes description.

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
