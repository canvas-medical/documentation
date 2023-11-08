---
title: Patient
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
        article: "a"
        description: >-
          Demographics and other administrative information about an individual or animal receiving care or other health-related services.<br><br> [http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-patient.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-patient.html)<br><br>

          **Supported Extensions**
          <br><br>

          Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match. Extensions are all `json` types and should be included in the `extension` array field as shown in the request/response examples on this page. The following extensions are supported:<br><br>

          **`birthsex`**
          <br><br>
          [http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex](http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex)
          <br><br>
          A code classifying the person’s sex assigned at birth as specified by the Office of the National Coordinator for Health IT (ONC). This extension aligns with the C-CDA Birth Sex Observation (LOINC 76689-9). After version 6.0.0, this extension is no longer a USCDI Requirement.
          <br><br>
          Supported values are:

            | value | description |
            | :---- | ---------   |
            | **M** | Male        |
            | **F** | Female      |
            | **O** | Other       |
            | **U** | Unknown     |

          **`genderIdentity`**
          <br><br>
          [http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity](http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity)
          <br><br>
          This extension provides concepts to describe the gender a person identifies as.
          <br><br>
          Please note that if this extension is included, it will override the root `gender` field. Supported values are:

            | value | description |
            | :---- | ---------   |
            | **446151000124109** | Identifies as Male |
            | **446141000124107** | Identifies as Female |
            | **407377005** | Female-to-Male (FTM)/Transgender Male/Trans Man |
            | **407376001** | Male-to-Female (MTF)/Transgender Female/Trans Woman |
            | **446131000124102** | Genderqueer, neither exclusively male nor female |
            | **OTH** | Additional gender category or other, please specify |
            | **ASKU** | Choose not to disclose |

          **`sexual-orientation`**
          <br><br>
          http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation
          <br><br>
          Sexual orientation of the patient. Supported values are:

            | value | description |
            | :---- | ---------   |
            | **20430005** | Straight or heterosexual |
            | **38628009** | Lesbian, gay or homosexual |
            | **42035005** | Bisexual |
            | **OTH** | Something else, please describe |
            | **UNK** | Don’t Know |
            | **ASKU** | Choose not to disclose |

          **`race`**
          <br><br>
          [http://hl7.org/fhir/us/core/StructureDefinition/us-core-race](http://hl7.org/fhir/us/core/StructureDefinition/us-core-race)<br><br>
          An extension to specify the races of a patient.
          <br><br>
          For create and update actions, the `url` attribute must equal **http://hl7.org/fhir/us/core/StructureDefinition/us-core-race**. Additionally, a list of objects where each object contains a `valueCoding` object with the value **urn:oid:2.16.840.1.113883.6.238** and the appropriate code of each race needed from the ValueSet.<br><br>

          **`ethnicity`**
          <br><br>
          [http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity](http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity)<br><br>
          An extension to specify the ethnicities of a patient.
          <br><br>
          For create and update actions, the `url` attribute must equal **http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity**. Additionally, a list of objects where each object contains a `valueCoding` object with the value **urn:oid:2.16.840.1.113883.6.238** and the appropriate code of each race needed from the ValueSet.<br><br>

          **`timezone`**
          <br><br>
          [http://hl7.org/fhir/StructureDefinition/tz-code](http://hl7.org/fhir/StructureDefinition/tz-code)
          <br><br>
          The timezone a patient lives in.
          <br><br>
          For create and update actions, the `url` attribute must equal **http://hl7.org/fhir/StructureDefinition/tz-code**, and the `valueCode` can contain any valid timezone code defined [here](http://build.fhir.org/valueset-timezones.html).<br><br>

          **`clinical-note`**
          <br><br>
          http://schemas.canvasmedical.com/fhir/extensions/clinical-note
          <br><br>
          This note displays under the patient's name in the clinical chart.
          <br><br>
          For create and update actions, the `url` attribute must equal **http://schemas.canvasmedical.com/fhir/extensions/clinical-note**. The `valueString` attribute is a free text field.<br><br>

          **`administrative-note`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/administrative-note](http://schemas.canvasmedical.com/fhir/extensions/administrative-note)
          <br><br>
          This note displays under the patient's name in the administrative profile.
          <br><br>
          For create and update actions, the `url` attribute must equal **http://schemas.canvasmedical.com/fhir/extensions/administrative-note**. The `valueString` attribute is a free text field.<br><br>

          **`preferred-pharmacy`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy](http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy)
          <br><br>
          A patient can have multiple preferred pharmacies added to their profile.
          <br><br>
          For create and update actions, the `url` attribute must be equal to *http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy*. For each object in `extension`, a `url` attribute with the value **ncpdp-id** should be included along with a `valueIdentifier` object including the NCPDP number of the pharmacy under `value` and the url **http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber** under `system`.<br><br>

          **`business-line`**
          <br><br>
          [http://schemas.canvasmedical.com/fhir/extensions/business-line](http://schemas.canvasmedical.com/fhir/extensions/business-line)
          <br><br>
          The business line that the patient belongs to.
          <br><br>
          Not all Canvas instances have Business Line functionality enabled. See [here](https://canvas-medical.zendesk.com/hc/en-us/articles/16777163916307-Customized-Patient-Communication#h_01H0T0Z79XFX215GRSABFC91JZ) for information on Business Lines.<br><br>
          If using business line functionality, create and update actions should include a json object with the `url` attribute equal to **http://schemas.canvasmedical.com/fhir/extensions/business-line** and the `valueId` set to the externallyExposableId of the business line in Canvas.

        attributes:
          - name: id
            type: string
            description: Unique Canvas identifier for this resource
          - name: text
            type: json
            description: A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource.
          - name: extension
            type: array[json]
            description: Reference the information at the top of this page to see the possible extensions contained in this resource. Please note that the `birthsex` extension is required.
          - name: identifier
            type: array[json]
            description: The identifier list defines additional identifiers that are able to be stored for a patient.
            create_description: The identifier list defines additional identifiers that are able to be stored for a patient. None of these identifiers will be surfaced on the Patient's chart but may help you to identify the patient in your internal system.
            update_description: The identifier list defines additional identifiers that are able to be stored for a patient. None of these identifiers will be surfaced on the Patient's chart but may help you to identify the patient in your internal system. If an <code>identifier</code> already exists in the Canvas database and is not included in the Update message, it will be deleted if and only if the period.end date is in the future.
            attributes:
              - name: use
                type: string
                description: Supported values are **usual**, **official**, **temp**, **secondary** and **old**. If omittted, the default value is **usual**.
              - name: system
                type: string
                description: Free text field to identify what this value represents.
              - name: value
                type: string
                description: Free text field to store the patient's identifier.
              - name: period
                type: date
                description: This is used to specify the start and end dates (format YYYY-MM-DD). If period is omitted it will default to <code>start</code> = 1970-01-01 and <code>end</code> = 2100-12-31. There is currently no validation if the end date is before the start date.
          - name: active
            type: boolean
            description: A boolean to specify if the patient is active in the healthcare system. If this value is not set, Canvas will default this to true.
          - name: name
            type: array[json]
            required: true
            description: >-
                The identifier of the patient. Name is a `required` list of objects.<br><br> One iteration must be marked with `use`: `official`. The first object with `use`: `official` will determine the patient's first, last, prefix, suffix or middle name. The first and last name is required within Canvas. For example: <br><br> • the `family` attribute will populate the patient's last name. <br>• the `given` list will populate the patient's first/middle name. The first item in the list will be the first name, while if more items in the list exists, it will populate the patient's middle name and be joined together with an empty space. <br>• the `prefix` attribute will be stored within Canvas's database but will not be displayed in the Canvas UI.<br>• the `suffix` attribute will be displayed on the Canvas UI but it will not be editable through the UI. <br><br> The example also demonstrates that Canvas ingests a nickname (preferred name) for the Patient. This element is identified by `use = nickname` and the first item in the given list will be the Patient's nickname. Canvas can also ingest old names or maiden names using `use`: `maiden` or `use`: `old`. These will not show up on the Canvas UI but will be stored by Canvas and will be returned via a read request.<br><br> In the Canvas UI, each patient will be displayed as `first-last-suffix (nickname)`. Searches can be performed using first, middle, last, suffix or nickname.<br><br>If there are any other objects defined in the name list they will be ignored.
          - name: telecom
            type: array[json]
            required: false
            description: Contact details for the individual.
            create_description: >-
                Telecom is an optional list of objects where you can provide the child  attributes listed below. Email and Phone system's will be surfaced in the Canvas UI. Currently Canvas stores the other systems in our database, but does not display them.
            update_description:
                Telecom is an optional list of objects where you can provide the child  attributes listed below. Email and Phone system's will be surfaced in the Canvas UI. Currently Canvas stores the other systems in our database, but does not display them.
            attributes:
              - name: id
                type: string
              - name: extension
                type: array
                description: >-
                    This is an optional object that you can specify for a Patient's phone number or email. This tells Canvas that the patient has consented to receiving text messages or emails to this contact point. This extension is identified with the <code>url</code> [http://schemas.canvasmedical.com/fhir/extensions/has-consent](http://schemas.canvasmedical.com/fhir/extensions/has-consent). A boolean value can be specified in the <code>valueBoolean</code> attribute.<br><br>
                    **Note:** This will not send a verification email or text as is the Canvas UI does. It will bypass this step and mark the contact as verified.
                attributes:
                  - name: url
                    type: string
                  - name: valueBoolean
                    type: boolean
              - name: system
                type: string
                description: Supported values are **phone**, **fax**, **email**, **pager**, **url**, **sms**, and **other**. If omitted, the default value is **other**.
              - name: value
                type: string
                required: true
                description: Free text string of the value for this contact point
              - name: use
                type: string
                description: Supported values are  **home**, **work**, **temp**, **old** and **mobile**. If omitted, the default value is **home**.
              - name: rank
                type: integer
                description: An integer representing the preferred order of contact points per system. The default value is 1.
          - name: gender
            type: string
            required: true
            description: >-
              A enum value that maps to the gender identity attribute in the Canvas UI. Supported values are **male**, **female**, **other** and **unknown**.<br><br>
              [https://hl7.org/fhir/R4/valueset-administrative-gender.html](https://hl7.org/fhir/R4/valueset-administrative-gender.html)
            create_description: >-
                The gender attribute is an optional string enum value that maps to our gender identity attribute on our UI. Currently Canvas accepts the following FHIR values: male, female, other, and unknown. <br><br> If <code>unknown</code> is entered at the time of creation, the patient chart will show gender as 'choose not to disclose'. If <code>other</code> is selected, the patient chart will display `Additional gender category or other, please specify` in the gender field.
            update_description: >-
                The gender attribute is an optional string enum value that maps to our gender identity attribute on our UI. Currently Canvas accepts the following FHIR values: male, female, other, and unknown. <br><br> If <code>unknown</code> is entered at the time of creation, the patient chart will show gender as 'choose not to disclose'. If <code>other</code> is selected, the patient chart will display `Additional gender category or other, please specify` in the gender field.
          - name: birthDate
            type: date
            required: true
            description: >-
              The date of birth for the individual, formatted as YYYY-MM-DD.
            create_description: >-
                 The birthDate field is required in Canvas for a patient. This is a string date format that is defined here. For Canvas it is best to get the format YYYY-MM-DD. If only a month and year is given, the birthdate is set to the 1st of the given month by default. If only a year is given, the birthdate defaults to January 1st of that year. To summarize, Canvas accepts the following formats: YYYY, YYYY-MM, and YYYY-MM-DD.
            update_description: >-
             The birthDate field is required in Canvas for a patient. This is a string date format that is defined here. For Canvas it is best to get the format YYYY-MM-DD. If only a month and year is given, the birthdate is set to the 1st of the given month by default. If only a year is given, the birthdate defaults to January 1st of that year. To summarize, Canvas accepts the following formats: YYYY, YYYY-MM, and YYYY-MM-DD.
          - name: deceasedBoolean
            type: boolean
            required: false
            description: Indicates if the individual is deceased or not.
          - name: address
            type: array[json]
            required: false
            description: Address(es) for the individual.
            attributes:
              - name: id
                type: string
              - name: use
                type: string
                description: Supported values are **home**, **work**, **temp** and **old**. If omitted, the default value is **home**.
              - name: type
                type: string
                description: Supported values are **both**, **physical** and **postal**. If omitted, the default value is **both**.
              - name: line
                type: string
                description:  List of strings. The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be address line 2.
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
              - name: period
                type: json
                attributes:
                  - name: start
                    type: date
                  - name: end
                    type: date
          - name: photo
            type: array[json]
            description: Image of the patient. This image shows on the patient avatar in the Canvas UI.
            create_description: >-
              When creating a `Patient` resource, a `data` attribute should include the photo as a base64-encoded string. This is different from a read or search, where a `url` attribute will contain a URL to the file.
            update_description: >-
              When updating a `Patient` resource, a `data` attribute should include the photo as a base64-encoded string. This is different from a read or search, where a `url` attribute will contain a URL to the file.
          - name: contact
            type: array[json]
            required: false
            description: A contact party (e.g. guardian, partner, friend) for the patient. Contact details will display on the Patient profile page in the Canvas UI.
            attributes:
              - name: id
                type: string
                description: A Canvas identifier for the contact.
              - name: name
                type: json
                required: true
                description: This is an object where you can specify the <code>text</code> that stores the contact's name.
                attributes:
                  - name: text
                    type: string
              - name: relationship
                type: array[json]
                description: This is a list of objects where you can specify the text that stores the contact's relationship. It is a free text field. While a list, Canvas currently only stores and displays the text of the first object.
                attributes:
                  - name: text
                    type: string
              - name: telecom
                type: json
                description: This is a list of objects where Canvas will take the first system equal to phone and store as the contact's phone number. Then the first system equal to email will be stored as this contact's email address. The value of the email or phone number is stored in the value field. If any other option is passed in the system field, the data will not be stored.
                attributes:
                  - name: system
                    type: string
                  - name: value
                    type: string
              - name: extension
                type: array[json]
                description: >-
                  An extension that includes the following values:<br><br>
                  - Emergency Contact<br>
                  - Authorized for Release of Information
          - name: communication
            type: array[json]
            description: A language which may be used to communicate with the patient about his or her health.
            update_description: <code>communication.language</code> is an object that contains a coding and a text description. Currently, Canvas only supports the language being set to English. If no language is added, it will default to English. Currently, it cannot be updated.
            attributes:
              - name: language
                type: json
                description: The language which can be used to communicate with the patient about his or her health. [Common Languages](https://hl7.org/fhir/R4/valueset-languages.html) (Preferred but limited to [AllLanguages](https://hl7.org/fhir/R4/valueset-all-languages.html)).
        search_parameters:
          - name: _has:CareTeam:participant:member
            type: boolean
            description: >-
              Search for patients based on references from other resources using the FHIR reverse-chaining syntax. Currently supported for CareTeam, e.g. <code>_has:CareTeam:participant:member=Practitioner/{practitioner_id}</code>
          - name: _id
            type: string
            description: A Canvas-issued unique identifier known as the patient key. This can be found in the url of the patient's chart.
          - name: _sort
            type: string
            description: Triggers sorting of the results by a specific criteria. Supported values are **_id**, **birthdate**, **family**, and **given**. Use **-_id**, **-birthdate**, **-family**, and **-given** to sort in descending order.
          - name: active
            type: boolean
            description: By default, both active and inactive patients are returned. Use this parameter to only return active (true) or inactive (false) patients.
          - name: birthdate
            type: date
            description: The patient's birthdate
          - name: email
            type: string
            description: Patient email address
          - name: family
            type: string
            description: Last name
          - name: gender
            type: string
            description: The gender of the patient. Supported values are **male**, **female**, **other** and **unknown**.
          - name: given
            type: string
            description: First Name
          - name: identifier
            type: string
            description: >-
                The Canvas-issued MRN or a saved identifier from an external system. <br><br><b>Examples:</b><br><br>
                <code>/Patient?identifier=abc123</code> will return patients with an identifier of "abc123" issued by any system, including Canvas-issued MRNs<br><br>
                <code>/Patient?identifier=foo|abc123</code> will return patients with an identifier of "abc123" issued by the system named "foo" <br><br>
                <code>/Patient?identifier=http://canvasmedical.com|012345</code> will return the patient with the Canvas-issued MRN of "012345"<br><br>
                <code>/Patient?identifier=foo|</code> will return all patients with an identifier issued by the system named "foo"<br><br>
                <code>/Patient?identifier=|abc123</code> will return patients with an identifier of "abc123" issued by the system named "" (empty string)
          - name: name
            type: string
            description: Part of a first or last name
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: phone
            type: string
            description: Patient phone number. Expected to be 10 digits.
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: patient-create-request
          example_response: patient-create-response
          description: >-
            Upon successful creation, the Patient identifier can be found in the `Location` header of the response. The patient record in Canvas can be viewed at *https://\<instance\>.canvasmedical.com/patient/\<id\>*. <br><br> Most of the fields that are populated through this endpoint will display and be editable on the Patient profile page.
        read:
          responses: [200, 401, 403, 404]
          example_request: patient-read-request
          example_response: patient-read-response
        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: patient-update-request
          example_response: patient-update-response
          description: >-
            <b>How updates/deletions to the identifier, telecom, address, and contact fields are handled:</b><br><br> Patient Search/Read will include an <code>id</code>  value for these fields.<br><br>If the <code>id</code>  field is included in the iteration, then Canvas will attempt to match to an existing value for that field.<br><br> If the <code>id</code> field is <b>not</b> included in the iteration, then Canvas will attempt to create a new entry in the database for that field.<br><br> If a <code>telecom</code>, <code>address</code>, or <code>contact</code> iteration returned via Search/Read is <b>not</b> included in the Update message, then it will be deleted.<br><br><b>Other Fields</b><br><br>If a field is required according to Patient Create, it is also required in the update. If the field is not required and is not added to the update request, the saved data will not be changed.
        search:
          responses: [200, 400, 401, 403]
          example_request: patient-search-request
          example_response: patient-search-response
          description: >-
            Search for patient resources.
---

<div id="patient-create-request">
{% tabs patient-create-request %}
{% tab patient-create-request curl %}
```sh
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Patient' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Patient",
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
            "valueCode": "20430005"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
            "extension":
            [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier":
                    {
                        "value": "1123152",
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2131-1",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2186-5",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "I am a clinical caption from a Create message"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "I am an administrative caption from a Create message"
        }
    ],
    "identifier":
    [
        {
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990"
        }
    ],
    "active": true,
    "name":
    [
        {
            "use": "official",
            "family": "Jones",
            "given":
            [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given":
            [
                "Sammy"
            ]
        }
    ],
    "telecom":
    [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1980-11-13",
    "address":
    [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line":
            [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "photo":
    [
        {
            "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
        }
    ],
    "contact":
    [
        {
            "name":
            {
                "text": "Dan Jones"
            },
            "relationship":
            [
                {
                    "text": "Spouse"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "danjones@example.com"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": true
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ]
        },
        {
            "name":
            {
                "text": "Linda Stewart"
            },
            "relationship":
            [
                {
                    "text": "Mother"
                }
            ],
            "telecom":
            [
                {
                    "system": "phone",
                    "value": "5557327068"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ]
        },
        {
            "name":
            {
                "text": "Jimmy Stewart"
            },
            "relationship":
            [
                {
                    "text": "Father"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "j.stewart@example.com"
                }
            ]
        }
    ],
    "communication":
    [
        {
            "language":
            {
                "coding":
                [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/all-languages",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
            }
        }
    ]
}
'
```
{% endtab %}

{% tab patient-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Patient"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Patient",
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
            "valueCode": "20430005"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
            "extension":
            [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier":
                    {
                        "value": "1123152",
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2131-1",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2186-5",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "I am a clinical caption from a Create message"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "I am an administrative caption from a Create message"
        }
    ],
    "identifier":
    [
        {
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990"
        }
    ],
    "active": True,
    "name":
    [
        {
            "use": "official",
            "family": "Jones",
            "given":
            [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given":
            [
                "Sammy"
            ]
        }
    ],
    "telecom":
    [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1980-11-13",
    "address":
    [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line":
            [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "photo":
    [
        {
            "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
        }
    ],
    "contact":
    [
        {
            "name":
            {
                "text": "Dan Jones"
            },
            "relationship":
            [
                {
                    "text": "Spouse"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "danjones@example.com"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": True
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": True
                }
            ]
        },
        {
            "name":
            {
                "text": "Linda Stewart"
            },
            "relationship":
            [
                {
                    "text": "Mother"
                }
            ],
            "telecom":
            [
                {
                    "system": "phone",
                    "value": "5557327068"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": True
                }
            ]
        },
        {
            "name":
            {
                "text": "Jimmy Stewart"
            },
            "relationship":
            [
                {
                    "text": "Father"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "j.stewart@example.com"
                }
            ]
        }
    ],
    "communication":
    [
        {
            "language":
            {
                "coding":
                [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/all-languages",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
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

<div id="patient-create-response">
{% include create-response.html %}
</div>

<div id="patient-read-request">
{% include read-request.html resource_type="Patient" %}
</div>

<div id="patient-read-response">
{% tabs patient-read-response %}
{% tab patient-read-response 200 %}
```json
{
    "resourceType": "Patient",
    "id": "7162fd82487e4dc8aa2581ddbca91892",
    "text":
    {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Samantha<b>Jones</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>963277285</td></tr><tr><td>Date of birth</td><td><span>1980-11-13</span></td></tr></tbody></table></div>"
    },
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
            "valueCode": "20430005"
        },
        {
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": "2131-1",
                        "display": "Other Race"
                    }
                },
                {
                    "url": "text",
                    "valueString": "Other Race"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
        },
        {
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": "2186-5",
                        "display": "Not Hispanic or Latino"
                    }
                },
                {
                    "url": "text",
                    "valueString": "Not Hispanic or Latino"
                }
            ],
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "I am a clinical caption from a Create message"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "I am an administrative caption from a Create message"
        },
        {
            "extension":
            [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier":
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber",
                        "value": "1123152"
                    }
                },
                {
                    "url": "specialty_type",
                    "valueString": "Retail"
                },
                {
                    "url": "default",
                    "valueBoolean": false
                }
            ],
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy"
        }
    ],
    "identifier":
    [
        {
            "use": "usual",
            "type":
            {
                "coding":
                [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR"
                    }
                ]
            },
            "system": "http://canvasmedical.com",
            "value": "963277285",
            "assigner":
            {
                "display": "Canvas Medical"
            }
        },
        {
            "id": "1e628d77-5cdd-400f-a239-b24929d4a0aa",
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990",
            "period":
            {
                "start": "1970-01-01",
                "end": "2100-12-31"
            }
        }
    ],
    "active": true,
    "name":
    [
        {
            "use": "official",
            "family": "Jones",
            "given":
            [
                "Samantha",
                "Ann"
            ],
            "period":
            {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        },
        {
            "use": "nickname",
            "given":
            [
                "Sammy"
            ],
            "period":
            {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        }
    ],
    "telecom":
    [
        {
            "id": "aa0d6ad0-0b69-4740-9c8c-759c769a63d1",
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "id": "49c0c29d-c56e-41bb-89ab-79562bb75afc",
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1980-11-13",
    "deceasedBoolean": false,
    "address":
    [
        {
            "id": "611aaf01-a515-4d55-b43d-88b8735359f7",
            "use": "home",
            "type": "both",
            "line":
            [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107",
            "country": "United States"
        }
    ],
    "photo":
    [
        {
            "url": "https://canvas-client-media.s3.amazonaws.com/local/patient-avatars/20230928_213831_7162fd82487e4dc8aa2581ddbca91892.unknown_image?AWSAccessKeyId=AKIAQB7SIDR7IJXXMF47&Signature=kG1YseB%2FjSd7UMErYFVst8%2B3yHY%3D&Expires=1695938081"
        }
    ],
    "contact":
    [
        {
            "id": "1ba81cb4-7f97-429d-b0d8-4c4f067b11a5",
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": true
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ],
            "relationship":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                            "code": "EMC",
                            "display": "Emergency contact"
                        },
                        {
                            "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                            "code": "ARI",
                            "display": "Authorized for release of information"
                        }
                    ],
                    "text": "Spouse"
                }
            ],
            "name":
            {
                "text": "Dan Jones"
            },
            "telecom":
            [
                {
                    "system": "email",
                    "value": "danjones@example.com"
                }
            ]
        },
        {
            "id": "f259a2b0-6bae-479b-8efe-f9436046cfb3",
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": false
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ],
            "relationship":
            [
                {
                    "coding":
                    [
                        {
                            "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                            "code": "ARI",
                            "display": "Authorized for release of information"
                        }
                    ],
                    "text": "Mother"
                }
            ],
            "name":
            {
                "text": "Linda Stewart"
            },
            "telecom":
            [
                {
                    "system": "phone",
                    "value": "5557327068"
                }
            ]
        },
        {
            "id": "30639a10-18c2-4222-8d26-32b2ca36a1bb",
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": false
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": false
                }
            ],
            "relationship":
            [
                {
                    "text": "Father"
                }
            ],
            "name":
            {
                "text": "Jimmy Stewart"
            },
            "telecom":
            [
                {
                    "system": "email",
                    "value": "j.stewart@example.com"
                }
            ]
        }
    ],
    "communication":
    [
        {
            "language":
            {
                "coding":
                [
                    {
                        "system": "urn:ietf:bcp:47",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
            }
        }
    ]
}
```
{% endtab %}
{% tab patient-read-response 401 %}
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
{% tab patient-read-response 403 %}
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
{% tab patient-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Patient resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}
</div>

<div id="patient-update-request">
{% tabs patient-update-request %}

{% tab patient-update-request curl %}
```sh
curl --request PUT \
     --url 'https://fumage-example.canvasmedical.com/Patient/<id>' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Patient",
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
            "valueCode": "20430005"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
            "extension":
            [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier":
                    {
                        "value": "1123152",
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2131-1",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2186-5",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "Prefers to be called Sammy"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "I am an administrative caption from a Create message"
        }
    ],
    "identifier":
    [
        {
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990"
        }
    ],
    "active": true,
    "name":
    [
        {
            "use": "official",
            "family": "Jones",
            "given":
            [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given":
            [
                "Sammy"
            ]
        }
    ],
    "telecom":
    [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1980-11-13",
    "address":
    [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line":
            [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "photo":
    [
        {
            "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
        }
    ],
    "contact":
    [
        {
            "name":
            {
                "text": "Dan Jones"
            },
            "relationship":
            [
                {
                    "text": "Spouse"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "danjones@example.com"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": true
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ]
        },
        {
            "name":
            {
                "text": "Linda Stewart"
            },
            "relationship":
            [
                {
                    "text": "Mother"
                }
            ],
            "telecom":
            [
                {
                    "system": "phone",
                    "value": "5557327068"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ]
        },
        {
            "name":
            {
                "text": "Jimmy Stewart"
            },
            "relationship":
            [
                {
                    "text": "Father"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "j.stewart@example.com"
                }
            ]
        }
    ],
    "communication":
    [
        {
            "language":
            {
                "coding":
                [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/all-languages",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
            }
        }
    ]
}
'
```
{% endtab %}

{% tab patient-update-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Patient/<id>"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Patient",
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446141000124107",
                        "display": "Identifies as female gender (finding)"
                    }
                ],
                "text": "Identifies as female gender (finding)"
            }
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
            "extension":
            [
                {
                    "url": "ncpdp-id",
                    "valueIdentifier":
                    {
                        "value": "1123152",
                        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2131-1",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
            "extension":
            [
                {
                    "url": "ombCategory",
                    "valueCoding":
                    {
                        "code": "2186-5",
                        "system": "urn:oid:2.16.840.1.113883.6.238"
                    }
                }
            ]
        },
        {
            "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
            "valueCode": "America/New_York"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
            "valueString": "Prefers to be called Sammy"
        },
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
            "valueString": "I am an administrative caption from a Create message"
        }
    ],
    "identifier":
    [
        {
            "use": "usual",
            "system": "HealthCo",
            "value": "s07960990"
        }
    ],
    "active": True,
    "name":
    [
        {
            "use": "official",
            "family": "Jones",
            "given":
            [
                "Samantha",
                "Ann"
            ]
        },
        {
            "use": "nickname",
            "given":
            [
                "Sammy"
            ]
        }
    ],
    "telecom":
    [
        {
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        },
        {
            "system": "email",
            "value": "samantha.jones@example.com",
            "use": "work",
            "rank": 1
        }
    ],
    "gender": "female",
    "birthDate": "1980-11-13",
    "address":
    [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line":
            [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
        }
    ],
    "photo":
    [
        {
            "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
        }
    ],
    "contact":
    [
        {
            "name":
            {
                "text": "Dan Jones"
            },
            "relationship":
            [
                {
                    "text": "Spouse"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "danjones@example.com"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": True
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": True
                }
            ]
        },
        {
            "name":
            {
                "text": "Linda Stewart"
            },
            "relationship":
            [
                {
                    "text": "Mother"
                }
            ],
            "telecom":
            [
                {
                    "system": "phone",
                    "value": "5557327068"
                }
            ],
            "extension":
            [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": True
                }
            ]
        },
        {
            "name":
            {
                "text": "Jimmy Stewart"
            },
            "relationship":
            [
                {
                    "text": "Father"
                }
            ],
            "telecom":
            [
                {
                    "system": "email",
                    "value": "j.stewart@example.com"
                }
            ]
        }
    ],
    "communication":
    [
        {
            "language":
            {
                "coding":
                [
                    {
                        "system": "http://hl7.org/fhir/ValueSet/all-languages",
                        "code": "en",
                        "display": "English"
                    }
                ],
                "text": "English"
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

<div id="patient-update-response">
{% include update-response.html resource_type="Patient" %}
</div>

<div id="patient-search-request">
{% include search-request.html resource_type="Patient" search_string="family=Jones&gender=female" %}
</div>

<div id="patient-search-response">
{% tabs patient-search-response %}
{% tab patient-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 1,
    "link":
    [
        {
            "relation": "self",
            "url": "/Patient?family=Jones&gender=female&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Patient?family=Jones&gender=female&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Patient?family=Jones&gender=female&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Patient",
                "id": "7162fd82487e4dc8aa2581ddbca91892",
                "text":
                {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Samantha<b>Jones</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>963277285</td></tr><tr><td>Date of birth</td><td><span>1980-11-13</span></td></tr></tbody></table></div>"
                },
                "extension":
                [
                    {
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                        "valueCode": "F"
                    },
                    {
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
                        "valueCodeableConcept":
                        {
                            "coding":
                            [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "446141000124107",
                                    "display": "Identifies as female gender (finding)"
                                }
                            ],
                            "text": "Identifies as female gender (finding)"
                        }
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation",
                        "valueCode": "20430005"
                    },
                    {
                        "extension":
                        [
                            {
                                "url": "ombCategory",
                                "valueCoding":
                                {
                                    "system": "urn:oid:2.16.840.1.113883.6.238",
                                    "code": "2131-1",
                                    "display": "Other Race"
                                }
                            },
                            {
                                "url": "text",
                                "valueString": "Other Race"
                            }
                        ],
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
                    },
                    {
                        "extension":
                        [
                            {
                                "url": "ombCategory",
                                "valueCoding":
                                {
                                    "system": "urn:oid:2.16.840.1.113883.6.238",
                                    "code": "2186-5",
                                    "display": "Not Hispanic or Latino"
                                }
                            },
                            {
                                "url": "text",
                                "valueString": "Not Hispanic or Latino"
                            }
                        ],
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
                    },
                    {
                        "url": "http://hl7.org/fhir/StructureDefinition/tz-code",
                        "valueCode": "America/New_York"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
                        "valueString": "I am a clinical caption from a Create message"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
                        "valueString": "I am an administrative caption from a Create message"
                    },
                    {
                        "extension":
                        [
                            {
                                "url": "ncpdp-id",
                                "valueIdentifier":
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber",
                                    "value": "1123152"
                                }
                            },
                            {
                                "url": "specialty_type",
                                "valueString": "Retail"
                            },
                            {
                                "url": "default",
                                "valueBoolean": false
                            }
                        ],
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy"
                    }
                ],
                "identifier":
                [
                    {
                        "use": "usual",
                        "type":
                        {
                            "coding":
                            [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                    "code": "MR"
                                }
                            ]
                        },
                        "system": "http://canvasmedical.com",
                        "value": "963277285",
                        "assigner":
                        {
                            "display": "Canvas Medical"
                        }
                    },
                    {
                        "id": "1e628d77-5cdd-400f-a239-b24929d4a0aa",
                        "use": "usual",
                        "system": "HealthCo",
                        "value": "s07960990",
                        "period":
                        {
                            "start": "1970-01-01",
                            "end": "2100-12-31"
                        }
                    }
                ],
                "active": true,
                "name":
                [
                    {
                        "use": "official",
                        "family": "Jones",
                        "given":
                        [
                            "Samantha",
                            "Ann"
                        ],
                        "period":
                        {
                            "start": "0001-01-01T00:00:00+00:00",
                            "end": "9999-12-31T23:59:59.999999+00:00"
                        }
                    },
                    {
                        "use": "nickname",
                        "given":
                        [
                            "Sammy"
                        ],
                        "period":
                        {
                            "start": "0001-01-01T00:00:00+00:00",
                            "end": "9999-12-31T23:59:59.999999+00:00"
                        }
                    }
                ],
                "telecom":
                [
                    {
                        "id": "aa0d6ad0-0b69-4740-9c8c-759c769a63d1",
                        "extension":
                        [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                                "valueBoolean": false
                            }
                        ],
                        "system": "phone",
                        "value": "5554320555",
                        "use": "mobile",
                        "rank": 1
                    },
                    {
                        "id": "49c0c29d-c56e-41bb-89ab-79562bb75afc",
                        "extension":
                        [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                                "valueBoolean": false
                            }
                        ],
                        "system": "email",
                        "value": "samantha.jones@example.com",
                        "use": "work",
                        "rank": 1
                    }
                ],
                "gender": "female",
                "birthDate": "1980-11-13",
                "deceasedBoolean": false,
                "address":
                [
                    {
                        "id": "611aaf01-a515-4d55-b43d-88b8735359f7",
                        "use": "home",
                        "type": "both",
                        "line":
                        [
                            "1234 Main St."
                        ],
                        "city": "Los Angeles",
                        "state": "CA",
                        "postalCode": "94107",
                        "country": "United States"
                    }
                ],
                "contact":
                [
                    {
                        "id": "1ba81cb4-7f97-429d-b0d8-4c4f067b11a5",
                        "extension":
                        [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                                "valueBoolean": true
                            },
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                                "valueBoolean": true
                            }
                        ],
                        "relationship":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                                        "code": "EMC",
                                        "display": "Emergency contact"
                                    },
                                    {
                                        "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                                        "code": "ARI",
                                        "display": "Authorized for release of information"
                                    }
                                ],
                                "text": "Spouse"
                            }
                        ],
                        "name":
                        {
                            "text": "Dan Jones"
                        },
                        "telecom":
                        [
                            {
                                "system": "email",
                                "value": "danjones@example.com"
                            }
                        ]
                    },
                    {
                        "id": "f259a2b0-6bae-479b-8efe-f9436046cfb3",
                        "extension":
                        [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                                "valueBoolean": false
                            },
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                                "valueBoolean": true
                            }
                        ],
                        "relationship":
                        [
                            {
                                "coding":
                                [
                                    {
                                        "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                                        "code": "ARI",
                                        "display": "Authorized for release of information"
                                    }
                                ],
                                "text": "Mother"
                            }
                        ],
                        "name":
                        {
                            "text": "Linda Stewart"
                        },
                        "telecom":
                        [
                            {
                                "system": "phone",
                                "value": "5557327068"
                            }
                        ]
                    },
                    {
                        "id": "30639a10-18c2-4222-8d26-32b2ca36a1bb",
                        "extension":
                        [
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                                "valueBoolean": false
                            },
                            {
                                "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                                "valueBoolean": false
                            }
                        ],
                        "relationship":
                        [
                            {
                                "text": "Father"
                            }
                        ],
                        "name":
                        {
                            "text": "Jimmy Stewart"
                        },
                        "telecom":
                        [
                            {
                                "system": "email",
                                "value": "j.stewart@example.com"
                            }
                        ]
                    }
                ],
                "communication":
                [
                    {
                        "language":
                        {
                            "coding":
                            [
                                {
                                    "system": "urn:ietf:bcp:47",
                                    "code": "en",
                                    "display": "English"
                                }
                            ],
                            "text": "English"
                        }
                    }
                ]
            }
        }
    ]
}
```
{% endtab %}
{% tab patient-search-response 400 %}
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
{% tab patient-search-response 401 %}
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
{% tab patient-search-response 403 %}
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
