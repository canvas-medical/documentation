---
title: Practitioner
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Practitioner
        article: "a"
        description: >-
         A person who is directly or indirectly involved in the provisioning of healthcare.<br><br>[https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-practitioner.html](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-practitioner.html)<br><br>To create a new staff member manually in the Canvas UI, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360058232193-Add-a-new-staff-member).<br><br>
          
        attributes:
          - name: id
            type: string
            required_in: update
            description: >-
              Unique Canvas identifier for this resource.
          - name: extension
            type: array[json]
            description: Canvas supports specific FHIR extensions on this resource. 
            create_description: Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match.
            update_description: Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match.<br><br> 
              During updates, When an extension is omitted from the payload request, it will be considered as an intention to remove the value stored associated to that field, thus their values will be deleted in Canvas. The only exception is the username extension, which remains unchanged and this API will return error if the update request is trying to change the Practitioner’s (Staff) username.
            attributes:
              - name: url
                type: string
                required_in: create, update
                description: Identifies the meaning of the extension
                enum_options:
                  - value: http://schemas.canvasmedical.com/fhir/extensions/username
                  - value: http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link
                  - value: http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location
                  - value: http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature
                  - value: http://schemas.canvasmedical.com/fhir/extensions/roles
              - name: valueString
                type: string
                description: Value of extension.<br><br> The `valueString` attribute is needed for the role's extension where the `url` is `http://schemas.canvasmedical.com/fhir/extensions/username`. <br><br> A username is a unique and often personalized identifier that an individual or entity uses to access a computer system, online platform, or any other service that requires user authentication
              - name: valueUrl
                type: string
                description: Value of extension.<br><br> The `valueUrl` attribute is needed for the meeting link extension where the `url` is `http://schemas.canvasmedical.com/fhir/extensions/practitioner-personal-meeting-room-link`. This value will represent the url that will be associated to any telehealth notes in Canvas. 
              - name: valueReference
                type: json
                description: Value of extension.<br><br> The `valueReference` attribute is needed for the primary location extension where the `url` is `http://schemas.canvasmedical.com/fhir/extensions/practitioner-primary-practice-location`. This attribute will be the reference the practitioner's primary location they practice at. 
                attributes:
                  - name: reference
                    type: string
                    required_in: create
                    description: The reference string of the location in the format of `"Location/95b9ac2d-e963-4d7a-b165-7901870f1663"`.
                  - name: type
                    type: string
                    description: Type the reference refers to (e.g. "Location").
              - name: valueAttachment
                type: json
                description: Value of extension.<br><br> The `valueAttachment` attribute is needed for the signature extension where the `url` is `http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature`. This attribute represents the attachment of the practitioner’s real handwritten signature file.
                attributes:
                  - name: data
                    type: string
                    description: A base64-encoded file. 
                    required_in: create
                    exclude_in: search, read
                  - name: url
                    type: string
                    description: Uri where the data can be found.
                    exclude_in: create, update
              - name: extension
                type: array[json]
                description: For the Role extensions where the url is `http://schemas.canvasmedical.com/fhir/extensions/roles`, the `extension` attribute is used to define the list of role's this practitioner has at the practice. 
                attributes: 
                  - name: url
                    type: string
                    description: Identifies the meaning of the extension.
                    enum_options: 
                      - value: code
                  - name: valueCoding
                    type: json
                    required_in: create, update
                    attributes: 
                      - name: system
                        description: The system url of the coding.
                        type: string
                        enum_options: 
                          - value: http://schemas.canvasmedical.com/fhir/roles
                      - name: code
                        required_in: create, update
                        description: The internal code. Examples of expected values include RN, CA, MA, etc. Some of these values are built in to each Canvas instance but are customizable. See this [zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/12851926883859-Creating-and-modifying-roles) for more information.
                        type: string
                      - name: display
                        description: The display name of the coding.
                        type: string
          - name: identifier
            type: array[json]
            description: A secondary identifier for the Practitioner. This is the NPI number of the Practitioner in Canvas.
            attributes:
              - name: system
                type: string
                description: The `system` attribute specifies the namespace in which the identifier value is unique. 
                enum_options:
                  - value: http://hl7.org/fhir/sid/us-npi
              - name: value
                type: string
                description: Practitioner's NPI number. Its value must be a 10 digit number.
          - name: active
            type: boolean
            description: A boolean to specify if the practitioner is active in the healthcare system. If this value is not set, Canvas will default this to true.
          - name: name
            type: array[json]
            required_in: create, update
            description: The name associated with the practitioner.
            attributes:
              - name: use
                type: enum [ ususal ]
                description: The 'use' attribute specifies the context in which the name is used. For this API, the only permitted value is 'usual,' which indicates that the name provided is the name typically used to identify the practitioner in daily practice.
                required_in: create, update
              - name: family
                type: string
                description: Practitioner's last name.
                required_in: create, update
              - name: given
                type: array[string]
                required_in: create, update
                description: Practitioner's first name. Only one first name is allowed.
          - name: telecom
            type: array[json]
            required_in: create, update
            description: Practitioner contact point(s) (email / phone / fax).
            create_description: >-
              Practitioner contact point(s) (email / phone / fax).
              <br><br>
              At least one contact point with the specifications `system`: **phone** and `use`: **work** is required and it is designated as the primary phone for the Practitioner.
              <br><br>
              There must be exactly one contact point with the specifications `system`: **email** and `rank`: **1**. An error will be triggered if there is more than one `email` with `rank` set to **1**, however, multiple emails with other ranks (e.g., rank 2, 3, 4, etc.) are allowed.
            update_description: >-
              Practitioner contact point(s) (email / phone / fax).
              <br><br>
              At least one contact point with the specifications `system`: **phone** and `use`: **work** is required as the primary phone for the Practitioner.
              <br><br>
              There must be exactly one contact point with the specifications `system`: **email** and `rank`: **1**. An error will be triggered if there is more than one `email` with `rank` set to **1**, however, multiple emails with other ranks (e.g., rank 2, 3, 4, etc.) are allowed.
              <br><br>
              **IMPORTANT**: Updating email contact points is not permitted. During updates, the values must remain unchanged from the original creation or retrieval.
            attributes:
              - name: id
                type: string
                description: The identifier (ID) of the telecom (contact point) record in Canvas.
                exclude_in: create
                update_description:
                  The identifier (ID) of the telecom (contact point) record in Canvas. <br><br>
                  If you want to update a specific telecom record in Canvas, use this property to target that record. <br><br>
                  If you omit "id" during update, a new telecom record will be created.
              - name: system
                type: enum [ phone | fax | email | pager | other ]
                required_in: create, update
                description: Telecommunications form for contact point - what communications system is required to make use of the contact.
              - name: value
                type: string
                required_in: create, update
                description: The actual contact point details, in a form that is meaningful to the designated communication system (i.e. phone number or email address).
                create_and_update_description:
                  The actual contact point details, in a form that is meaningful to the designated communication system (i.e. phone number or email address).
                  Values for phone numbers (where "system" is set to "phone") must be only digits, with no sign characters or spaces.
              - name: use
                type: enum [ home | work | temp | old | mobile ]
                required_in: create, update
                description: Identifies the purpose for the contact point.
              - name: rank
                type: integer
                required_in: create, update
                description: Specifies a preferred order in which to use a set of contacts. ContactPoints with lower rank values are more preferred than those with higher rank values.
          - name: address
            type: array[json]
            description: Address(es) of the practitioner entered in Canvas. No default values will be set.
            attributes:
              - name: id
                type: string
                description: The identifier (ID) of the address record in Canvas.
                exclude_in: create
                update_description:
                  The identifier (ID) of the address record in Canvas. <br><br>
                  If you want to update a specific address record in Canvas, use this property to target that record. <br><br>
                  If you omit "id" during update, a new address record will be created.
              - name: use
                type: enum [ home | work | temp | old | billing ]
                required_in: create, update
                description: Defines the purpose of this address.
              - name: type
                type: enum [ both | physical | postal ] 
                required_in: create, update
                description: Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.
              - name: line
                type: array[string]
                description: This component contains the house number, apartment number, street name, street direction, P.O. Box number, delivery hints, and similar address information.<br><br> The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be address line 2.
              - name: city
                type: string
                description: The name of the city, town, suburb, village or other community or delivery center.
              - name: state
                type: string
                description: Two-letter state abbreviation of the address.
              - name: postalCode
                type: string
                description: The 5-digit postal code of the address.
              - name: country
                type: string
                description: Specifies the country in which the practitioner's address is located. This field typically contains the name of the country, following the ISO 3166 standard.
          - name: birthDate
            type: date
            description: The date on which the practitioner was born, formatted as YYYY-MM-DD.
          - name: photo
            type: array[json]
            description: Practitioner photo(s).
            attributes:
              - name: url
                type: string
                required_in: create, update
                description: Uri where the data can be found.
              - name: title
                type: string
                description: Label to display in place of the data.
          - name: qualification
            type: array[json]
            description: Practitioner license(s)
            attributes:
              - name: identifier
                type: array[json]
                required_in: create, update
                description: This component identifies the issuing authority of the Practitioner's qualification (license).
                attributes:
                  - name: system
                    type: string
                    description: The `system` attribute specifies the namespace in which the identifier value is unique. 
                    enum_options:
                      - value: http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url
                  - name: value
                    type: string
                    description: The `value` attribute contains the actual identifier assigned to the practitioner's qualification. This value is unique within the context defined by the `system` attribute. It can be any string that serves as a meaningful identifier, such as a license number, certification ID, or other relevant qualification identifiers.
              - name: code
                type: object[json]
                description: License coding object. This attribute has no effect.
                attributes:
                  - name: text
                    type: string
                    description: This field has no effect. Provide **"License"** as value.
                    enum_options:
                      - value: License
              - name: period
                type: object[json]
                required_in: create, update
                description: A component of the Practitioner's license that defines validity period of the license with starting and the ending dates.
                attributes:
                  - name: start
                    type: string
                    description: Start date of the Practitioner's license. Expected date format is YYYY-MM-DD (Example - "2020-01-01")
                  - name: end
                    type: string
                    description: Start date of the Practitioner's license. Expected date format is YYYY-MM-DD (Example - "2020-01-01")
              - name: issuer
                type: object[json]
                description: A component of the Practitioner's license object that defines the license issuing authority short name.
                attributes:
                  - name: display
                    type: string
                    description: The display text of the license's short name.
                  - name: extension
                    type: array[json]
                    attributes:
                      - name: url
                        type: string
                        description: Reference that defines the content of this object.
                        enum_options:
                          - value: http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name
                      - name: valueString
                        type: string
                        description: The issuing authority short name.
                  
        search_parameters:
          - name: _id
            type: string
            description: A Canvas-issued unique identifier
          - name: include-non-schedulable-practitioners
            type: boolean
            description: By default, only schedulable practitioners are displayed. Passing this parameter as "true" will return both schedulable and non-schedulable practitioners.
          - name: active
            type: string
            description: Search by `active` status ("true" or "false" - case insensitive). By default if this param is not present, it will return practitioners with `active` set to True ("true").
          - name: name
            type: string
            description: A search that may match any of the string fields in the name, including `family`, `given`, `prefix`, `suffix`, and/or `text`. Partial search is supported.
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
          description: Create Practitioner with provided fields and values.

        read:
          responses: [200, 401, 403, 404]
          example_request: practitioner-read-request
          example_response: practitioner-read-response
          description: Read a Practitioner resource

        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: practitioner-update-request
          example_response: practitioner-update-response
          description: Update Practitioner with provided fields and values.

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
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                        "valueString": "MDU LA"
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
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                        "valueString": "MDU LA"
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
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature"
            "extension": [
                {
                    "valueAttachment": {
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=ljyujvD4fkgOG7b3SxlIokdDIlQ%3D&Expires=1703596102"
                    }
                }
            ],
            
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDU LA"
                    }
                ]
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
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "extension": [
                {
                    "valueAttachment": {
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=ljyujvD4fkgOG7b3SxlIokdDIlQ%3D&Expires=1703596102"
                    }
                }
            ]
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDU LA"
                    }
                ]
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
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=ljyujvD4fkgOG7b3SxlIokdDIlQ%3D&Expires=1703596102"
                    }
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDU LA"
                    }
                ]
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
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-signature",
            "extension": [
                {
                    "valueAttachment": {
                        "url": "https://canvas-client-media.s3.amazonaws.com/local/signature-cdfkizrj.pdf?AWSAccessKeyId=AKIA5KJ2QWTAU572JXPZ&Signature=ljyujvD4fkgOG7b3SxlIokdDIlQ%3D&Expires=1703596102"
                    }
                }
            ]
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/roles",
            "extension": [
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "RN"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "MA"
                    }
                },
                {
                    "url": "code",
                    "valueCoding": {
                        "system": "http://schemas.canvasmedical.com/fhir/roles",
                        "code": "CC"
                    }
                }
            ]
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
                "display": "MD University Los Angeles",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "MDU LA"
                    }
                ]
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
