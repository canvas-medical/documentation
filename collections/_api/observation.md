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

          <br><br>

            Here are some Canvas specific workflows where observations will be created:

            1. Documenting Vitals via our [Vital Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs) (category coding will be `vital-signs`)<br>
            2. Submitting a Questionnaire, Review Of System (ROS), Structured Assessment (SA), or a Physical Exam will result in an observation for each question answered if the question's code system is LOINC or SNOMED (category coding will be `social-history`). <br>
            3. There is a specific Physical Exam to capture Pediatric Vitals. Upon submission of the Exam, associated observations for Body Length, Head Circumference, and Head Occipital-Frontal Circumference Percentile (category coding will be `vital-signs`) will be created along with the observations for the answers of the exam (category coding will be `social-history`). Please contact Customer Support for help loading this Exam into your instance if you want to utilize it. <br>
            4. Once weight and either height or pediatric body length is entered on a patients chart, the vital observations of BMI for Age Percentile (for patients 2 years or older) and Weight-for-Length Percentile will be calculated (category coding will be `vital-signs`). 
            4. Submitting a Questionnaire that has custom scoring defined will result in an observation containing the scored value (category coding will be `survey`). <br>
            5. When a lab report is created in Canvas through [DI](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports), API, integration with HG, or [POC Lab Test Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055629214-Point-of-Care-POC-Tests), there will be resulting Observations made (category coding will be `laboratory`).
              
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
                      - value: social-history
                      - value: imaging
                      - value: laboratory
                      - value: procedure
                      - value: survey
                      - value: exam
                      - value: therapy
                      - value: activity
                  - name: display
                    description: The display name of the coding.
                    type: string
                    enum_options: 
                      - value: Vital Signs
                      - value: Social History
                      - value: Vital Signs
                      - value: Imaging
                      - value: Laboratory
                      - value: Procedure
                      - value: Survey
                      - value: Exam
                      - value: Therapy
                      - value: Activity
          - name: code
            type: json
            exclude_in: read, search
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
          - name: code
            type: json
            exclude_in: create, update
            description: Describes what was observed.
            attributes: 
              - name: extension
                description: For observations that do not have an associated code (e.g Laboratory Observations), an extension will be displayed to denote an absent of a coding.
                attributes:
                    - name: url
                      type: string
                      description: Reference that defines the content of this object.
                      enum_options:
                        - value: http://hl7.org/fhir/StructureDefinition/data-absent-reason
                    - name: valueString
                      type: string
                      description: The reason the Observation.coding attribute is missing. 
                      enum_options:
                        - value: unsupported
                        - value: unknown
              - name: coding
                description: Identifies where the definition of the code comes from.
                type: array[json]
                attributes: 
                  - name: system
                    description: >-
                      The system url of the coding.
                    type: string
                    enum_options:
                      - value: http://loinc.org
                      - value: http://snomed.info/sct
                  - name: code
                    description: The code of the observation.
                    type: string
                    enum_options: 
                      - value: Any LOINC codes from Vital Panel or Vital Signs captured in the Observation Create / Vital Command
                      - value: Any LOINC or SNOMED code from questions filled out through a Questionnaire, Structured Assessment, Physical Exam, Review of Systems
                      - value: Any code from a Questionnaire Scoring Result
                      - value: "Pediatric Vital observations: 8306-3 (Body Length), 8289-1 (Head Occipital-Frontal Circumference Percentile), and 8287-5 (Head Circumference)"
                      - value: 59576-9 (LOINC code for BMI for Age Percentile)
                      - value: 77606-2 (LOINC code for Weight-for-Length Percentile)
                      - value: Any LOINC codes from Lab Report Values captured 
                  - name: display
                    description: The display name of the coding.
                    type: string
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
            description: Date/Time this version was made available. It is the timestamp in Canvas when the observation was ingested.
          - name: valueQuantity
            type: json
            description: Actual result. <br><br> Used for observations with numeric values like vitals, lab report values, any questionnaire result scoring programed in Canvas.
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
                required_in: create
                description: Numerical value (with implicit precision).
              - name: unit
                type: string
                description: Unit representation.
                create_description: Unit representation. If omitted, it will default to the values in the table defined above. For the submitted `code`, only units from the table above can be sent. Sending a different unit will result in a 422 error.
              - name: system
                type: string
                exclude_in: create
                description: System that defines coded unit form.
                enum_options: 
                  - value: http://unitsofmeasure.org
              - name: code
                type: string
                exclude_in: create
                description: Coded form of the unit may be shown.
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
          - name: valueString
            type: string
            description: Actual result. <br><br> Used for observations containing text values like vitals that are strings (e.g Blood Pressure, notes, and pulse rhythm) and free text lab result values.
            create_description:
              Actual result.<br><br>

              This is used for vital observation that correspond with a string value. If this field is not provided or specifically the value attribute in the json is omitted, Canvas will interpret that as an empty value. A Read/Search of this observation will display the `dataAbsentReason` attribute. <br><br>

              Currently supported string values are <br>
              - **note** - this is a free text comment field in the Canvas Vital Command <br><br>
              - **pulse rhythm** - This is an enum in the Canvas Vital command. Values supported are **Regular**, **Irregularly Irregular**, **Regulary Irregular**. If one of these values is not provided, a 422 error will occur. <br><br>
              - **blood pressure** - This is a string reprentation of the systolic and diastolic combined in the format `"100/80"`. If this valueString is not given, it will not appear correctly in the Canvas Vital Command. 
          - name: valueCodeableConcept
            type: json
            exclude_in: create
            description: Actual result.<br><br>Used for observations with a selected coding like Questionnaire Responses showing the answer to a specific question. This comes from Questionnaires, Structured Assessment, Physical Exam, and Review of Systems in Canvas.
            attributes:
              - name: coding
                description: Identifies where the definition of the code comes from. Codings are used when the Observation comes from a QuestionnaireResponse.
                type: array[json]
                attributes: 
                  - name: system
                    description: The system url of the coding.
                    type: string
                  - name: code
                    description: The code of the observation.
                    type: string
                  - name: display
                    description: The display name of the coding.
                    type: string
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
                - name: display
                  type: string
                  description: The coding display of the reference.
          - name: derivedFrom
            type: array[json]
            description: >-
              Related resource that the Observation is made from.<br><br> 

              For vital signs, the derivedFrom reference would be the observation that corresponds to the "parent" vital sign panel this observation is part of.
              <br>
              For observations originating from a custom scoring of a Questionnaire or from answers filled out in Questionnaires, ROS, SA, or Physical Exams the `derivedFrom` attribute will be a reference to the associated QuestionnaireResponse record.
            create_description: >-
              Related Observation resource that the Observation is made from.<br><br>
              This attribute should only be used to link a vital sign to an existing "parent" vital sign panel. It ingests a reference to the vital sign panel's observation. This observation ID can be found using the [Observation Search](/api/observation/#search).<br><br> 
              If this field is omitted on a vital sign observation, a vital sign panel will automatically be created. <br><br>
              It is important to note that each vital sign panel can only contain a single vital sign of each type. Adding a duplicate of a vital sign will result in a 422 error: "Vital sign reading already exists for the given reading".
            attributes:
              - name: reference
                type: string
                required_in: create
                description: The reference string of the child observation in the format of `"Observation/920807d3-034b-4423-a65b-980068cb4bd1"` or `"QuestionnaireResponse/0e34b12d-0494-4ade-9a51-aa12225dd959"`.
              - name: type
                type: string
                description: Type the reference refers to (e.g. "Observation", "QuestionnaireResponse").
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
                required_in: create
                description: Type of component observation (code / type).
                attributes: 
                  - name: coding
                    required_in: create
                    description: Identifies where the definition of the code comes from.
                    type: array[json]
                    attributes: 
                      - name: system
                        description: The system url of the coding.
                        type: string
                        required_in: create
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
                        required_in: create
                        enum_options:
                          - value: Systolic blood pressure
                          - value: Diastolic blood pressure
              - name: valueQuantity
                type: json
                description: Actual component result. Since this endpoint only supports blood pressure systolic/diastolic components, the units are already defaulted to `mmHg`.
                exclude_in: read, search
                attributes:
                  - name: value
                    type: number
                    required_in: create
                    description: Numerical value (with implicit precision).
              - name: valueQuantity
                type: json
                exclude_in: create
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
              - name: dataAbsentReason
                type: json
                exclude_in: create
                description: Why the result is missing (if there is no `Component[x].value[y]` section)
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
        search_parameters:
          - name: _id
            type: string
            description: The Canvas resource id for the Observation
          - name: category
            type: string
            description: >-
              Classification of the type of observation. Filters by the code and/or system under `category.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g  `http://terminology.hl7.org/CodeSystem/observation-category|vital-signs`).
          - name: code
            type: string
            description: >-
              The code of the observation type. Filters by the code and/or system under `code.coding` attribute. You can search by just the code value or you can search by the system and code in the format `system|code` (e.g  `http://loinc.org|85353-1`).
          - name: date
            type: date
            description: Filter by the `effectiveDateTime` attribute. See [Date Filtering](/api/date-filtering) for more information.
          - name: derived-from
            type: string
            description: >-
              A reference to a related measurement the observation is made from. <br><br>

              Use this search parameter to find all observations of a specific vital panel or questionnaire response observations from the same interview.
            search_options: 
              - value: QuestionnaireResponse/_id
              - value: Observation/_id
          - name: patient
            type: string
            description: The patient reference associated to the observation in the format `Patient/a39cafb9d1b445be95a2e2548e12a787`.
        endpoints: [create, read, search]
        create:
          responses: [201, 400, 401, 403, 405, 422]
          example_request: observation-create-request
          example_response: observation-create-response
          description: >-
            Although the observation endpoint houses many different Canvas models, currently, **only vital signs and panels can be created through this endpoint**.<br><br>
            
            **Vital signs and Vital Sign Panels**<br>
            See this [helpful guide](/guides/submit-vitals-via-fhir/) to walk you through creating a vital panel via FHIR.<br>
              - Vital sign panels and vital signs are both observations.<br>
                - Vital sign panels are the parent that "contain" the vital sign observations.  The `hasMembers` attribute contains references to the child observations<br>
                - Each vital sign that is part of the panel links back to the parent Observation via the `derivedFrom` attribute.<br> 
                - If a `derivedFrom` value is not included for a vital sign observation, then a new vital sign panel observation is created and will autofill the `derivedFrom` attribute field.<br>
              - Vital signs and their parent panel feed into our [Vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs).<br><br>
            
            **Note types**<br>
            Most our FHIR endpoints insert commands into a Data Import Note type on the patient's timeline.
            With the release of [configurable note types](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-), if you create a new Note Type in Settings with **system = Canvas** and **code = VitalsImport**,
            then the Observation Create endpoint will always import into that note type instead.<br><br>


            **Supported vital sign codes used in create**

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
      "reference": "Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e",
      "type": "Observation"
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
            "reference": "Observation/dd7f25f3-0fa6-4f15-9b8c-c61c24f139d8",
            "type": "Observation",
            "display": "Weight"
        },
        {
            "reference": "Observation/3b96ab8b-aef6-4cbe-8ec5-b88c8e120e19",
            "type": "Observation",
            "display": "Body Temperature"
        },
        {
            "reference": "Observation/201d4404-60c0-4f07-88c1-534456271a74",
            "type": "Observation",
            "display": "Blood Pressure"
        },
        {
            "reference": "Observation/841187ae-0c35-4db7-8852-b5370e4a5c51",
            "type": "Observation",
            "display": "Pulse Rhythm"
        },
        {
            "reference": "Observation/60e563bd-7848-487d-8852-c0db383dc115",
            "type": "Observation",
            "display": "Oxygen Saturation Arterial"
        },
        {
            "reference": "Observation/cb8bca44-d0de-48b0-8786-6887a4b649ec",
            "type": "Observation",
            "display": "Height"
        },
        {
            "reference": "Observation/b96e8bd4-1db9-46db-b292-e9a474bdca44",
            "type": "Observation",
            "display": "Waist Circumference"
        },
        {
            "reference": "Observation/1e8b6774-82c3-4f0b-9b28-fca5fc17e8c9",
            "type": "Observation",
            "display": "Pulse"
        },
        {
            "reference": "Observation/8642e444-53a6-4db8-a15f-17fdb2e01247",
            "type": "Observation",
            "display": "Respiration Rate"
        },
        {
            "reference": "Observation/d0996ff1-643a-4711-88f8-2e303d208663",
            "type": "Observation",
            "display": "Note"
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
{% include search-request.html resource_type="Observation" search_string="category=vital-signs&patient=Patient/b60b818fad134c3095b34dd392be9533" %}
</div>

<div id="observation-search-response">
{% tabs observation-search-response %}
{% tab observation-search-response 200 %}
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 19,
    "link": [
        {
            "relation": "self",
            "url": "/Observation?patient=Patient%2Fb60b818fad134c3095b34dd392be9533&_count=20&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Observation?patient=Patient%2Fb60b818fad134c3095b34dd392be9533&_count=20&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Observation?patient=Patient%2Fb60b818fad134c3095b34dd392be9533&_count=20&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Observation",
                "id": "378d88eb-cbfc-4668-a96e-c1e011f9f015",
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
                            "code": "85353-1",
                            "display": "Vital Signs Panel"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-09T18:35:35.633932+00:00",
                "issued": "2024-04-09T18:35:35.651181+00:00",
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
                        "reference": "Observation/201d4404-60c0-4f07-88c1-534456271a74",
                        "type": "Observation",
                        "display": "Blood Pressure"
                    },
                    {
                        "reference": "Observation/60e563bd-7848-487d-8852-c0db383dc115",
                        "type": "Observation",
                        "display": "Oxygen Saturation Arterial"
                    },
                    {
                        "reference": "Observation/cb8bca44-d0de-48b0-8786-6887a4b649ec",
                        "type": "Observation",
                        "display": "Height"
                    },
                    {
                        "reference": "Observation/841187ae-0c35-4db7-8852-b5370e4a5c51",
                        "type": "Observation",
                        "display": "Pulse Rhythm"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "cb8bca44-d0de-48b0-8786-6887a4b649ec",
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
                            "code": "8302-2",
                            "display": "Height"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-09T18:35:35.754424+00:00",
                "issued": "2024-04-09T18:35:35.756630+00:00",
                "valueQuantity": {
                    "value": 69.0,
                    "unit": "in",
                    "system": "http://unitsofmeasure.org",
                    "code": "[in_i]"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/378d88eb-cbfc-4668-a96e-c1e011f9f015",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "60e563bd-7848-487d-8852-c0db383dc115",
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
                            "code": "2708-6",
                            "display": "Oxygen Saturation Arterial"
                        },
                        {
                            "system": "http://loinc.org",
                            "code": "59408-5",
                            "display": "Oxygen Saturation"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-09T18:35:35.744026+00:00",
                "issued": "2024-04-09T18:35:35.745602+00:00",
                "valueQuantity": {
                    "value": 98.0,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/378d88eb-cbfc-4668-a96e-c1e011f9f015",
                        "type": "Observation"
                    }
                ],
                "component": [
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "3150-0",
                                    "display": "Inhaled oxygen concentration"
                                }
                            ]
                        },
                        "valueQuantity": {
                            "value": 98.0,
                            "unit": "%",
                            "system": "http://unitsofmeasure.org",
                            "code": "%"
                        }
                    },
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "3151-8",
                                    "display": "Inhaled oxygen flow rate"
                                }
                            ]
                        },
                        "dataAbsentReason": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                                    "code": "not-performed",
                                    "display": "Not Performed"
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "841187ae-0c35-4db7-8852-b5370e4a5c51",
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
                            "code": "8884-9",
                            "display": "Pulse Rhythm"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-09T18:35:35.739851+00:00",
                "issued": "2024-04-09T18:35:35.741587+00:00",
                "valueString": "Regular",
                "derivedFrom": [
                    {
                        "reference": "Observation/378d88eb-cbfc-4668-a96e-c1e011f9f015",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "201d4404-60c0-4f07-88c1-534456271a74",
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
                            "code": "85354-9",
                            "display": "Blood Pressure"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-09T18:35:35.714893+00:00",
                "issued": "2024-04-09T18:35:35.716508+00:00",
                "valueString": "120/80 mmHg",
                "derivedFrom": [
                    {
                        "reference": "Observation/378d88eb-cbfc-4668-a96e-c1e011f9f015",
                        "type": "Observation"
                    }
                ],
                "component": [
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "8480-6",
                                    "display": "Systolic blood pressure"
                                }
                            ]
                        },
                        "valueQuantity": {
                            "value": 120.0,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "8462-4",
                                    "display": "Diastolic blood pressure"
                                }
                            ]
                        },
                        "valueQuantity": {
                            "value": 80.0,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "93d50727-307e-4be4-b4b3-fad266e22083",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "76503-2",
                            "display": "HARK - Kick"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-09T18:41:38.029091+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "LA33-6",
                            "display": "Yes"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/74b511d0-a112-48ff-9e03-ba5f103a2a15",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "b37b8285-b1e7-4298-9c25-a62b1303f799",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "76502-4",
                            "display": "HARK - Rape"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-09T18:41:38.024815+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "LA33-6",
                            "display": "Yes"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/74b511d0-a112-48ff-9e03-ba5f103a2a15",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "d3d10677-c211-4a04-ab8f-d5fe4b736bf8",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "76501-6",
                            "display": "HARK - Afraid"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-09T18:41:38.020391+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "LA33-6",
                            "display": "Yes"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/74b511d0-a112-48ff-9e03-ba5f103a2a15",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "77e9ef2c-f702-4cf7-ae6d-a093527a9727",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "76500-8",
                            "display": "HARK - Humiliated"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-09T18:41:38.012952+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "LA33-6",
                            "display": "Yes"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/74b511d0-a112-48ff-9e03-ba5f103a2a15",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "79e21363-d1e2-4be9-a9d0-2a737c595cd6",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "laboratory",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "code": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                            "valueCode": "unsupported"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-03T07:00:00+00:00",
                "issued": "2024-04-08T20:11:12.198162+00:00",
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
                        "reference": "Observation/13a6df29-a0c7-4233-a4e5-940c82f58006",
                        "type": "Observation",
                        "display": "Act.Prt.C Resist."
                    },
                    {
                        "reference": "Observation/84c34368-d839-4bb2-b967-787ecef5b595",
                        "type": "Observation",
                        "display": "Amended report:"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "84c34368-d839-4bb2-b967-787ecef5b595",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "laboratory",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "N/A",
                            "display": "Amended report:"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-03T07:00:00+00:00",
                "issued": "2024-04-08T20:11:12.256507+00:00",
                "valueString": "test"
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "13a6df29-a0c7-4233-a4e5-940c82f58006",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "laboratory",
                                "display": "Laboratory"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "13590-5",
                            "display": "Act.Prt.C Resist."
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-03T07:00:00+00:00",
                "issued": "2024-04-08T20:11:12.243418+00:00",
                "valueQuantity": {
                    "value": 1.0,
                    "unit": "ratio",
                    "system": "http://unitsofmeasure.org"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "f7370ea2-f44b-4f47-9ba1-073db8e6c365",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "survey",
                                "display": "Survey"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "76499-3"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-09T18:41:37.996595+00:00",
                "valueQuantity": {
                    "value": 4.0,
                    "system": "http://unitsofmeasure.org"
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/74b511d0-a112-48ff-9e03-ba5f103a2a15",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "1397bed8-7bab-4fdf-b926-b7542ccfbef0",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8287-5",
                            "display": "Head circumference (cm)"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-08T18:58:45.819506+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8287-5",
                            "display": "20"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/82f09164-afa8-462c-88e0-552b89976613",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "221534cf-690f-4166-86f2-7f392edf4348",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "social-history",
                                "display": "Social History"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8306-3",
                            "display": "Body length (in)"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:34.594656+00:00",
                "issued": "2024-04-08T18:58:45.805651+00:00",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8306-3",
                            "display": "30"
                        }
                    ]
                },
                "derivedFrom": [
                    {
                        "reference": "QuestionnaireResponse/82f09164-afa8-462c-88e0-552b89976613",
                        "type": "QuestionnaireResponse"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "84a41e03-34f2-414e-8bf8-c7fc8ee75c16",
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
                            "code": "8289-1",
                            "display": "Head Occipital-frontal circumference Percentile"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:45.616779+00:00",
                "issued": "2024-04-08T18:58:45.781371+00:00",
                "valueQuantity": {
                    "value": 90.0,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/74c7bcd6-a229-4bef-82fa-b0fec3c0cc1a",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "ab2cce20-4186-4ccd-bf7d-93009fbe7748",
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
                            "code": "8287-5",
                            "display": "Head Circumference"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:45.616779+00:00",
                "issued": "2024-04-08T18:58:45.766580+00:00",
                "valueQuantity": {
                    "value": 37.0,
                    "unit": "cm",
                    "system": "http://unitsofmeasure.org",
                    "code": "cm"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/74c7bcd6-a229-4bef-82fa-b0fec3c0cc1a",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "d0bb3a0f-8925-4bb8-958a-af0d37b095ab",
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
                            "code": "8306-3",
                            "display": "Length"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:45.616779+00:00",
                "issued": "2024-04-08T18:58:45.751224+00:00",
                "valueQuantity": {
                    "value": 20.0,
                    "unit": "in",
                    "system": "http://unitsofmeasure.org",
                    "code": "[in_i]"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/74c7bcd6-a229-4bef-82fa-b0fec3c0cc1a",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "74c7bcd6-a229-4bef-82fa-b0fec3c0cc1a",
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
                            "code": "85353-1",
                            "display": "Vital Signs Panel"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/b60b818fad134c3095b34dd392be9533",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-04-08T18:58:45.616779+00:00",
                "issued": "2024-04-08T18:58:45.629738+00:00",
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
                        "reference": "Observation/d0bb3a0f-8925-4bb8-958a-af0d37b095ab",
                        "type": "Observation",
                        "display": "Length"
                    },
                    {
                        "reference": "Observation/ab2cce20-4186-4ccd-bf7d-93009fbe7748",
                        "type": "Observation",
                        "display": "Head Circumference"
                    },
                    {
                        "reference": "Observation/84a41e03-34f2-414e-8bf8-c7fc8ee75c16",
                        "type": "Observation",
                        "display": "Head Occipital-frontal circumference Percentile"
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
