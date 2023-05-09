---
title: "Patient Create"
slug: "patient-create"
excerpt: "Create a patient"
hidden: false
createdAt: "2022-06-07T19:05:24.029Z"
updatedAt: "2023-04-10T15:28:13.144Z"
---
# Getting the newly-created patient's ID.

Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this patient. 

This ID will also match the url when navigated to the patient chart.  
https\://<instance>.canvasmedical.com/patient/<patient-id>

Most of the fields that are populated through this endpoint will display and be editable on the Patient Registration page. You can navigate to this view when you click the Patient's name in the top left corner on their patient chart or if you click the three dot menu next to the patient name and click `Registration`

# Patient Attributes:

Canvas accepts a FHIR standard request body, you may refer to [FHIR Patient Documentation](https://www.hl7.org/fhir/patient.html) to help out in building your patient request. Below is our documentation on how Canvas specifically will use each attribute

## name [REQUIRED]

Name is a **required** list of objects. 

One iteration must be marked with `"use": "official"`. The first object with use=official will determine the Patient's first, last, prefix, suffix or middle name. The First and Last name is required within Canvas.  
If you look at the example: 

- the `family` attribute will populate the Patient's Last Name
- the `given` list will populate the Patient's First/Middle Name.  The first item in the list will be the First Name,  while if more items in the list exists, it will populate the Patient's Middle Name and be joined together with an empty space.
- the `prefix` attribute will be stored within Canvas's database but will not be displayed in the Canvas UI. 
- the `suffix` attribute will be displayed on the Canvas UI but it will not be editable through the UI.

This example also demonstrates that Canvas ingests a Nick Name (preferred name) for the Patient. This element is identified by `use` = `nickname` and the first item in the `given` list will be the Patient's nickname. 

Canvas can also ingest old names or maiden names using `use` = `maiden` or `use`= `old`. These will not show up on the Canvas UI but will be stored by Canvas (and will be returned via a read request).

```curl
"name": [
        {
            "use": "official",
            "family": "Mark",
            "given": [
                "Isabella",
                "Robel"
            ],
            "prefix": "Mrs.",
            "suffix": "Jr."
        },
        {
            "use": "nickname",
            "given": [
                "Izzy"
            ]
        },
        {
            "use": "maiden",
            "family": "Smith"
        }
    ]
```



In the Canvas UI, each Patient will be displayed with `First Last Suffix (Nick name)`. You will be able to search for a patient by any of these attributes defined here: First, Middle, Last, Suffix or Nick Name.

If there are any other objects defined in the name list they will currently be ignored in Canvas. 

## birthDate [REQUIRED]

The birthDate field is required in Canvas for a patient. This is a string date format that is defined [here](https://www.hl7.org/fhir/datatypes.html#date). For Canvas it is best to get the format `YYYY-MM-DD`.

If only a month and year is given, the birthdate is set to the 1st of the given month by default. If only a year is given, the birthdate defaults to January 1st of that year. To summarize, Canvas accepts the following formats: YYYY, YYYY-MM, and YYYY-MM-DD.

```curl
"birthDate": "1980-11-13",
```



## extension

Canvas allows a few specific FHIR extensions to be ingested. For us to identify which extension maps to specific fields in Canvas, we use the `url` field as an exact string match. Here are the following extensions we support in Canvas:

### Birthsex Extension [REQUIRED]

There is one extensions that is **required** and that is the Patient's sex at birth. We identify this extension with the `url` equal to `http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex`. The values allowed in the `valueCode` attribute is 

- M   (for Male)
- F    (for Female)
- O    (for Other) 
- UNK  (for Unknown)

```text
{
  "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
  "valueCode": "M"
}
```



### Ethnicity Extension

There is an extension to specify the ethnicities of a patient. [Us Core Ethnicity extension](http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity). 

- The `url` must match "<http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity>"
- Then you will define an `extension` list of objects where each object needs a `valueCoding` object. The `system` of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate `code` of each ethnicity needed from the ValueSet.

```text
{
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
      "extension": [
        {
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2186-5"
        	}
        },
        {
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2180-8"
        	}  
        }
      ]
    },
```



### Race Extension

There is an extension to specify the races of a patient. This is defined using the [Us Core Race extension](http://hl7.org/fhir/us/core/StructureDefinition/us-core-race). 

- The `url` must match "<http://hl7.org/fhir/us/core/StructureDefinition/us-core-race>"
- Then you will define an `extension` list of objects where each object needs a `valueCoding` object. The `system` of each valueCoding will equal "urn:oid:2.16.840.1.113883.6.238". Then you can specify the appropriate `code` of each race needed from the ValueSet. 

```text
{
      "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
      "extension": [
        {
          "valueCoding": {
            "system": "urn:oid:2.16.840.1.113883.6.238",
            "code": "2110-5"
          }  
        }
      ]
    },
```



### Timezone Extension

An optional extension Canvas accepts is to specify the timezone a Patient live in. The extension must have the `url` equal to "<http://hl7.org/fhir/StructureDefinition/tz-code">. Then the `valueCode` field can be anything defined [here](http://hl7.org/fhir/StructureDefinition/tz-code). You can see examples [here](http://build.fhir.org/valueset-timezones.html). If the URL does not match exactly, a timezone will not be set. If the URL matches exactly but a valid timezone is not given, the database will save what is passed in; however, the UI will display the current user's timezone. 

```text
{
	"url": "http://hl7.org/fhir/StructureDefinition/tz-code",
	"valueCode": "America/New_York"
},
```



### Clinical Note Extension

An optional extension Canvas accepts is to define a Clinical Note. This note will display on the Patient's Chart right under the patient's name. 

The `url` must equal "<http://schemas.canvasmedical.com/fhir/extensions/clinical-note">, while the `valueString` is a free text field.

```text
{
	"url": "http://schemas.canvasmedical.com/fhir/extensions/clinical-note",
	"valueString": "I am a clinical caption from a Create message"
},
```



### Administrative Note Extension

An optional extension Canvas accepts is to define a Adminstrative Note. To learn more about this attribute, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360056388234-Administrative-Caption).

The `url` must equal "<http://schemas.canvasmedical.com/fhir/extensions/administrative-note">, while the `valueString` is a free text field.

```text
{
	"url": "http://schemas.canvasmedical.com/fhir/extensions/administrative-note",
	"valueString": "I am an administrative caption from a Create message"
}
```



### Preferred Pharmacy Extension

This extension is used to set a patient's preferred pharmacy using the NCPDP id. This is one of the many preferences you can set on a patient that is documented in this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339654-Patient-Preferences)

The extension contains the following attributes:

- The `url` must match `http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy`.
- The `extension` list of objects where each object needs:
  - `url` that must match `ncpdp-id`
  - `valueIdentifier` object that contains the `system` that must equal  
     "<http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber">. Then you can specify the  
     appropriate `value` of the pharmacy, which is a 7 digit NDPDP ID.

```text
{
  "url" : "http://schemas.canvasmedical.com/fhir/extensions/preferred-pharmacy",
  "extension": [
    {
      "url": "ncpdp-id",
      "valueIdentifier": {
        "value": "5670496",
        "system": "http://terminology.hl7.org/CodeSystem/NCPDPProviderIdentificationNumber"
      }
    }
  ]
}
```



Here are a few callouts on workflow for the value attribute:

1. If a valid 7 digit NCPDP id value is specified, then the patient's preferred pharmacy will be updated accordingly with the pharmacy's name, phone, fax and address.
2. If there is any other value given that is not a 7 digit number, you will see an error that they message did not adhere to the Patient Schema. 
3. If a 7 digit number is passed, but it is not a valid NCPDP id and does not correlate to a pharmacy in Canvas, the patient's preferred pharmacy will be blank. 
4. If this extension is not specified in the request body, any current preferred pharmacy set for the patient will remain. 

## gender

The gender attribute is an optional string enum value that feds into our gender identity attribute on our UI. Currently we are tied to the FHIR values allowed: 

- male
- female
- other
- unknown

If `unknown` is entered at the time of creation, the patient chart will show gender as 'choose not to disclose'. If `other` is selected, the patient chart will display 'Additional gender category or other, please specify' in the gender field. 

On the Canvas UI we do allow more options than the just the FHIR standards. 

```text
"gender": "female",
```



## active

The active attribute is a boolean to specify if the patient is active in your healthcare system. If this value is not set, Canvas will default this to `true`

```text
"active": true,
```



## telecom

Telecom is an optional list of objects where you can provide the following attributes in each object: 

- `system` : This can be phone, fax, email, pager, url, sms, or other (This will default to other if you try to pass anything else). 
- `value` [REQUIRED]\: Free text string of the actual value for this contact point
- `use`: This can be home, work, temp, old, mobile  (default is home)
- `rank`: This is an integer to specified the preferred order of contact points per system (default is 1)
- `extension` : This is an optional object that you can specify for a Patient's phone number or email. This tells Canvas that we have the Patient's consent to send text messages or emails to this number. We identify this extension with the `url` equal to "<http://schemas.canvasmedical.com/fhir/extensions/has-consent>" and then you can specify a boolean for the `valueBoolean` attribute. **Note: This will not send the verification email or text as our UI does. It will bypass this step and mark the contact as verified**

Email and Phone system's will be surfaced in the Canvas UI. Currently we do store the other systems in our database, we just do not display them. 

```text
"telecom": [
        {
            "id": "46c850f4-bf87-47fe-88d1-1eb9883ab095",
            "system": "other",
            "value": "other test",
            "use": "home",
            "rank": 1
        },
        {
            "id": "5e610aac-4627-40b5-bff0-892a7040a0a4",
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/has-consent",
                    "valueBoolean": false
                }
            ],
            "system": "phone",
            "value": "5554320555",
            "use": "mobile",
            "rank": 1
        }
    ],
```



## identifier

The identifier list defines additional identifiers you may want to store for a patient. None of these identifiers will be surfaced on the Patient's chart but may help you to identify the patient in your internal system. For each identifier object you can specify the following attributes:

- `use`:  This could be usual, official, temp, secondary, old (This will default to usual if omitted)
- `system`:  Free text field to help you identify what this value represents
- `value`: Free text to store the patient's identifier
- `period`: This is used to specify the start and end dates (format YYYY-MM-DD). If period is omitted it will default to `start` = 1970-01-01 and `end` = 2100-12-31. There is currently no validation if the end date is before the start date.

```text
"identifier": [
        {
            "use": "usual",
            "system": "HealthCo Internal Identifer",
            "value": "s07960990",
            "period": {
                "start": "1980-03-01",
                "end": "2051-12-31"
            }
        }
]
```



## address

The address is a list of objects. For each address we allow the following attributes:

- `use`: choices allowed are home, work, temp, old (default is home)
- `type`: choices allowed are both, physical, postal (default is both)
- `line`: List of strings. The first item in the list will be address line 1 in Canvas. The rest of the items in the list will be concatenated to be the address line 2
- 'city': String representing the city of the address
- `state`: This should be the 2 letter abbreviation for the state of the address
- `postalCode`: This should be the 5 digit postal code of the address

```text
"address": [
        {
            "use": "home",
            "type": "both",
            "line": [
                "4247 Murry Street"
            ],
            "city": "Chesapeake",
            "state": "VA",
            "postalCode": "23322"
        }
    ],
```



## photo

The photo attribute is where you can define a [base64binary](https://www.hl7.org/fhir/datatypes.html#base64Binary) string representing the image you want to upload for the patient avatar on the Canvas UI. The example below binary represents a rubber duck. 

```text
"photo": [
    {
      "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
    }
  ],
```



## deceased

This is an optional boolean that defaults to false. This variable is not displayed in the Canvas UI but is stored by Canvas.

```text
"deceased": false,
```



## contact

The contact attribute is a list of contact objects. They specify a contact party for the patient (friend, parent, emergency contact). The will display on the Patient Registration page. 

The following attributes are allowed for each contact object:

- `name` [REQUIRED]\:  This is an object where you can specify the `text` that stores the contact's name. 
- `relationship`: This is a list of objects where you can specify the `text` that stores the contact's relationship. It is a free text field. While a list, we currently only store and display the first object's text
- `telecom`: This is a list of objects where Canvas will take the first `system` equal to `phone` and store as the contact's phone number. Then the first `system` equal to `email` will be stored as this contact's email address. The value of the email or phone number is stored in the `value` field. If any other option is passed in the system field, the data will not be stored. 
- `extension`: Optional extensions are allowed in Canvas to specify a few additional information about a patient's contact.  
  If you want to specify if this contact is  "authorized for release of information" or not we want to pass in an extensions with a `url` equal to "<http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information>" and pass a boolean to the `valueBoolean` field.  
  If you want to specify if this contact is the patient's "emergency contact" or not we want to pass in an extension with a `url` equal to "<http://schemas.canvasmedical.com/fhir/extensions/emergency-contact>" and pass a boolean to the `valueBoolean` field. 

```text
"contact": [
        {
            "name": {
                "text": "Nick Smith"
            },
            "relationship": [
                {
                    "text": "Spouse"
                }
            ],
            "telecom": [
                {
                    "system": "email",
                    "value": "test@me.com"
                }
            ],
            "extension": [
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/emergency-contact",
                    "valueBoolean": true
                },
                {
                    "url": "http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information",
                    "valueBoolean": true
                }
            ]
        }
]
```