---
title: Observation
sections:
  - type: section
    blocks:
      - type: apidoc
        name: Observation
        article: "a"
        description: >-
          Measurements and simple assertions made about a patient, device or other subject.<br><br>
          Canvas supports the following US Core Profiles for Observations:<br>
            - [US Core Laboratory Result Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-observation-lab.html)
            - [US Core Pediatric BMI for Age Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-pediatric-bmi-for-age.html)
            - [US Core Pediatric Head Occipital-frontal Circumference Percentile Profile](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-head-occipital-frontal-circumference-percentile.html)
            - [US Core Pediatric Weight for Height Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-pediatric-weight-for-height.html)
            - [US Core Smoking Status Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-smokingstatus.html)
            - [US Core Pulse Oximetry Profile](http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-pulse-oximetry.html)<br>

          The following USCDI data elements are retrievable from this endpoint:<br>
            - Laboratory Tests
            - Laboratory Values/Results
            - Smoking Status
        attributes:
          - name: resourceType
            description: The FHIR Resource name.
            type: string
          - name: id
            type: string
            exclude_in: create
            description: The Canvas identifier of the observation
          - name: status
            required_in: create
            type: enum [ final | unknown | entered-in-error ]
            description: The status of the result value. 
            create_description: The status of the result value. In Canvas only `final` committed vitals can be created.
            required_in: create
          - name: category
            type: array[json]
            exclude_in: create
            description: Classifies the general type of observation being made.
            attributes: 
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://terminology.hl7.org/CodeSystem/observation-category
                  - name: code
                    description: The code of the observation.
                    type: string
                    enum_options: 
                      - value: vital-signs
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Vital Signs
          - name: code
            type: json
            description: Describes what was observed.
            create_description: >-
              Describes what was observed.<br><br>
              For create interactions, only vital sign LOINC codes are supported.  
            required_in: create
            attributes: 
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                required_in: create
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    type: string
                    required_in: create
                    enum_options:
                      - value: http://loinc.org
                  - name: code
                    description: The code of the observation.
                    type: string
                    required_in: create
                    enum_options: 
                      - value: 85353-1 (panel)
                      - value: 85354-9 (blood pressure)
                      - value: 29463-7 (weight)
                      - value: 8302-2 (height)
                      - value: 8867-4 (pulse rate)
                      - value: 8310-5 (body temperature)
                      - value: 2708-6 (oxygen saturation arterial)
                      - value: 59408-5 (oxygen saturation)
                      - value: 9279-1 (respiration rate)
                      - value: 56086-2 (waist circumference)
                      - value: 80339-5 (note)
                      - value: 8884-9 (pulse rhythm)
                  - name: display
                    description: The display name of the coding.
                    type: string
                    required_in: create
          - name: subject
            type: json
            description: Canvas Patient reference the Observation is for.
            required_in: create
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the subject in the format of `"Patient/a39cafb9d1b445be95a2e2548e12a787"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Patient").
          - name: effectiveDateTime
            type: datetime
            description: Clinically relevant time/time-period for observation.
            create_description: >-
              Clinically relevant time/time-period for observation.<br><br>
              For an individual vital sign, if the effectiveDateTime differs from the panel time, it will be reflected in a read/search; however, you will not see the individual date in the UI, only the panel's datetime.<br><br>
              If omitted from create, Canvas will save a default value of the current datetime.
          - name: issued
            type: datetime
            exclude_in: create
            description: Date/Time this version was made available. It is the timestamp in Canvas when the vital record was ingested.
          - name: valueQuantity
            exclude_in: read, search
            type: json
            description: Actual result.
            create_description:
              Actual result.<br><br>

              This is used for vital observation that correspond with a numeric value. If this field is not provided or specifically the value attribute in the json is omitted, Canvas will interpret that as an empty value. A Read/Search of this observation will display the `dataAbsentReason` attribute. <br><br>

              Currently supported numeric values are<br><br>
                  -  height<br>
                  -  weight<br>
                  -  waist circumference<br>
                  -  body temperature<br>
                  -  pulse rate<br>
                  -  oxygen saturation<br>
                  -  respiration rate
            attributes:
              - name: value
                type: number
                description: Numerical value (with implicit precision).
              - name: unit
                type: string
                create_description: Unit representation. If omitted, it will default to the values in the table defined above. For the submitted `code`, only units from the table above can be sent. Sending a different unit will result in a 422 error.
          - name: valueString
            type: string
            exclude_in: read, search
            create_description:
              Actual result.<br><br>

              This is used for vital observation that correspond with a string value. If this field is not provided or specifically the value attribute in the json is omitted, Canvas will interpret that as an empty value. A Read/Search of this observation will display the `dataAbsentReason` attribute. <br><br>

              Currently supported string values are <br>
              - **note** - this is a free text comment field in the Canvas Vital Command <br><br>
              - **pulse rhythm** - This is an enum in the Canvas Vital command. Values supported are **Regular**, **Irregularly Irregular**, **Regulary Irregular**. If one of these values is not provided, a 422 error will occur. <br><br>
              - **blood pressure** - This is a string reprentation of the systolic and diastolic combined in the format `"100/80"`. If this valueString is not given, it will not appear correctly in the Canvas Vital Command. 
          - name: value[x]
            type: string | json
            exclude_in: create
            read_and_search_description: Actual result.<br><br>Canvas currently will support `valueQuantity` for observations with numeric values and `valueString` for observations containing text values. 
            attributes:
              - name: value
                type: number
                description: Numerical value (with implicit precision).
              - name: unit
                type: string
                description: Unit representation.
              - name: system
                type: string
                description: System that defines coded unit form.
                enum_options: 
                  - value: http://unitsofmeasure.org
              - name: code
                type: string
                description: Coded form of the unit
                enum_options:
                  - value: "[lb_av]"
                  - value: "cm"
                  - value: "[in_i]"
                  - value: "[degF]"
                  - value: "mm[Hg]"
                  - value: "%"
                  - value: "[in_i]"
                  - value: "/min"
                  - value: "kg/m2"
                  - value: "L/min"
          - name: dataAbsentReason
            type: json
            exclude_in: create
            description: Why the result is missing (if there is no `value[x]` section)
            attributes: 
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://terminology.hl7.org/CodeSystem/data-absent-reason
                  - name: code
                    description: The code of the observation.
                    type: string
                    enum_options: 
                      - value: not-performed
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Not Performed         
          - name: hasMember
            type: array[json]
            read_and_search_description: Related Observation reference(s) that belongs to the Observation group/panel. <br><br> In Canvas, all the vital signs taken in a Vitals Command will be listed in this `hasMember` attribute.
            create_description: >-
              Related Observation reference(s) that belongs to the Observation group/panel.<br><br>
              Only need to supply this attribute in a Vital Sign Panel to specify specific child observations that are a part of the panel. In Canvas these will form the Vitals Command. This observation IDs can be found using the [Observation Search](/api/observation/#search). <br><br>
              If a new vital sign panel is created and links pre-existing vital signs via the `hasMember` attribute, those linked observations will update their `derivedFrom` attribute to be set to the newly created vital sign panel.
            attributes:
                - name: reference
                  type: string
                  required_in: create
                  description: The reference string of the child observation in the format of `"Observation/920807d3-034b-4423-a65b-980068cb4bd1"`.
                - name: type
                  type: string
                  description: Type the reference refers to (e.g. "Observation").              
          - name: derivedFrom
            type: array[json]
            description: >-
              Related Observation resource that the Observation is made from.<br><br> In Canvas this observation would correspond to the "parent" vital sign panel.
            create_description: >-
              Related Observation resource that the Observation is made from.<br><br>
              This attribute should only be used to link a vital sign to an existing "parent" vital sign panel. It ingests a reference to the vital sign panel's observation. This observation ID can be found using the [Observation Search](/api/observation/#search).<br><br> 
              If this field is omitted on a vital sign observation, a vital sign panel will automatically be created. <br><br>
              It is important to note that each vital sign panel can only contain a single vital sign of each type. Adding a duplicate of a vital sign will result in a 422 error: "Vital sign reading already exists for the given reading".
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the child observation in the format of `"Observation/920807d3-034b-4423-a65b-980068cb4bd1"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Observation").   
          - name: component
            type: array[json]
            description: Component results. <br><br> Currently only used for blood pressure observations to display the systolic and diastolic components.
            create_description: >-
              Component results<br><br>
              This attribute is only used for blood pressure, as it has two components (systolic and diastolic). <br>
              
               - These components are added to a vital sign observation by including their `code` and `valueQuantity`. 
               - The components are what will be stored in the database; however, they will not display on the UI. The `Observation.valueString` will be the attribute that displays on the UI.
               - The `valueQuantity` for the systolic component should match the first number in the blood pressure vital sign `valueQuantity`, where the `valueQuantity` of the diastole component should match the second number.
            attributes:
              - name: code
                type: json
                description: Type of component observation (code / type).
                attributes: 
                  - name: coding
                    description: Identifies where the definition of the code comes from.
                    type: array[json]
                    attributes: 
                      - name: system
                        description: The system url of the coding.
                        type: string
                        enum_options:
                          - value: http://loinc.org
                      - name: code
                        description: The code of the observation.
                        type: string
                        required_in: create
                        enum_options: 
                          - value: 8480-6 (systolic)
                          - value: 8462-4 (diastolic)
                      - name: display
                        description: The display name of the coding.
                        type: string
                        enum_options:
                          - value: Systolic blood pressure
                          - value: Diastolic blood pressure
              - name: valueQuantity
                type: json
                description: Actual component result.
                attributes:
                  - name: value
                    type: number
                    description: Numerical value (with implicit precision).
                  - name: unit
                    type: string
                    description: Unit representation.
                    enum_options: 
                      - value: mmHg
                  - name: system
                    type: string
                    description: System that defines coded unit form.
                    enum_options: 
                      - value: http://unitsofmeasure.org
                  - name: code
                    type: string
                    description: Coded form of the unit
                    enum_options:
                      - value: "mm[Hg]"
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource id for the Observation
          - name: category
            type: string
            description: Classification of the type of observation
          - name: code
            type: string
            description: The code of the observation type
          - name: date
            type: array
            description: >-
              Obtained date/time (UTC).<br><br>
              The date parameter is specified with an operand an a date value in YYYY-MM-DD format, e.g. `/Observation?date=ge2021-09-16`. If no operand is provided, the operand **eq** is used.<br><br>
              Supported operands are: **eq**, **gt**, **ge**, **lt**
          - name: derived-from
            type: string
            description: >-
              Related measurements the observation is made from<br><br>
              Supported: **QuestionnaireResponse**
          - name: patient
            type: string
            description: A Canvas Patient resource
        endpoints: [create, read, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: observation-create-request
          example_response: observation-create-response
          description: >-
            Although the observation endpoint houses many different Canvas models, currently, **only vital signs and panels can be created through this endpoint**.<br><br>
            
            **Vital signs and Vital Sign Panels**<br>
              - Vital sign panels and vital signs are both observations.<br>
                - Vital sign panels are the parent that "contain" the vital sign observations.  The `hasMembers` attribute contains references to the child observations<br>
                - Each vital sign that is part of the panel links back to the parent Observation via the `derivedFrom` attribute.<br> 
                - If a `derivedFrom` value is not included for a vital sign observation, then a new vital sign panel observation is created and will autofill the `derivedFrom` attribute field.<br>
              - Vital signs and their parent panel feed into our [Vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs).<br><br>
            
            **Note types**<br>
            Most our FHIR endpoints insert commands into a Data Import Note type on the patient's timeline.
            With the release of [configurable note types](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-), if you create a new Note Type in Settings with **system = Canvas** and **code = VitalsImport**,
            then the Observation Create endpoint will always import into that note type instead.<br><br>


            **Supported vital sign codes**

              | vital sign                     | LOINC code | default unit | additional accepted units |
              | :----------------------------- | :--------- | :----------- | :------------------------ |
              | vital sign panel               | 85353-1    |              |                           |
              | blood pressure                 | 85354-9    | mmHg         |                           |
              | weight                         | 29463-7    | oz           | lb, kg                   |
              | height                         | 8302-2     | in           | cm                        |
              | pulse rate                     | 8867-4     | bpm          |                           |
              | body temperature               | 8310-5     | °F           |                           |
              | oxygen saturation (arterial)\* | 2708-6     | %            |                           |
              | oxygen saturation\*            | 59408-5    | %            |                           |
              | respiration rate               | 9279-1     | bpm          |                           |
              | waist circumference            | 56086-2    | cm           | in                        |
              | note                           | 80339-5    |              |                           |
              | pulse rhythm                   | 8884-9     |              |                           |

            *If an oxygen saturation vital sign is created, an oxygen saturation (arterial) vital sign code is also automatically generated.<br><br>
        
            **Additional examples**

              - [Creating a vital panel](https://www.postman.com/canvasmedical/workspace/canvas-medical-public-documentation/request/17030070-9375d12e-012c-4a68-8f2a-5709c758b4f0)
              - [Creating a vital sign with components (should only be used for blood pressure)](https://www.postman.com/canvasmedical/workspace/canvas-medical-public-documentation/request/17030070-b020fab6-334b-4aa9-9cde-cf1dc59444b4)
              - [Creating a vital sign without components](https://www.postman.com/canvasmedical/workspace/canvas-medical-public-documentation/request/17030070-f87d6190-3a72-42e0-9429-520bd6eaa66b)
        read:
          responses: [200, 401, 403, 404]
          example_request: observation-read-request
          example_response: observation-read-response
        search:
          responses: [200, 400, 401, 403]
          example_request: observation-search-request
          example_response: observation-search-response
---

<div id="observation-create-request">
  {% tabs observation-create-request %}
    {% tab observation-create-request curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Observation' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "resourceType": "Observation",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "29463-7",
        "display": "Weight"
      }
    ]
  },
  "subject": {
    "reference": "Patient/ee8672f3497e4a83937b9e71d0a704a5"
  },
  "effectiveDateTime": "2022-07-29T08:50:24.883809+00:00",
  "valueQuantity": {
    "value": "50",
    "unit": "kg"
  },
  "derivedFrom": [
    {
      "reference": "Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e"
    }
  ]
}
'
```
{% endtab %}

{% tab observation-create-request python %}
```python
import requests

url = "https://fumage-example.canvasmedical.com/Observation"

payload = {
    "resourceType": "Observation",
    "status": "final",
    "category": [
      { 
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
            "code": "vital-signs",
            "display": "Vital Signs"
          }
        ],
       }
    ],
    "code": {
      "coding": [
        {
          "system": "http://loinc.org",
          "code": "29463-7",
          "display": "Weight"
        }
      ]
    },
    "subject": { "reference": "Patient/ee8672f3497e4a83937b9e71d0a704a5" },
    "effectiveDateTime": "2022-07-29T08:50:24.883809+00:00",
    "valueQuantity": { "value": "50", "unit": "lb" },
    "derivedFrom": [{ "reference": "Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e" }]
}
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```
    {% endtab %}

  {% endtabs %}
</div>

<div id="observation-create-response">
{% include create-response.html %}
</div>

<div id="observation-read-request">
{% include read-request.html resource_type="Observation" %}
</div>

<div id="observation-read-response">
{% tabs observation-read-response %}
{% tab observation-read-response 200 %}
```json
{
    "resourceType": "Observation",
    "id": "43b74793-5de6-435a-871d-8ae2232f3aa0",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85353-1"
            }
        ]
    },
    "subject": {
        "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
        "type": "Patient"
    },
    "effectiveDateTime": "2022-06-28T20:18:54.141759+00:00",
    "issued": "2022-06-28T20:43:10.465819+00:00",
    "dataAbsentReason": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                "code": "not-performed",
                "display": "Not Performed"
            }
        ]
    },
    "hasMember": [
        {
            "reference": "Observation/40cec197-041f-4db5-bd12-addbfb68c3b3",
            "type": "Observation"
        },
        {
            "reference": "Observation/5fa47fbe-eeb3-43c8-a287-11b18cad40b7",
            "type": "Observation"
        },
        {
            "reference": "Observation/4533ad2e-7ea4-4ae9-8018-301e1b99dcbb",
            "type": "Observation"
        },
        {
            "reference": "Observation/8f2c43eb-feeb-49c8-b509-b67fb1ecca51",
            "type": "Observation"
        },
        {
            "reference": "Observation/6a908edf-f75c-4a40-87cb-347d8a753bae",
            "type": "Observation"
        },
        {
            "reference": "Observation/2966fcba-be4e-4400-bd4a-aa7051ee38c6",
            "type": "Observation"
        },
        {
            "reference": "Observation/89edc763-4129-4d6c-94c7-6a3bcf1c776f",
            "type": "Observation"
        },
        {
            "reference": "Observation/f578d894-cfe2-49c2-88d2-48f5109ceed9",
            "type": "Observation"
        },
        {
            "reference": "Observation/2e368a90-8038-49c4-a26e-ebebdb736269",
            "type": "Observation"
        },
        {
            "reference": "Observation/b93d554a-b54b-4375-b531-e4f6337dc42d",
            "type": "Observation"
        }
    ]
}
```
{% endtab %}
{% tab observation-read-response 401 %}
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

    {% tab observation-read-response 403 %}
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

    {% tab observation-read-response 404 %}
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown coverage resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
    {% endtab %}
{% endtabs %}
</div>

<div id="observation-search-request">
{% include search-request.html resource_type="Observation" search_string="category=vital-signs&patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2" %}
</div>

<div id="observation-search-response">
{% tabs observation-search-response %}
{% tab observation-search-response 200 %}
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 3,
  "link": [
    {
      "relation": "self",
      "url": "/Observation?category=vital-signs&patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
    },
    {
      "relation": "first",
      "url": "/Observation?category=vital-signs&patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
    }
    ,
    {
      "relation": "last",
      "url": "/Observation?category=vital-signs&patient=Patient%2Fa1197fa9e65b4a5195af15e0234f61c2&_count=10&_offset=0"
    }
  ],
  "entry": [
    {
      "resource": {
          "resourceType": "Observation",
          "id": "43b74793-5de6-435a-871d-8ae2232f3aa0",
          "status": "unknown",
          "category": [
            {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                  "code": "vital-signs",
                  "display": "Vital Signs"
                }
              ]
            }
          ],
          "code": {
              "coding": [
                {
                  "system": "http://loinc.org",
                  "code": "85353-1",
                  "display": "Vital Panel"
                }
              ]
          },
          "subject": {
              "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2",
              "type": "Patient"
          },
          "effectiveDateTime": "2022-06-28T20:18:54.141759+00:00",
          "issued": "2022-06-28T20:43:10.465819+00:00",
          "dataAbsentReason": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                  "code": "not-performed",
                  "display": "Not Performed"
                }
              ]
          },
          "hasMember": [
            {
              "reference": "Observation/40cec197-041f-4db5-bd12-addbfb68c3b3",
              "type": "Observation"
            },
            {
              "reference": "Observation/e0ba7d6e-be80-487a-a65c-b96af9b559d8",
              "type": "Observation"
            },
          ]
      }
    },
    {
      "resource": {
          "resourceType": "Observation",
          "id": "40cec197-041f-4db5-bd12-addbfb68c3b3",
          "status": "unknown",
          "category": [
            {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                  "code": "vital-signs",
                  "display": "Vital Signs"
                }
              ]
            }
          ],
          "code": {
              "coding": [
                  {
                    "system": "http://loinc.org",
                    "code": "85354-9",
                    "display": "BP"
                  }
              ]
          },
          "component": [ 
            {
              "code": {
                  "coding": [
                    {
                      "system": "http://loinc.org",
                      "code": "8480-6",
                      "display": "BP - Systolic"
                    }
                  ]
              },
              "valueQuantity": {
                  "value": 100
              }
            },
            {
              "code": {
                  "coding": [
                    {
                      "system": "http://loinc.org",
                      "code": "8462-4",
                      "display": "BP - Diastole"
                    }
                  ]
              },
              "valueQuantity": {
                  "value": 80
              }
            }
          ],
          "subject": {
              "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2"
          },
          "effectiveDateTime": "2022-06-01T08:50:24.883809+00:00",
          "derivedFrom": [
            {
              "reference": "Observation/43b74793-5de6-435a-871d-8ae2232f3aa0"
            }
          ]
      }
    },
    {
      "resource": {
          "resourceType": "Observation",
          "id": "e0ba7d6e-be80-487a-a65c-b96af9b559d8",
          "status": "unknown",
          "category": [
            {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                  "code": "vital-signs",
                  "display": "Vital Signs"
                }
              ]
            }
          ],
          "code": {
              "coding": [
                {
                  "system": "http://loinc.org",
                  "code": "29463-7",
                  "display": "Weight"
                }
              ]
          },
          "subject": {
              "reference": "Patient/a1197fa9e65b4a5195af15e0234f61c2"
          },
          "effectiveDateTime": "2022-09-29T08:50:24.883809+00:00",
          "valueQuantity": {
              "value": 50,
              "unit": "kg"
          },
          "derivedFrom": [
            {
              "reference": "Observation/43b74793-5de6-435a-871d-8ae2232f3aa0"
            }
          ]
      }
    }
  ]
}
```
{% endtab %}
{% tab observation-search-response 400 %}
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
{% tab observation-search-response 401 %}
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

    {% tab observation-search-response 403 %}
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
