---
title: Patient
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Patient
        article: "a"
        description: >-
           Demographics and other administrative information about an individual or animal receiving care or other health-related services.<br><br> Canvas supports specific FHIR extensions on this resource. In order to identify which extension maps to specific fields in Canvas, the url field is used as an exact string match.<br><br>[http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-patient.html](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-patient.html)
        attributes:
          - name: id
            type: string
            description: Unique Canvas identifier for this resource
          - name: text
            type: json
            description: A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource.
          - name: extension
            type: array[json]
            description: Reference the **extension-\*** fields below to see the possible extensions contained in this resource.
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
                Telecom is an optional list of objects where you can provide the child  attributes listed below. Email and Phone system's will be surfaced in the Canvas UI. Currently we do store the other systems in our database, we just do not display them.
            update_description:
                Telecom is an optional list of objects where you can provide the child  attributes listed below. Email and Phone system's will be surfaced in the Canvas UI. Currently we do store the other systems in our database, we just do not display them.
            attributes:
              - name: id
                type: string
              - name: extension
                type: array
                description: >-
                    This is an optional object that you can specify for a Patient's phone number or email. This tells Canvas that we have the patient's consent to send text messages or emails to this number. This extension is identified with the <code>url</code> [http://schemas.canvasmedical.com/fhir/extensions/has-consent](http://schemas.canvasmedical.com/fhir/extensions/has-consent). A boolean value can be specified in the <code>valueBoolean</code> attribute. <b>Note: This will not send a verification email or text as is the Canvas UI does. It will bypass this step and mark the contact as verified.</b>
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
                The gender attribute is an optional string enum value that maps to our gender identity attribute on our UI. Currently we are tied to the FHIR values allowed: male, female, other, and unknown. <br><br> If <code>unknown</code> is entered at the time of creation, the patient chart will show gender as 'choose not to disclose'. If <code>other</code> is selected, the patient chart will display `Additional gender category or other, please specify` in the gender field.
            update_description: >-
                The gender attribute is an optional string enum value that maps to our gender identity attribute on our UI. Currently we are tied to the FHIR values allowed: male, female, other, and unknown. <br><br> If <code>unknown</code> is entered at the time of creation, the patient chart will show gender as 'choose not to disclose'. If <code>other</code> is selected, the patient chart will display `Additional gender category or other, please specify` in the gender field.
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
            type: json
            description: Image of the patient. Data should be passed as a base64-encoded string. This image shows on the patient avatar in the Canvas UI.
            attributes:
              - name: url
                type: string
          - name: contact
            type: array[json]
            required: false
            description: A contact party (e.g. guardian, partner, friend) for the patient. Contact details will display on the Patient Registration page in the Canvas UI.
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
                type: json
                description: This is a list of objects where you can specify the text that stores the contact's relationship. It is a free text field. While a list, we currently only store and display the first object's text.
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
          - name: extension - birthsex
            type: json
            required: true
            description: >-
                A code classifying the person’s sex assigned at birth as specified by the Office of the National Coordinator for Health IT (ONC). This extension aligns with the C-CDA Birth Sex Observation (LOINC 76689-9). After version 6.0.0, this extension is no longer a USCDI Requirement. Supported Values are:<br><br>
                - M - Male<br>
                - F - Female<br>
                - O - Other<br>
                - UNK - Unknown<br><br>
                [http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex](http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex)
          - name: extension - genderIdentity
            type: json
            description: >-
              This extension represents an individual’s sense of being a man, woman, boy, girl, nonbinary, or something else, ascertained by asking them what that identity is. Systems requiring multiple gender identities and associated dates SHOULD use the FHIR R5 [http://hl7.org/fhir/extensions/StructureDefinition-individual-genderIdentity.html](genderIdentity) extension. When future versions of US Core are based on FHIR R5, the FHIR R5 extension will supersede this extension.<br><br>The following value codes are supported:<br><br>
              - 446151000124109 - Identifies as Male<br>
              - 446141000124107 - Identifies as Female<br>
              - 407377005 - Female-to-Male (FTM)/Transgender Male/Trans Man<br>
              - 407376001 - Male-to-Female (MTF)/Transgender Female/Trans Woman<br>
              - 446131000124102 - Genderqueer, neither exclusively male nor female<br>
              - OTH - Additional gender category or other, please specify<br>
              - ASKU - Choose not to disclose
          - name: extension - sexual-orientation
            type: json
            description: >-
              Sexual orientation of the patient. The following value codes are supported:<br><br>
              - 20430005 - Straight or heterosexual<br>
              - 38628009 - Lesbian, gay or homosexual<br>
              - 42035005 - Bisexual<br>
              - OTH - Something else, please describe<br>
              - UNK - Don't Know<br>
              - ASKU - Choose not to disclose
          - name: extension - race
            type: codeable concept
            description: An extension to specify the races of a patient. This is defined using the Us Core Race extension [http://hl7.org/fhir/us/core/StructureDefinition/us-core-race](http://hl7.org/fhir/us/core/StructureDefinition/us-core-race)
            create_description: The url must match "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race" Then you will define an extension list of objects where each object needs a valueCoding object. The system of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate code of each race needed from the ValueSet.
            update_description: The url must match "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race" Then you will define an extension list of objects where each object needs a valueCoding object. The system of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate code of each race needed from the ValueSet.
          - name: extension - ethnicity
            type: json
            description: >-
              An extension to specify the ethnicities of a patient - [http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity](http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity)
            create_description:
                The url must match "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity" Then you will define an extension list of objects where each object needs a valueCoding object. The system of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate code of each ethnicity needed from the ValueSet.
            update_description:
                The url must match "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity" Then you will define an extension list of objects where each object needs a valueCoding object. The system of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate code of each ethnicity needed from the ValueSet.
          - name: extension - timezone
            type: json
            description:
                The timezone a patient lives in.
            create_description:
                An optional extension Canvas accepts is to specify the timezone a Patient lives in. The extension must have the url equal to "http://hl7.org/fhir/StructureDefinition/tz-code". Then the valueCode field can be anything defined here. You can see examples here. If the URL does not match exactly, a timezone will not be set. If the URL matches exactly but a valid timezone is not given, the database will save what is passed in; however, the UI will display the current user's timezone.
            update_description:
               An optional extension Canvas accepts is to specify the timezone a Patient lives in. The extension must have the url equal to "http://hl7.org/fhir/StructureDefinition/tz-code". Then the valueCode field can be anything defined here. You can see examples here. If the URL does not match exactly, a timezone will not be set. If the URL matches exactly but a valid timezone is not given, the database will save what is passed in; however, the UI will display the current user's timezone.
          - name: extension - clinical-note
            type: json
            description: This note displays under the patient's name in the clinical chart.
            create_description: This note displays under the patient's name in the clinical chart. The `url` must equal "http://schemas.canvasmedical.com/fhir/extensions/clinical-note", while the `valueString` is a free text field.
            update_description: This note displays under the patient's name in the clinical chart. The `url` must equal "http://schemas.canvasmedical.com/fhir/extensions/clinical-note", while the `valueString` is a free text field.
          - name: extension - administrative-note
            type: json
            description: This note displays under the patient's name in the administrative profile.
            create_description: This note displays under the patient's name in the administrative profile. The `url` must equal "http://schemas.canvasmedical.com/fhir/extensions/administrative-note", while the `valueString` is a free text field.
          - name: extension - preferred-pharmacy
            type: json
            description: A patient can have multiple preferred pharmacies added to their profile.
            create_description: >-
                The url must match http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy. The extension list of objects where each object needs: url that must match ncpdp-id valueIdentifier object that contains the system that must equal "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber". Then you can specify the appropriate value of the pharmacy, which is a 7 digit NDPDP ID. Here are a few callouts on workflow for the value attribute: <br><br>**1.** If a valid 7 digit NCPDP id value is specified, then the patient's preferred pharmacy will be updated accordingly with the pharmacy's name, phone, fax and address.<br>**2.** If there is any other value given that is not a 7 digit number, you will see an error that they message did not adhere to the Patient Schema.<br>**3.** If a 7 digit number is passed, but it is not a valid NCPDP id and does not correlate to a pharmacy in Canvas, the patient's preferred pharmacy will be blank.<br>**4.** If this extension is not specified in the request body, any current preferred pharmacy set for the patient will remain.
            update_description: >-
                The url must match http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy. The extension list of objects where each object needs: url that must match ncpdp-id valueIdentifier object that contains the system that must equal "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber". Then you can specify the appropriate value of the pharmacy, which is a 7 digit NDPDP ID. Here are a few callouts on workflow for the value attribute: <br><br>**1.** If a valid 7 digit NCPDP id value is specified, then the patient's preferred pharmacy will be updated accordingly with the pharmacy's name, phone, fax and address.<br>**2.** If there is any other value given that is not a 7 digit number, you will see an error that they message did not adhere to the Patient Schema.<br>**3.** If a 7 digit number is passed, but it is not a valid NCPDP id and does not correlate to a pharmacy in Canvas, the patient's preferred pharmacy will be blank.<br>**4.** If this extension is not specified in the request body, any current preferred pharmacy set for the patient will remain.
          - name: extension - business-line
            type: json
            description: >-
                The business line that the patient belongs to.
        search_parameters:
          - name: _id
            type: string
            description: >-
                A Canvas-issued unique identifier known as the patient key. This can be found in the url of the patient's chart.
          - name: identifier
            type: string
            description: >-
                The Canvas-issued MRN or a saved identifier from an external system. <br><br><b>Examples:</b><br><br>
                <code>/Patient?identifier=abc123</code> will return patients with an identifier of “abc123” issued by any system, including Canvas-issued MRNs<br><br>
                <code>/Patient?identifier=foo|abc123</code> will return patients with an identifier of “abc123" issued by the system named “foo” <br><br>
                <code>/Patient?identifier=http://canvasmedical.com|012345</code> will return the patient with the Canvas-issued MRN of “012345"<br><br>
                <code>/Patient?identifier=foo|</code> will return all patients with an identifier issued by the system named “foo”<br><br>
                <code>/Patient?identifier=|abc123</code> will return patients with an identifier of “abc123" issued by the system named “” (empty string)
          - name: name
            type: string
            description: Part of a first or last name
          - name: birthdate
            type: date
            description: The patient's birthdate
          - name: gender
            type: string
            description: The gender of the patient. Supported values are **male**, **female**, **other** and **unknown**.
          - name: family
            type: string
            description: Last name
          - name: given
            type: string
            description: First Name
          - name: email
            type: string
            description: Patient email address
          - name: nickname
            type: string
            description: Preferred or alternate name
          - name: phone
            type: string
            description: Patient phone number. Expected to be 10 digits.
          - name: active
            type: boolean
            description: By default, both active and inactive patients are returned. Use this parameter to only return active (true) or inactive (false) patients.
          - name: _has:CareTeam:participant:member
            type: boolean
            description: Search for patients based on references from other resources using the FHIR reverse-chaining syntax. Currently supported for CareTeam, e.g. <code>_has:CareTeam:participant:member=Practitioner/{practitioner_id}</code>
          - name: _sort
            type: string
            description: Triggers sorting of the results by a specific criteria. Accepted values are **id**, **birthdate**, **family** and **given**. Use **-id**, **-birthdate**, **-family** and **-given** to sort in descending order.
        endpoints: [create, read, update, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: patient-create-request
          example_response: patient-create-response
          description: >-
            Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this patient.<br><br> This ID will also match the url when navigated to the patient chart. https://.canvasmedical.com/patient/<br><br> Most of the fields that are populated through this endpoint will display and be editable on the Patient Registration page. You can navigate to this view when you click the Patient's name in the top left corner on their patient chart or if you click the three dot menu next to the patient name and click `Registration`.
        read:
          responses: [200, 401, 403, 404]
          example_request: patient-read-request
          example_response: patient-read-response
        update:
          responses: [200, 400, 401, 403, 404, 405, 412, 422]
          example_request: patient-update-request
          example_response: patient-update-response
          description: >-
            <b>How updates/deletions to the identifier, telecom, address, and contact fields are handled:</b><br><br> Patient Search/Read will include an <code>id</code>  value for these fields.<br><br>If the <code>id</code>  field is included in the iteration, then we will attempt to match to an existing value for that field.<br><br> If the <code>id</code> field is <b>not</b> included in the iteration, then we will attempt to create a new entry in the database for that field.<br><br> If a <code>telecom</code>, <code>address</code>, or <code>contact</code> iteration returned via Search/Read is <b>not</b> included in the Update message, then it will be deleted.<br><br><b>Other Fields</b><br><br>If a field is required according to Patient Create, it is also required in the update. If the field is not required and is not added to the update request, the saved data will not be changed.
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
        }
    ],
    "birthDate": "1980-11-13",
    "gender": "female",
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        }
    ],
    "address": [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line": [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
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
        }
    ],
    "birthDate": "1980-11-13",
    "gender": "female",
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        }
    ],
    "address": [
        {
            "use": "home",
            "type": "both",
            "text": "1234 Main St., Los Angeles, CA 94107",
            "line": [
                "1234 Main St."
            ],
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "94107"
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
    "id": "57db0d48fd834be4a2ad068c553e6fbb",
    "text":
    {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Mark<b>Williams</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>644854429</td></tr><tr><td>Date of birth</td><td><span>1980-11-13</span></td></tr></tbody></table></div>"
    },
    "extension":
    [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "M"
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
            "valueCodeableConcept":
            {
                "coding":
                [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "446151000124109",
                        "display": "Identifies as male gender (finding)"
                    }
                ],
                "text": "Identifies as male gender (finding)"
            }
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
            "value": "644854429",
            "assigner":
            {
                "display": "Canvas Medical"
            }
        }
    ],
    "active": true,
    "name":
    [
        {
            "use": "official",
            "family": "Williams",
            "given":
            [
                "Mark",
                "John"
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
                "Marko"
            ],
            "period":
            {
                "start": "0001-01-01T00:00:00+00:00",
                "end": "9999-12-31T23:59:59.999999+00:00"
            }
        }
    ],
    "gender": "male",
    "birthDate": "1980-11-13",
    "deceasedBoolean": false,
    "address":
    [
        {
            "id": "322caf77-2609-4257-b3dc-faa437e877c4",
            "use": "home",
            "type": "both",
            "line":
            [
                "789 Front St."
            ],
            "city": "Denver",
            "state": "CO",
            "postalCode": "80014",
            "country": "us"
        }
    ],
    "photo":
    [
        {
            "url": "https://canvas-client-media.s3.amazonaws.com/local/patient-avatars/20230926_195900_57db0d48fd834be4a2ad068c553e6fbb.unknown_image?AWSAccessKeyId=AKIAQB7SIDR7IJXXMF47&Signature=%2BIg4FlLrYym31y6vTgit%2FXC49pE%3D&Expires=1695769441"
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
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
      "valueCode": "M"
    },
    {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
        "extension": [
            {
                "url": "ombCategory",
                "valueCoding": {
                    "code": "2186-5",
                    "system": "urn:oid:2.16.840.1.113883.6.238"
                }
            }
        ]
    },
    {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
        "extension": [
            {
                "url": "ombCategory",
                "valueCoding": {
                    "code": "2131-1",
                    "system": "urn:oid:2.16.840.1.113883.6.238"
                }
            }
        ]
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
      "extension": [
        {
          "url": "ncpdp-id",
          "valueIdentifier": {
            "value": "1123152",
            "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
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
  "name": [
    {
      "use": "official",
      "family": "Williams",
      "given": [
        "Mark",
        "John"
      ]
    },
    {
      "use": "nickname",
      "given": [
        "Nick Name"
      ]
    }
  ],
  "birthDate": "1980-11-13",
  "gender": "male",
  "address": [
      {
          "use": "home",
          "type": "both",
          "text": "1234 Main St., Los Angeles, CA 94107",
          "line": [
              "1234 Main St."
          ],
          "city": "Los Angeles",
          "state": "CA",
          "postalCode": "94107"
      }
  ],
  "photo": [
    {
      "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
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
  "extension": [
    {
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
      "valueCode": "M"
    },
    {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
        "extension": [
            {
                "url": "ombCategory",
                "valueCoding": {
                    "code": "2186-5",
                    "system": "urn:oid:2.16.840.1.113883.6.238"
                }
            }
        ]
    },
    {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
        "extension": [
            {
                "url": "ombCategory",
                "valueCoding": {
                    "code": "2131-1",
                    "system": "urn:oid:2.16.840.1.113883.6.238"
                }
            }
        ]
    },
    {
      "url": "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
      "extension": [
        {
          "url": "ncpdp-id",
          "valueIdentifier": {
            "value": "1123152",
            "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
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
  "name": [
    {
      "use": "official",
      "family": "Williams",
      "given": [
        "Mark",
        "John"
      ]
    },
    {
      "use": "nickname",
      "given": [
        "Nick Name"
      ]
    }
  ],
  "birthDate": "1980-11-13",
  "gender": "male",
  "address": [
      {
          "use": "home",
          "type": "both",
          "text": "1234 Main St., Los Angeles, CA 94107",
          "line": [
              "1234 Main St."
          ],
          "city": "Los Angeles",
          "state": "CA",
          "postalCode": "94107"
      }
  ],
  "photo": [
    {
      "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
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
{% include search-request.html resource_type="Patient" search_string="family=Williams&gender=male" %}
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
            "url": "/Patient?family=Williams&gender=male&_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Patient?family=Williams&gender=male&_count=10&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Patient?family=Williams&gender=male&_count=10&_offset=0"
        }
    ],
    "entry":
    [
        {
            "resource":
            {
                "resourceType": "Patient",
                "id": "57db0d48fd834be4a2ad068c553e6fbb",
                "text":
                {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Mark<b>Williams</b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>644854429</td></tr><tr><td>Date of birth</td><td><span>1980-11-13</span></td></tr></tbody></table></div>"
                },
                "extension":
                [
                    {
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                        "valueCode": "M"
                    },
                    {
                        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity",
                        "valueCodeableConcept":
                        {
                            "coding":
                            [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "446151000124109",
                                    "display": "Identifies as male gender (finding)"
                                }
                            ],
                            "text": "Identifies as male gender (finding)"
                        }
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
                        "value": "644854429",
                        "assigner":
                        {
                            "display": "Canvas Medical"
                        }
                    }
                ],
                "active": true,
                "name":
                [
                    {
                        "use": "official",
                        "family": "Williams",
                        "given":
                        [
                            "Mark",
                            "John"
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
                            "Marko"
                        ],
                        "period":
                        {
                            "start": "0001-01-01T00:00:00+00:00",
                            "end": "9999-12-31T23:59:59.999999+00:00"
                        }
                    }
                ],
                "gender": "male",
                "birthDate": "1980-11-13",
                "deceasedBoolean": false,
                "address":
                [
                    {
                        "id": "322caf77-2609-4257-b3dc-faa437e877c4",
                        "use": "home",
                        "type": "both",
                        "line":
                        [
                            "789 Front St."
                        ],
                        "city": "Denver",
                        "state": "CO",
                        "postalCode": "80014",
                        "country": "us"
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
