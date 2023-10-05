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
            - [US Core Pediatric Weight for Height Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-pediatric-weight-for-height.html)
            - [US Core Smoking Status Observation Profile](https://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-smokingstatus.html)<br>
            
          The following USCDI data elements are retrievable from this endpoint:<br>
            - Laboratory Tests
            - Laboratory Values/Results
            - Smoking Status
        attributes:
          - name: id
            type: string
            description: >-
              The Canvas identifier of the observation
          - name: status
            type: string
            description: >-
              The status of the result value<br><br>
              Supported codes for create interactions:  **final**, **unknown**
            required: true
          - name: category
            type: array[json]
            description: >-
              Classifies the general type of observation being made<br><br>
              Supported for create interactions: **vital-signs**
            required: true
          - name: code
            type: json
            description: >-
              Describes what was observed<br><br>
              For create interactions, only vital sign LOINC codes are supported.  
            required: true
          - name: subject
            type: json
            description: >-
              Canvas Patient reference the Observation is for
            required: true
          - name: effectiveDateTime
            type: datetime
            description: >-
              Clinically relevant time/time-period for observation<br><br>
              For an individual vital sign, if the effectiveDateTime differs from the panel time, it will 
              be reflected in a read/search; however, you will not see the individual date in the UI, only the panel's datetime.<br><br>
              If omitted from create, Canvas will save a default value of the current datetime.
          - name: issued
            type: datetime
            description: >-
              Date/Time this version was made available<br><br>
              `issued` is not a field you can create via Observation Create -  it is the timestamp in Canvas when the vital record was ingested.
          - name: value[x]
            type: json
            description: >-
              Actual result<br><br>
              Supported value types for create interactions: `valueQuantity`<br><br>
              **Additional notes for create:**
               - If the observation is a vital sign panel, the `valueQuantity` will be ignored.<br>
               - For the submitted `code`, only units from the table above can be sent in `valueQuantity.unit`. Sending a different unit will result in a 422 error. 
               - If `unit` is omitted, the it will default to the unit in the table above.
               - If `value` is omitted, it will default to an empty field. 
               - If this field's input type cannot be converted to the given vital sign's expected type (e.g. a string "fifty" is given for weight), it will only display on the Canvas UI's patient chart on the left-hand column under vitals - it will not display in the Vitals command that is generated on the imported note. It will still be saved in the database and returned in a read/search.<br>
               - Blood pressure vital sign observations support components for diastolic and systolic blood pressure. However, if only the components are included, and the `valueQuantity` isn't included (e.g. "100/80"), it will not display on the Canvas UI.
               - When creating a vital sign for pulse rhythm, accepted values are: **Regular**, **Irregularly Irregular**, **Regulary Irregular**

          - name: dataAbsentReason
            type: json
            description: Why the result is missing (if there is no `value[x]` section)
          - name: hasMember
            type: array[json]
            description: >-
              Related Observation reference(s) that belongs to the Observation group/panel<br><br>
              Present when an Observation is something like a panel (e.g. a vital signs panel) and has child observations (e.g. pulse rhythm done as a part of the vitals signs panel)<br><br>
              If a new vital sign panel is created and links pre-existing vital signs via the `hasMember` attribute, those linked observations will update their `derivedFrom` attribute to be set to the newly created vital sign panel.
          - name: derivedFrom
            type: array[json]
            description: >-
              Related Observation resource that the Observation is made from<br><br>
              **For create interactions:**
              This attribute should only be used to link a vital sign to an existing "parent" vital sign panel. It ingests a reference to the vital sign panel's observation. This observation ID can be found using the [Observation Search](/api/observation/#search).<br><br> 
              It is important to note that each vital sign panel can only contain a single vital sign of each type. Adding a duplicate of a vital sign will result in a 422 error: "Vital sign reading already exists for the given reading".
          - name: component
            type: array[json]
            description: >-
              Component results<br><br>
              **For create interactions:** This attribute is only used for blood pressure, as it has two components (systolic and diastolic). <br>
              
               - These components are added to a vital sign observation by including their `code` and `valueQuantity`. 
               - The components are what will be stored in the database; however, they will not display on the UI. 
               - The `valueQuantity` for the blood pressure vital sign (e.g. "100/80") will be the one used to generate a display on the UI. 
               - The `valueQuantity` for the systolic component should match the first number in the blood pressure vital sign `valueQuantity`, where the `valueQuantity` of the diastole component should match the second number.
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
              Obtained date/time (UTC).  
              <li>Uses an operand and a date field in the format YYYY-MM-DD.</li>
              <li>eq, gt, ge, lt, and le are supported operands (eq is assumed if no operand is sent).</li>
              <li><b>Example</b>:  "/Observation?date=ge2021-09-16"</li>
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
            With the release of [configurable note types](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-), if you specify a new Note Type with **system = Canvas** and **code = VitalsImport**, 
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

              - [Creating a vital panel](https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-463cfe84-d9ff-42c9-a110-4fedfe2baa9b)
              - [Creating a vital sign with components (should only be used for blood pressure)](https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-4866da6b-f0ec-44d1-8a61-85441dc60ad7)
              - [Creating a vital sign without components](https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-3f5dbfe9-073f-45a6-ba49-38dc80e3c7ce)
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
    "unit": "in"
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
