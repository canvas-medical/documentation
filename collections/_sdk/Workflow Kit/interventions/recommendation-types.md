---
title: "Recommendation Types"

---

We saw in our [last example](/sdk/workflow-sdk-quickstart/#expanding-a-protocol) that instead of adding an instance of a generic `Recommendation` to be passed to the `add_recommendation` method, we used an instance of the more specific `InterviewRecommendation` class. The Canvas Workflow Kit contains many built-in Recommendation classes that can be used to add different types of recommendations to a Protocol. These are used in order to provide guidance to a course of action for a patient.

To get you started using these recommendations, we have written out some example protocol code for you. Please see our [Open Source SDK repo](https://github.com/canvas-medical/open-source-sdk/tree/main/canvas_workflow_helpers/protocols/recommendations).
<br>
<br>
* * *
## AllergyRecommendation

**Description**: A recommendation specifying that a patient may have an allergy that should be recorded via the [allergy command](https://canvas-medical.help.usepylon.com/articles/9964004914-document-allergies).

**Parameters**:

| Name        | Type       | Required | Description                                                                                                                                                                                                                                                                                                                                       |
| ----------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                                                                                                       |
| `rank`      | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.                                                                                                                                                                 |
| `button`    | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                                                                                                                                                                        |
| `allergy`   | `ValueSet` | `true`   | The `ValueSet` class for the allergy that should be recommended. If multiple codings are supplied, they will all be stored with the same display that is populated from the `title` passed. It is strongly recommended that only a single coding is included to achieve expected behavior.                                                        |
| `title`     | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation. It will display next to the allergy button on the protocol window. It will populate the allergy name. If it is omitted, it will default to the allergy ValueSet name. It is strongly recommended that the title is set to the substance that the patient is allergic to. |
| `narrative` | _string_   | `false`  | The text used to populate the reaction field. It is strongly recommended that narrative is set to a string describing the reaction.                                                                                                                                                                                                               |
| `context`   | _dict_     | `false`  | A dictionary that stores the value of the allergy's severity ('mild', 'moderate', or 'severe') and onset date ("YYYY-MM-DD").                                                                                                                                                                                                                     |

**Note:** In the SDK patient object, only allergy records that have an onset date will be shown. If an allergy record does not have an associated date, it will not be able to satisfy the protocol because it will be filtered out of the dataset. 

**Example**:

```python
from canvas_workflow_kit.recommendation import AllergyRecommendation

class BeefAllergy(ValueSet):
    VALUE_SET_NAME = 'Beef Products'
    FDB = {'900124'}

allergy_recommendation = AllergyRecommendation(
      key='RECOMMEND_BEEF_ALLERGY',
      rank=1,
      button='Allergy',
      allergy=BeefAllergy,
      title='Beef Products',
      narrative='Swelling of the throat.',
      context={
             'severity': 'mild',
             'onset_date': "2022-08-11"
      }
)

result = ProtocolResult()
result.add_recommendation(allergy_recommendation)
result.add_narrative(allergy_recommendation.narrative)
```

An allergy recommendation will appear in the list of Protocols for applicable patients along with an allergy button:

![](https://files.readme.io/7559882-Screen_Shot_2022-08-10_at_2.58.20_PM.png "Screen Shot 2022-08-10 at 2.58.20 PM.png"){:width="50%"}

When the "Allergy" button is clicked, it will generate an Allergy command:

![](https://files.readme.io/2a66399-Screen_Shot_2022-08-10_at_2.58.32_PM.png "Screen Shot 2022-08-10 at 2.58.32 PM.png"){:width="70%"}
<br>
<br>
* * *
## AssessRecommendation

**Description**: A recommendation specifying that a patient may need to have an active condition assessed that should be recorded via the [assess condition command](https://canvas-medical.help.usepylon.com/articles/7998893827-managing-conditions#assessing-a-condition-8).

**Parameters**:

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>key</code></td>
      <td><em>string</em></td>
      <td><strong>true</strong></td>
      <td>A unique identifier for the recommendation.</td>
    </tr>
    <tr>
      <td><code>rank</code></td>
      <td><em>integer</em></td>
      <td><strong>true</strong></td>
      <td>A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.</td>
    </tr>
    <tr>
      <td><code>button</code></td>
      <td><em>string</em></td>
      <td><strong>false</strong></td>
      <td>The text that will appear on the button next to a Protocol recommendation. If not provided, it will default to <code>Assess</code>.</td>
    </tr>
    <tr>
      <td><code>title</code></td>
      <td><em>string</em></td>
      <td><strong>false</strong></td>
      <td>The text to show on a patient's chart that describes the recommendation. It will display next to the assess button on the protocol window. If omitted, it will default to <code>Assess condition</code>.</td>
    </tr>
    <tr>
      <td><code>context</code></td>
      <td><em>dict</em></td>
      <td><strong>false</strong></td>
      <td>
        A dictionary that stores various information to pass to the command fields. It accepts the following keys (all are optional):
        <ul>
          <li><code>background</code>: String text representing the background of the condition.</li>
          <li><code>narrative</code>: Text representing "today's assessment" of the condition.</li>
          <li><code>condition_id</code>: This is an integer representing one of the conditions. You can find this id by searching for the condition in the <code>self.patient.conditions</code> list.</li>
          <li><code>status</code>: This string represents the status of the condition you are assessing. You can specify it to be <code>improved</code>, <code>stable</code>, or <code>deteriorated</code>.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>



**Note:** In the SDK patient object, only allergy records that have an onset date will be shown. If an allergy record does not have an associated date, it will not be able to satisfy the protocol because it will be filtered out of the dataset. 

**Example**:

```python
from canvas_workflow_kit.recommendation import AssessRecommendation

class Depression(ValueSet):
    VALUE_SET_NAME = "Depression, unspecified"
    ICD10CM = {'F32A'}
    
conditions = self.patient.conditions.find(Depression).filter(clinicalStatus='active')
if len(conditions):
  assess_recommendation = AssessRecommendation(
    key='RECOMMEND_ASSESS_CONDITION',
    rank=1,
    button='Assess',
    patient=self.patient,
    title=f'Assess Condition: {condition["coding"][0]["display"]}',
    context={
      "background": "This is the background",
      "narrative": "This is today's assessment",
      "condition_id": condition['id'],
      "status": "improved"
    }
  )

  result = ProtocolResult()
  result.add_recommendation(assess_recommendation)
  result.add_narrative("Patient has an condition to assess")
```

An assess recommendation will appear in the list of Protocols for applicable patients along with an assess button:

![](https://files.readme.io/ad3bb90-Screenshot_2023-06-13_at_5.18.16_PM.png){:width="50%"}

When the "Assess" button is clicked, it will generate an Assess command:

![](https://files.readme.io/3afa278-Screenshot_2023-06-13_at_5.22.23_PM.png){:width="70%"}
<br>
<br>
* * *
## DiagnoseRecommendation

**Description**: A recommendation specifying that a patient may require a condition to be diagnosed. A Diagnose Recommendation allows providers the ability to create a [Diagnose Command](https://canvas-medical.help.usepylon.com/articles/7998893827-managing-conditions#diagnosing-a-condition-2) with the click of a button directly in a patient's chart.

**Parameters:**

| Name        | Type       | Required | Description                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `key`       | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                                                                                                                                                            |
| `rank`      | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top.                                                                                                                                                                                                                    |
| `button`    | _string_   | `true`   | The text that will appear on the button next to the Recommendation. When clicked, an `Diagnose` command will appear as a Note command in the patient's chart.                                                                                                                                                                                                                                          |
| `patient`   | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                                                                                                                                                                                                                            |
| `condition` | `ValueSet` | `true`   | The `ValueSet` class for the diagnosis that is being recommended. It is recommended that a ValueSet with only a single code is included.                                                                                                                                                                                                                                                               |
| `title`     | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation. This will also be the title of the diagnosis. It is recommended that title is inputted as the name of the diagnosis. If the title is not included in the recommendation, it will default to the name of the condition ValueSet.                                                                                               |
| `narrative` | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command `add_narrative(diagnose_recommendation.narrative) must be used. If a narrative is not included in the recommendation, but the `add_narrative\` command is used, the narrative will be automatically set to "Consider diagnosing {patient.first_name} with {condition.name}" |

**Example**:

```python

class Hypertension(ValueSet):
    VALUE_SET_NAME = 'Essential (Primary) Hypertension'
    ICD10CM = {'I10'}

diagnose_recommendation = DiagnoseRecommendation(
    key='RECOMMEND_HYPERTENSION_DIAGNOSIS',
    rank=1,
    button='Diagnose',
    patient=self.patient,
    condition=Hypertension,
    title='Essential Hypertension',
    narrative="This is the narrative."
)

result = ProtocolResult()
result.add_recommendation(diagnose_recommendation)
result.add_narrative(diagnose_recommendation.narrative)

```

A Diagnose recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/ffbb4bc-Screen_Shot_2022-08-08_at_4.57.53_PM.png "Screen Shot 2022-08-08 at 4.57.53 PM.png"){:width="50%"}

When the "Diagnose" button is clicked, it will generate a Diagnose command and populate it with the title of the recommendation as the diagnosis name followed by the code in the conditions ValueSet:

![](https://files.readme.io/975dca0-Screen_Shot_2022-08-08_at_4.57.44_PM.png "Screen Shot 2022-08-08 at 4.57.44 PM.png"){:width="70%"}
<br>
<br>
* * *
## FollowUpRecommendation

**Description**: A recommendation specifying that a patient may require a Follow Up appointment, which can be indicated using the [Follow Up](https://canvas-medical.help.usepylon.com/articles/4617508394-appointment-mangement#scheduling-follow-up-appointment-84) command.

**Parameters:**

| Name        | Type      | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_  | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `rank`      | _integer_ | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top.                                                                                                                                                                                                                                                                                                                                                                                           |
| `button`    | _string_  | `true`   | The text that will appear on the button next to the Recommendation. When clicked, an `Follow Up` command will appear as a Note command in the patient's chart.                                                                                                                                                                                                                                                                                                                                                                                                                |
| `patient`   | `Patient` | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `title`     | _string_  | `false`  | The text to show on a patient's chart that describes the recommendation. If it is omitted, it will default to "Request follow-up appointment"                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `narrative` | _string_  | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command `add_narrative(followUp_recommendation.narrative) must be used. If a narrative is not included in the recommendation, but the `add_narrative\` command is used, it will default to "{patient.name} needs a follow-up appointment."                                                                                                                                                                                                                 |
| `context`   | _dict_    | `false`  | A dictionary that may optionally contain the keys: <br> `requested_date` - where the value is a string in the format "YYYY-MM-DD" <br>`reason_for_visit` - where the value is a string representing free text for reason for visit description <br> `reason_for_visit_coding` - where the value is a string that matches the coding of a structured RFV <br> `internal_comment` - where the value is a string that will populate the 'scheduling comments' field of the Follow Up command <br> `requested_note_type` - where the value is a code pertaining to a note type. This note type must be scheduleable. To learn more about configurable note types, see this [article](/documentation/appointment-and-note-types). |

**Example**:

```python

followUp_recommendation = FollowUpRecommendation(
     key='RECOMMEND_FOLLOW_UP',
     rank=1,
     button='Follow up',
     patient=self.patient,
     title=f'Follow Up with {self.patient.first_name}',
     narrative='This is the narrative.',
     context={
         'requested_date':'2022-09-02',
          'reason_for_visit':'Concussion followup',
          'internal_comment':'This is the internal comment.'
          'requested_note_type':'308335008' # Office Visit code
      }
)

result = ProtocolResult()
result.add_recommendation(followUp_recommendation)
result.add_narrative(followUp_recommendation.narrative)
```

A Follow Up recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/7cb8e24-Screen_Shot_2022-08-11_at_12.13.52_PM.png "Screen Shot 2022-08-11 at 12.13.52 PM.png"){:width="50%"}

Upon clicking the Follow up button, the `Follow Up` command will be populated: 

![](https://files.readme.io/7004a3f-Screen_Shot_2022-08-11_at_10.38.56_AM.png "Screen Shot 2022-08-11 at 10.38.56 AM.png"){:width="70%"}
<br>
<br>
* * *
## HyperlinkRecommendation

**Description**: A recommendation specifying a button and href that opens a link in a new tab.

**Parameters**:

| Name        | Type      | Required | Description                                                                                                                                                                                  |
| ----------- | --------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_  | `true`   | A unique identifier for the recommendation.                                                                                                                                                  |
| `rank`      | _integer_ | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top.          |
| `button`    | _string_  | `true`   | The text that will appear on the button next to the recommendation.                                                                                                                          |
| `href`      | _string_  | `true`   | A fully-qualified URL that the button will link to.                                                                                                                                          |
| `title`     | _string_  | `true`   | The text to show that describes the link.                                                                                                                                                    |
| `narrative` | _string_  | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(hyperlink_recommendation.narrative) must be used. |

**Example**:

```python
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import ClinicalQualityMeasure
from canvas_workflow_kit.protocol import ProtocolResult
from canvas_workflow_kit.protocol import STATUS_DUE
from canvas_workflow_kit.recommendation import HyperlinkRecommendation


class HyperlinkExample(ClinicalQualityMeasure):

    class Meta:
        title = 'Hyperlink Example Title'
        description = 'Hyperlink Example Description'
        version = '2024-10-08'
        information = 'https://docs.canvasmedical.com'
        identifiers = ['CNV178']
        types = ['WWW']
        compute_on_change_types = [CHANGE_TYPE.ENCOUNTER, CHANGE_TYPE.PATIENT]
        references = ['Protocol Reference https://www.canvasmedical.com/protocols']

    def in_denominator(self):
        return True

    def in_numerator(self):
        return False

    def compute_results(self):
        result = ProtocolResult()        
        hyperlink_recommendation = HyperlinkRecommendation(
            key='PROTOCOL_DOCUMENTATION_LINK',
            rank=1,
            button='Custom Button Text',
            href='https://www.canvasmedical.com/',
            title='Hyperlink Example'
        )
        
        result = ProtocolResult()
        result.status = STATUS_DUE
        result.add_recommendation(hyperlink_recommendation)
        result.add_narrative(f'{self.patient.first_name} should refer to the linked resource.')

        return result
```

A recommendation that contains the link will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/56c85b4-recs_href_card.png "recs_href_card.png"){:width="60%"}
<br>
<br>
* * *
## ImagingRecommendation

**Description**: A recommendation specifying that a patient may be due for an imaging order. An Imaging Recommendation allows providers the ability to create an [Image command](https://canvas-medical.help.usepylon.com/articles/2615916315-order-an-imaging-study) with the click of a button directly in a patient's chart.

**Parameters:**

| Name          | Type       | Required | Description                                                                                                                                                                                |
| ------------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `key`         | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                |
| `rank`        | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top.        |
| `button`      | _string_   | `true`   | The text that will appear on the button next to the Recommendation. When clicked, an `Imaging` command will appear as a Note command in the patient's chart.                               |
| `patient`     | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                |
| `imaging`\*   | `ValueSet` | `true`   | The `ValueSet` class for the imaging that is being ordered. It is recommended that a ValueSet with only a single code is included.                                                         |
| `title`       | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                   |
| `context` | _dict_     | `false`  | A dictionary that may contain the keys `conditions` and `priority`. If `conditions` is included, it will populate the indications field of the `image` command. If `priority` is included, it will specify the priority level for the image processing task. The `priority` can either be `routine` or `urgent`.                                          |
| `narrative`   | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(imaging_recommendation.narrative) must be used. |

\* Imaging Note: In order for the coding in the imaging argument above to populate the image command, the Image Order Templates in the settings page must have an entry that matches. If there is not a matching image order template, one can be created via the admin settings. Select 'Imaging report templates', which can be found under the **data integration** section. Then select 'ADD IMAGING REPORT TEMPLATE' on the upper righthand corner. The name and long name can be any string, but the code must match the code associated with the imaging object that was passed in. The code system must be inputted in url format (e.g. LOINC would be <http://loinc.org>). The mappings are shown below. For help setting up these templates correctly or if access is needed, please consult Canvas's support and implementation teams. 

| code system | url                              |
| :---------- | :------------------------------- |
| SNOMED      | <http://snomed.info/sct>         |
| LOINC®       | <http://loinc.org>               |
| CPT®         | <http://www.ama-assn.org/go/cpt> |

If there are multiple codings in the ValueSet passed into the imaging argument, the coding that was entered first into the database will be used. We strongly recommend you only pass the single coding desired. 

**Example**:

```python
class BoneScan(ValueSet):
        VALUE_SET_NAME = 'SPECT Whole body Bone'
        LOINC = {'39820-6'}

class Osteopenia(ValueSet):
        VALUE_SET_NAME = 'Other specified disorders of bone density and structure, unspecified site'
        ICD10CM = {'M8580'}

imaging_recommendation = ImagingRecommendation(
            key='RECOMMEND_BONESCAN',
            rank=1,
            button='Order',
            patient=self.patient,
            imaging=BoneScan, 
            title='Order a SPECT Whole body Bone', 
            narrative='A bonescan should be ordered for this patient.',
            context={
                'conditions': [[{ #condition must already exist in the patient or won't show up
                    'code': 'M8580',
                    'system': 'ICD-10',
                    'display': Osteopenia.VALUE_SET_NAME,
                }]],
                'priority': 'Urgent'  # options are Routine or Urgent
            }
        )

result = ProtocolResult()
result.add_recommendation(imaging_recommendation)
result.add_narrative(imaging_recommendation.narrative)
```

An Imaging recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/110df3c-Screen_Shot_2022-08-05_at_12.41.12_PM.png "Screen Shot 2022-08-05 at 12.41.12 PM.png"){:width="50%"}

After pressing the _Order_ button, a Note Command to order imaging will be populated in the chart:

![](/assets/images/imagerec.png){:width="80%"}
<br>
<br>
* * *
## ImmunizationRecommendation

**Description**: A recommendation specifying that a patient may be due for an immunization. Use this to guide the user to the [immunization command](https://canvas-medical.help.usepylon.com/articles/4155771468-command-immunize).

**Parameters**:

| Name             | Type       | Required | Description                                                                                                                                                                                     |
| ---------------- | ---------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`            | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                     |
| `rank`           | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.               |
| `button`         | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                      |
| `patient`        | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                     |
| `immunization`\* | `ValueSet` | `true`   | The `ValueSet` class for the immunization that should be administered. Canvas currently only accepts cvx codings. The ValueSet should only contain one coding.                                  |
| `title`\*\*      | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                        |
| `context`        | _dict_     | `false`  | A dictionary that stores the value of the immunization's sig when key='sig'. (eg. context={'sig': 'Administer shot to the upper arm'})                                                          |
| `narrative`      | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(immunization_recommendation.narrative) must be used. |

\* immunization note: It is recommended that the ValueSet that the `immunization` argument is set to only contain a single code. However, if the ValueSet contains multiple codes, it will recommend the immunization code that was last in the list. It is important to note that this list will likely be reordered, and as such, using only one code is strongly recommended. Additionally, if the ValuesSet includes multiple codes, Canvas will generate a record of all of these immunizations and link them to the patient. Only the last item in the list will autofill in the immunize command and will be shown on the patient's chart.

\*\* title note: The title will be displayed next to the immunization button. Additionally, the name of the immunization that is autofilled into the immunize command will be generated from this string.  The immunization name will be anything following "order a" or "perform a". If neither of these prefixes are present, the title will exactly match the name of the immunization. 

**Example**:

```python
from canvas_workflow_kit.recommendation import ImmunizationRecommendation

class FluShotRec(ValueSet):
    VALUE_SET_NAME = 'Influenza, seasonal, injectable'
    CVX ={'141'}  

immunization_recommendation = ImmunizationRecommendation(
            key='RECOMMEND_INFLUENZA_VACCINE',
            rank=1,
            button='Immunize',
            patient=self.patient,
            immunization=FluShotRec, 
            title='Perform a Influenza Immunization',
            narrative='Administer an annual flu vaccine',
            context={'sig': 'This the sig'}
)

result = ProtocolResult()
result.add_recommendation(immunization_recommendation)
result.add_narrative(immunization_recommendation.narrative)
```

An immunization recommendation will appear in the list of Protocols for applicable patients along with an immunize button:

![](https://files.readme.io/31bf15d-Screen_Shot_2022-08-12_at_11.41.51_AM.png "Screen Shot 2022-08-12 at 11.41.51 AM.png"){:width="50%"}

Upon clicking the _Immunize_ button, the _Immunize_ command will be populated in the patient's chart:

![](https://files.readme.io/a14a2f9-Screen_Shot_2022-08-05_at_1.34.07_PM.png "Screen Shot 2022-08-05 at 1.34.07 PM.png"){:width="70%"}
<br>
<br>
* * *
## InstructionRecommendation

**Description**: A recommendation specifying that a provider may need to provide a set of instructions to a patient. An Instruction Recommendation allows providers the ability to create an [Instruct command](https://canvas-medical.help.usepylon.com/articles/4244748724-command-instruct) with the click of a button directly in a patient's chart.

**Parameters**:

| Name            | Type       | Required | Description                                                                                                                                                                                    |
| --------------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`           | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                    |
| `rank`          | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.              |
| `button`        | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                     |
| `patient`       | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                    |
| `instruction`\* | `ValueSet` | `true`   | The `ValueSet` class for the instruction given to the patient. Canvas only accepts snomed codes for instructions. The ValueSet should only contain one coding.                                 |
| `title`\*\*     | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                       |
| `narrative`     | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(instruction_recommendation.narrative) must be used. |

\* instruction note: If multiple codes are added to the instruction ValueSet, the instruct command's autofill feature will default to the last code in the list. Therefore, we recommend using a value set with only a single code.

\*\* title note: the title determines the text that is displayed in the autofilled instruct command. It is treated as an open text field. If no title is added, it defaults to "Instruct", followed by the ValueSet name. 

**Example**:

```python
from canvas_workflow_kit.recommendation import InstructionRecommendation

class LowCholesterolInstruction(ValueSet):
    VALUE_SET_NAME = 'How to Eat to Lower Cholesterol'
    SNOMEDCT = {'183062005'}

instruction_recommendation = InstructionRecommendation(
            key='RECOMMEND_DISCUSS_DIET',
            rank=1,
            button='Instruct',
            patient=self.patient,
            instruction=LowCholesterolInstruction,
            title='Discuss and Instruct on Dietary Recommendations',
            narrative="This is the narrative"
)

result = ProtocolResult()
result.add_recommendation(instruction_recommendation)
result.add_narrative(instruction_recommendation.narrative)
```

An Instruction recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/12b633d-Screen_Shot_2022-08-05_at_2.14.10_PM.png "Screen Shot 2022-08-05 at 2.14.10 PM.png"){:width="50%"}

Upon clicking the _Instruct_ button, the _Instruct_ command will be populated in the patient's chart:

![](https://files.readme.io/5dc873b-Screen_Shot_2022-08-05_at_2.14.24_PM.png "Screen Shot 2022-08-05 at 2.14.24 PM.png"){:width="70%"}
<br>
<br>
* * *
## InterviewRecommendation

**Description**: A recommendation specifying that a patient may need to complete one or more questionnaires.  
An Interview Recommendation allows providers the ability to create a [Questionnaire command](https://canvas-medical.help.usepylon.com/articles/5651999344-command-questionnaire) with the click of a button directly in a patient's chart.

**Parameters**:

| Name               | Type             | Required | Description                                                                                                                                                                                  |
| ------------------ | ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`              | _string_         | `true`   | A unique identifier for the recommendation.                                                                                                                                                  |
| `rank`             | _integer_        | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.            |
| `button`           | _string_         | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                   |
| `patient`          | `Patient`        | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                  |
| `questionnaires`\* | `list[ValueSet]` | `true`   | A list of `ValueSet` classes for the questionnaire(s) to be completed by the patient. It accepts the following coding systems: LOINC, SNOMED, INTERNAL.                                      |
| `title`            | _string_         | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                     |
| `narrative`        | _string_         | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(interview_recommendation.narrative) must be used. |

\* interview note: for this feature to work as expected, each questionnaire loaded into Canvas should have a unique coding. If two questionnaires share the same coding, the first item found in Canvas will be used. If two questionnaire codings are included in the ValueSet, the first item in the list will be used to autogenerate the interview command. To learn more about importing questionnaires to Canvas, see [here](/documentation/questionnaires). 

**Example**:

```python
from canvas_workflow_kit.recommendation import InterviewRecommendation

class PHQ9(ValueSet):
    VALUE_SET_NAME = 'PHQ-9 Depression Screening' 
    LOINC = {'44249-2'}

interview_recommendation = InterviewRecommendation(
            key='RECOMMEND_PHQ9_DIABETES',
            rank=1,
            button='Interview',
            patient=self.patient,
            questionnaires=[PHQ9],
            title='Patient is due for their PHQ-9 assessment'
)

result = ProtocolResult()
result.add_recommendation(interview_recommendation)
```

An Interview recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/4c11524-Screen_Shot_2022-08-05_at_3.18.35_PM.png "Screen Shot 2022-08-05 at 3.18.35 PM.png"){:width="50%"}

Upon pressing the _Interview_ button, the _Questionnaire_ command will populate the patient's chart:

![](https://files.readme.io/a7dfe43-Screen_Shot_2022-08-05_at_3.22.24_PM.png "Screen Shot 2022-08-05 at 3.22.24 PM.png"){:width="70%"}
<br>
<br>
* * *
## LabRecommendation

**Description**: A recommendation specifying that a patient may be due for a Lab order. A Lab Recommendation allows providers the ability to create a [Lab Order](https://canvas-medical.help.usepylon.com/articles/3065191197-placing-a-lab-order) with the click of a button directly in a patient's chart.

**Parameters**:

| Name       | Type       | Required | Description                                                                                                                       |
|------------|------------|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| `key`      | _string_   | `true`   | A unique identifier for the recommendation.                                                                                        |
| `rank`     | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. Recommendations with lower rank values will appear at the top. |
| `button`   | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                       |
| `patient`  | _Patient_  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                       |
| `condition`| _ValueSet_ | `true`   | A `ValueSet` class for the patient's condition associated with the reason for the lab recommendation. This argument is required, and if the title is not added, the ValueSet's name will be used to generate a narrative. |
| `lab`      | _ValueSet_ | `true`   | A `ValueSet` class for the laboratory test.                                                                                       |
| `title`    | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                          |
| `context`  | _dict_     | `false`  | A dictionary that may contain the key 'conditions'. If 'conditions' is included, it will populate the indications field of the `lab order` command. If 'health_gorilla_order_codes' is included, it will prioritize searching for laboratory tests that include the given code over the one specified in the lab parameter (e.g., `'health_gorilla_order_codes': ['1234']`). |
| `narrative`| _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to display successfully, use the command `add_narrative(lab_recommendation.narrative)`. |


Additional notes:

- The lab test that populates the lab order command is found in Canvas with the following logic:  
      1. If your ValueSet contains a CPT code, it will try to find a lab test with the matching CPT code.  
      2. If your ValueSet contains a LOINC, it will try to find a lab test in Generic lab with an order code matching the LOINC code.  
      3. If a lab test wasn't found in steps 1 and 2, it will generate a new lab test under the Generic lab using the recommendation title (removing the prefix of "order a" if given) followed by the coding in parentheses. If no title is provided, the title will be generated using the ValueSet's name ("Order `ValueSet.name`"). 

- If multiple codings from the ValueSet are found within the Canvas database, it will use the first coding entered into the system. 

- Currently when a `Lab Order` command is committed, it will not appear in the `self.patient` object. For a lab recommendation to be satisfied, a lab report must be attached to this patient using our [Data Integrations](https://canvas-medical.help.usepylon.com/articles/8618913529-data-integration-overview) feature and the report must be reviewed by a practitioner. So, a Lab Report Template must exist that contains the coding for the lab ValueSet that is being recommended. To learn more about importing lab report templates, see this [Zendesk article](https://canvas-medical.help.usepylon.com/articles/5081934202-custom-lab-report-templates).

**Example**:

```python
from canvas_workflow_kit.recommendation import LabRecommendation
from canvas_workflow_kit.value_set.v2021 import (
    Diabetes)

class HBA1C(ValueSet):
    VALUE_SET_NAME = 'HbA1c Laboratory Test'
    LOINC = {'4548-4'}

lab_recommendation = LabRecommendation(
            key='RECOMMEND_HBA1C',
            rank=1,
            button='Order',
            patient=self.patient,
            condition=Diabetes,
            lab=HBA1C,
            title='HbA1c Blood Test',
            context={'conditions': [[{
                'code': 'O2402',
                'system': 'ICD-10',
                'display': "Pre-existing type 1 diabetes mellitus, in childbirth",
            }]]}
)

result = ProtocolResult()
result.add_recommendation(lab_recommendation)
```

A Lab recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/080ad6e-Screen_Shot_2022-08-05_at_3.37.21_PM.png "Screen Shot 2022-08-05 at 3.37.21 PM.png"){:width="50%"}

Upon pressing the _Order_ button, the _Lab Order_ command will populate the patient's chart:

![](https://files.readme.io/9b5a9ce-Screen_Shot_2022-08-05_at_3.37.31_PM.png "Screen Shot 2022-08-05 at 3.37.31 PM.png"){:width="70%"}
<br>
<br>
* * *
## PerformRecommendation

**Description**: A recommendation specifying that a provider may need to [perform an In-Office Procedure](https://canvas-medical.help.usepylon.com/articles/5988007695-command-perform) for a patient. A Perform Recommendation allows providers the ability to create an Instruction command with the click of a button directly in a patient's chart.

**Parameters**:

| Name        | Type       | Required | Description                                                                                                                                                                                                                                                |
| ----------- | ---------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                |
| `rank`      | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.                                                                          |
| `button`    | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                                                                                 |
| `patient`   | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                                                                                |
| `procedure` | `ValueSet` | `true`   | A `ValueSet` class for the procedure being recommended.                                                                                                                                                                                                    |
| `condition` | `ValueSet` | `true`   | A `ValueSet` class for the condition associated with the reason for the procedure. Although this argument is required, it will only be used to generate the narrative if the title is omitted. The narrative only utilizes the condition ValueSet's title. |
| `title`     | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                                                                                   |
| `narrative` | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(perform_recommendation.narrative) must be used.                                                                 |

**Notes**:

- In order for the autofill functionality to work correctly, the procedure must include at least one code that exists in the fee schedule. To learn more about how to enter procedures into the fee schedule, see this [article](https://canvas-medical.help.usepylon.com/articles/6307219926-fee-schedule). Currently, the fee schedule only accepts CPT codes. 
- If none of the codes in the procedure ValueSet are in the fee schedule, the perform command will not auto-populate with a procedure. 
- If multiple codes in the procedure ValueSet are in the fee schedule, the perform command will be autofilled with the one that was most recently added to the fee schedule. To ensure expected behavior, it is recommended that only a single code is entered in the procedure ValueSet. 
- If a title is not included, both the title and narrative will be autogenerated. The title will be set to "Perform procedure.name" and the narrative will be set to "`patient.first_name` has `condition.name` and a `procedure.name` is recommended". 
- The command will autofill with the title (either inputted or auto-generated) without the prefix of "perform a", followed by the CPT code in parentheses (Eg. Retinal Examination (CPT: 92229))

**Example**:

```python
from canvas_workflow_kit.recommendation import PerformRecommendation
from canvas_workflow_kit.value_set.v2021 import Diabetes

class EyeExam(ValueSet):
    VALUE_SET_NAME = 'Remote Imaging Retinal Exam'
    CPT = {'92229' }

perform_recommendation = PerformRecommendation(
    key='RECOMMEND_PERFORM_EYE_EXAM',
    rank=1,
    button='Perform',
    patient=self.patient,
    procedure=EyeExam,
    condition=Diabetes,
    title='Perform retinal examination'
)

result = ProtocolResult()
result.add_recommendation(perform_recommendation)
result.add_narrative(perform_recommendation.narrative)
```

A Perform recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/0a3ff5a-recs_perform_card.png "recs_perform_card.png"){:width="50%"}

Upon pressing the _Perform_ button, the _Perform_ command will populate the patient's chart:

![](https://files.readme.io/f2be03e-Screen_Shot_2022-07-18_at_12.44.06_PM.png "Screen Shot 2022-07-18 at 12.44.06 PM.png"){:width="70%"}
<br>
<br>
* * *
## PlanRecommendation

**Description**: A recommendation specifying that a provider may need to document a Plan. A Plan Recommendation allows providers the ability to create a [Plan Command](https://canvas-medical.help.usepylon.com/articles/7699598664-command-plan) with the click of a button directly in a patient's chart.

**Parameters**:

| Name        | Type      | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------- | --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_  | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                                                                                                                                                                                         |
| `rank`      | _integer_ | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.                                                                                                                                                                                                                                                   |
| `button`    | _string_  | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                                                                                                                                                                                                                                                          |
| `patient`   | `Patient` | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                                                                                                                                                                                                                                                         |
| `title`     | _string_  | `false`  | The text to show on a patient's chart that describes the recommendation. If title is not passed in, it will default to "Make a plan".                                                                                                                                                                                                                                                                                               |
| `narrative` | _string_  | `false`  | The text that will populate the Plan command Note in the chart. For this to also display on the protocol card, the command `add_narrative(plan_recommendation.narrative) must be used. If title is not included, narrative will be set to "`Patient's name\` should have a plan." If title is included and narrative is not, when you click the plan button, you will get the error: “Something went wrong with this plan command”. |

**Note:**  
There is currently no change type for plan, nor is plan saved in the patient recordset. 

**Example**:

```python
from canvas_workflow_kit.recommendation import PlanRecommendation

plan_recommendation = PlanRecommendation(
    key='RECOMMEND_EXERCISE_PLAN',
    rank=1,
    button='Plan',
    patient=self.patient,
    title=f'Plan an Excercise Regimen with {self.patient.first_name}',
    narrative='Discuss daily goals for exercise'
)

result = ProtocolResult()
result.add_recommendation(plan_recommendation)
result.add_narrative(f'Discussing planning an exercise regimen with {self.patient.first_name}')
```

A Plan recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/4d9208b-recs_plan_card.png "recs_plan_card.png"){:width="50%"}

Upon pressing the _Plan_ button, the _Plan_ command will populate the patient's chart. The _narrative_ that was passed to the recommendation will populate the text in the command:

![](https://files.readme.io/af679df-recs_plan_chart.png "recs_plan_chart.png"){:width="70%"}
<br>
<br>
* * *
## PrescribeRecommendation

**Description**: A recommendation advising the provider to prescribe a treatment for a patient.

**Parameters**:

| Name           | Type       | Required | Description                                                                                                                                                                                  |
| -------------- | ---------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`          | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                  |
| `rank`         | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.            |
| `button`       | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                   |
| `patient`      | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                  |
| `prescription` | `ValueSet` | `true`   | A `ValueSet` for the recommended prescription.                                                                                                                                               |
| `title`        | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation.                                                                                                                     |
| `context`      | _dict_     | `true`   | A dictionary that may optionally includes sig, duration, dispense quantity, refill count conditions, and substitutions allowed. These will be used to populate the prescribe command.        |
| `narrative`    | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(prescribe_recommendation.narrative) must be used. |

**Notes:**

- The context contains several keys that will autofill the prescribe command:  
      - `sig_original_input`: a string that will autofill the sig field of the command.  
      - `duration_in_days`:  an integer that autofills the "days supply" field  
      - `dispense_quantity`:  an integer that autofills the "quantity to dispense" field  
      - `dosage_form`: a string that will autofill the unit on the quantity to dispense field  
      - `count_of_refills`: an integer that autofills the "refills" field  
      - `generic_substitutions_allowed`: a boolean that autofills the substitutions field as either "allowed" (True) or "Not Allowed" (False)  
      - `note_to_pharmacist`: a string that autofills the "Note to pharmacist" field  
      - `conditions`: a dictionary that contains the keys `code`, `system` and `display`. 
- The medication ValueSet class only requires an FDB code to look up the medication. Canvas will ignore all other codes in the ValueSet. However, if FDB is not provided and RXNORM is provided, the RXNORM code will be used to look up the medication.

```
class tylenolNDC(ValueSet):
    VALUE_SET_NAME = 'Tylenol Ex-Str 500 mg caplet'
    FDB = {206813}
    RXNORM = {'198440'}
```

It is important to note that the FDB code is not a string, whereas the RXNORM code is. If more than one code is entered, only the first coding will be ingested. 

- If a condition is included in the context that the patient is not diagnosed with, the command will insert without that condition in the indications field. This reflects the Canvas UI Behavior of not allowing a patient to be prescribed a drug with an indication not already in their chart.

**Example**:

```python
from canvas_workflow_kit.recommendation import PrescribeRecommendation

class tylenolNDC(ValueSet):
    FDB = {206813}


prescribe_recommendation = PrescribeRecommendation(
    key='RECOMMEND_TYLENOL_MEDICATION',
            rank=1,
            button='Prescribe',
            patient=self.patient,
            prescription=tylenolNDC,
            title='Recommendation of Tylenol.',
            context={
            'sig_original_input': "This is the sig" ,
            'duration_in_days': 5 ,
            'dispense_quantity': 45 ,
            'count_of_refills_allowed': 4 ,
            'dosage_form': "tablet",
            'generic_substitutions_allowed': False ,
            'note_to_pharmacist': "This is the note to pharmacist",
            'conditions': [[{ 
                'code': 'G43C1',
                'system': 'ICD-10',
                'display': "Headache Syndrome",
            }]]
            }
        )

result = ProtocolResult()
result.add_recommendation(prescribe_recommendation)
```

A Prescribe recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/de5a9e0-Screen_Shot_2022-08-05_at_6.40.15_PM.png "Screen Shot 2022-08-05 at 6.40.15 PM.png"){:width="50%"}

A Prescribe command will appear after clicking the prescribe button:

![](https://files.readme.io/3577c92-Screen_Shot_2022-08-05_at_6.40.05_PM.png "Screen Shot 2022-08-05 at 6.40.05 PM.png"){:width="70%"}
<br>
<br>
* * *
## ReferRecommendation

**Description**: A recommendation advising a provider to create a referral for a patient. A Refer Recommendation allows providers the ability to create an [Refer Command](https://canvas-medical.help.usepylon.com/articles/8339414277-command-referrals) with the click of a button directly in a patient's chart.

**Parameters**:

| Name        | Type       | Required | Description                                                                                                                                                                                       |
| ----------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_   | `true`   | A unique identifier for the recommendation.                                                                                                                                                       |
| `rank`      | _integer_  | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.                 |
| `button`    | _string_   | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                        |
| `patient`   | `Patient`  | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                       |
| `referral`  | `ValueSet` | `true`   | A `ValueSet` class for the referral. Only the name of the ValueSet will be used.                                                                                                                  |
| `condition` | `ValueSet` | `false`  | A `ValueSet` class for the condition associated with the reason for the referral. Only the name of the ValueSet will be used if title is not included.                                            |
| `title`     | _string_   | `false`  | The text to show on a patient's chart that describes the recommendation. If no title is included, it will default to "Refer `referral.name`".                                                     |
| `context`   | _dict_     | `false`  | A dictionary that may optionally store a string that stores the specialty name with the key 'specialties', as well as a dictionary that stores condition codes, stored with the key 'conditions'. |
| `narrative` | _string_   | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(refer_recommendation.narrative) must be used.          |

**Notes: **
- If no title is included, the narrative will also be autogenerated.  
      - If condition is included, the narrative will be set to "`patient.name` has `condition.name` and should be referred for `referral.name`".  
      - If condition is not included, the narrative will be set to "`patient.name` should be referred for `referral.name`"

- Currently when a `Refer` command is committed, it will not appear in the `self.patient` object. For a refer recommendation to be satisfied, a Specialist Consult Report must be attached to this patient using our [Data Integrations](https://canvas-medical.help.usepylon.com/articles/8618913529-data-integration-overview) feature with the document type set to "[Specialist Consult Report](https://canvas-medical.help.usepylon.com/articles/8163023191-data-integration-specialist-consult-reports)". The specialty should be set to the same name as what was inputted in the referral name. The report must then be reviewed by a practitioner through the patient's chart.  A Specialist Consult Report Template must exist that contains the coding for the refer ValueSet that is being recommended. 

- The referral command should autofill the "Refer to" title with the string that was passed in within context['specialties'], followed by "(TBD)". 

**Example**:

```python
from canvas_workflow_kit.recommendation import ReferRecommendation
from canvas_workflow_kit.value_set.v2021 import MalignantNeoplasmOfColon

class Colonoscopy(ValueSet):
    VALUE_SET_NAME = 'Colonoscopy'
    CPT = {'44388'}

refer_recommendation = ReferRecommendation(
            key='RECOMMEND_REFER_COLONOSCOPY',
            rank=1,
            button='Refer',
            patient=self.patient,
            referral=Colonoscopy,
            condition=MalignantNeoplasmOfColon,
            title='Refer for a Colonoscopy',
            context={
            'specialties': ['Colonoscopy'],
            'conditions': [[{
                'code': 'C186',
                'system': 'ICD-10',
                'display': "Malignant neoplasm of descending colon (C18.6)" ,
            }]]}
)

result = ProtocolResult()
result.add_recommendation(refer_recommendation)
```

A Refer recommendation will appear in the list of Protocols for applicable patients:
{:refdef: style="text-align: center;"}
![](https://files.readme.io/214d728-Screen_Shot_2022-08-05_at_6.57.10_PM.png "Screen Shot 2022-08-05 at 6.57.10 PM.png"){:width="50%"}
{: refdef}


A Refer command will appear after clicking the refer button:
{:refdef: style="text-align: center;"}
![](https://files.readme.io/aa5ce68-Screen_Shot_2022-08-05_at_6.57.00_PM.png "Screen Shot 2022-08-05 at 6.57.00 PM.png"){:width="70%"}
{: refdef}
<br>
<br>
* * *
## StructuredAssessmentRecommendation

**Description**: A recommendation specifying that one or more Structured Assessments should be completed for a patient.  A Structured Assess Recommendation allows providers the ability to create an [Structured Assessment command](https://canvas-medical.help.usepylon.com/articles/8805008571-command-structured-assessment) with the click of a button directly in a patient's chart.

**Parameters**:

| Name             | Type             | Required | Description                                                                                                                                                                                              |
| ---------------- | ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`            | _string_         | `true`   | A unique identifier for the recommendation.                                                                                                                                                              |
| `rank`           | _integer_        | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.                        |
| `button`         | _string_         | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                               |
| `patient`        | `Patient`        | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                              |
| `questionnaires` | `list[ValueSet]` | `true`   | A list of `ValueSet` classes for the structured questionnaire(s) associated with the Assessment. Although this attribute is a list, it will only ingest the first item.                                  |
| `title`          | _string_         | `false`  | The text to show on a patient's chart that describes the recommendation.  If a title is not included, the questionnaire ValueSet title is used, formatted as "Interview `questionnaire.name`".           |
| `narrative`      | _string_         | `false`  | The text to show on a patient's chart under the title of the recommendation. For this to successfully display, the command \`add_narrative(structured_assessment_recommendation.narrative) must be used. |

**Notes:**

- For this feature to work as expected, each assessment loaded into Canvas should have a unique coding. If two assessments share the same coding, the first item found in Canvas will be used. If two assessment codings are included in the ValueSet, the first item in the list will be used to autogenerate the Structured Assessment command. To learn more about importing structured assessments to canvas, see this [Zendesk article](https://canvas-medical.help.usepylon.com/articles/8805008571-command-structured-assessment). 

**Example**:

```python
from canvas_workflow_kit.recommendation import StructuredAssessmentRecommendation
from canvas_workflow_kit.value_set.value_set import ValueSet

class StructuredAssessmentQuestionnaireCOPD(ValueSet):
    VALUE_SET_NAME = 'COPD'
    INTERNAL = {'COPD_ASSESSMENT'}

structured_assessment_recommendation = StructuredAssessmentRecommendation(
    key='RECOMMEND_COPD_STRUCTURED_ASSESSMENT',
    rank=1,
    button='Assess',
    patient=self.patient,
    questionnaires=[StructuredAssessmentQuestionnaireCOPD],
    title='Assess COPD'
)

result = ProtocolResult()
result.add_recommendation(structured_assessment_recommendation)
result.add_narrative(f'{self.patient.first_name} is recommended to take a COPD Assessment')
```

An Assessment recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/901cc17-recs_struct_card.png "recs_struct_card.png"){:width="50%"}

Upon pressing the _Assess_ button, the _Structured Assessment_ command will populate the patient's chart:

![](https://files.readme.io/bce9ad2-recs_structure_chart_updated.png "recs_structure_chart_updated.png"){:width="70%"}
<br>
<br>
* * *
## TaskRecommendation

**Description**: A recommendation advising the provider to set up a task for another staff member. A provider can use the [Task command](https://canvas-medical.help.usepylon.com/articles/8460447495-task-management) to fulfill this recommendation.

**Parameters**:

| Name        | Type      | Required | Description                                                                                                                                                                         |
| ----------- | --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `patient`   | `Patient` | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                         |
| `key`       | _string_  | `true`   | A unique identifier for the recommendation.                                                                                                                                         |
| `rank`      | _integer_ | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top. |
| `title`     | _string_  | `true`   | The text to show on a patient's chart that describes the recommendation.                                                                                                            |
| `narrative` | _string_  | `true`   | A string that will be used as the internal comment for the task.                                                                                                                    |
| `context`   | _dict_    | `false`  | A dictionary that may contain keys 'due_date' and 'labels'. Due date stores a string in the format "YYYY-MM-DD" and labels is a list of strings                                     |

**Example**:

```python
from canvas_workflow_kit.recommendation import TaskRecommendation

task_recommendation = TaskRecommendation(
    patient=self.patient,
    key='TASK_MEDICATION_RECONCILIATION',
    rank=1,
    button='Task',
    title='Medication Reconciliation Task',
    context={
            'labels':['Urgent'],
            'due_date':'2022-07-31'
    },
    narrative="Patient medications should be reviewed for safety measures."
)

result = ProtocolResult()
result.add_recommendation(task_recommendation)
```

A Task recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/7613698-Screen_Shot_2022-07-22_at_9.50.48_AM.png "Screen Shot 2022-07-22 at 9.50.48 AM.png"){:width="50%"}

Once the task button is selected, it will generate a task command that has been autofilled: 

![](https://files.readme.io/c9ef318-Screen_Shot_2022-07-22_at_9.53.38_AM.png "Screen Shot 2022-07-22 at 9.53.38 AM.png"){:width="70%"}
<br>
<br>
* * *
## VitalSignRecommendation

**Description**: A recommendation specifying a vital sign reading should be taken. This recommendation can be fulfilled with the [Vitals command](https://canvas-medical.help.usepylon.com/articles/9426091672-command-vitals).

**Parameters**:

| Name        | Type      | Required | Description                                                                                                                                                                                                                                                                                                                                                            |
| ----------- | --------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `key`       | _string_  | `true`   | A unique identifier for the recommendation.                                                                                                                                                                                                                                                                                                                            |
| `rank`      | _integer_ | `true`   | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower _rank_ values will appear at the top.                                                                                                                                                                                    |
| `button`    | _string_  | `true`   | The text that will appear on the button next to a Protocol recommendation.                                                                                                                                                                                                                                                                                             |
| `patient`   | `Patient` | `true`   | An instance of a `Patient`. This should always be passed as `self.patient`.                                                                                                                                                                                                                                                                                            |
| `title`     | _string_  | `false`  | The text to show on a patient's chart that describes the recommendation. If title is not included it will default to "Collect Vitals".                                                                                                                                                                                                                                 |
| `narrative` | _string_  | `false`  | Text that may optionally be used to add to a recommendation under the title and protocol type. It will not display unless the code `result.add_narrative(vital_sign_recommendation.narrative)` is used.  If a title is omitted, the narrative will be set to "`Patient.name` should have vital signs collected." regardless of if narrative has already been assigned. |

**Example**:

```python
from canvas_workflow_kit.recommendation import VitalSignRecommendation

vital_sign_recommendation = VitalSignRecommendation(
    key='RECOMMEND_VITAL_SIGN_READING',
    rank=1,
    button='Vitals',
    patient=self.patient,
    title='Recommend Reading Vital Signs'
    narrative=f'{self.patient.first_name} should have their vitals recorded at the beginning of their upcoming appointment.'
)

result = ProtocolResult()
result.add_recommendation(vital_sign_recommendation)
```

A Vital Sign recommendation will appear in the list of Protocols for applicable patients:

![](https://files.readme.io/6ec6c69-Screen_Shot_2022-07-22_at_11.29.30_AM.png "Screen Shot 2022-07-22 at 11.29.30 AM.png"){:width="50%"}

A vitals command will be generated upon clicking the vitals button:

![](https://files.readme.io/c7d7c5c-Screen_Shot_2022-07-22_at_11.30.31_AM.png "Screen Shot 2022-07-22 at 11.30.31 AM.png"){:width="70%"}
