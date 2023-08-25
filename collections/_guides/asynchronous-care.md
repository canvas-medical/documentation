---
title: "Asynchronous Care"
guide_for: 
---

Async care can happen in various ways, and while it’s not a new model of care delivery, it has become increasingly popular in recent years, especially since the start of the Covid-19 pandemic. The guide below outlines how you can surface patient completed questionnaires for review by your care team. It also offers suggestions on how you can leverage the structured data collected to surface recommendations based on your care model.
<br> 

* * *
## What you'll learn
In this guide, you will learn how to address asynchronous patient requests by completing the following steps
1. Write patient collected data using Questionnaires
2. Write tasks to create a worklist in Canvas
3. Surface recommendations based on Questionnaire responses
<br>
<br>

* * *

### 1. Write patient collected data using Questionnaires

In order to evaluate a patient asynchronously, you will need to collect all of the necessary inputs (histories, symptoms, preferences, etc.) so that your clinicians have the full picture when making treatment decisions. Some of the data may map to our existing write endpoints and anything that may not fit elsewhere can be added through a Questionnaire. Questionnaires are a great way to extend the Canvas data model as they are fully configurable and designed to be code-backed.

<b>I. Super Users 🦸:</b> Once you design and finalize the your intake forms, you will need to build and upload them as Questionnaires in Canvas. Follow [these instructions]({{site.baseurl}}/documentation/questionnaires/) to do so. <br><br>
<b>II. Developers 👨‍💻:</b> Canvas does not offer a patient experience for completing Questionnaires. You will need to extend Canvas by building the patient facing front end (or leveraging a partner to build it for you). Once the data has been captured within your workflow, you can leverage our [FHIR QuestionnaireResponse Create endpoint]({{site.baseurl}}/api/questionnaireresponse/)to surface the responses in Canvas. Without specificying an Encounter reference, the completed Questionnaire Command will be added to a Data Import Note in the patient's Timeline. 

{% include alert.html type="info" content="Data Import notes are automatically locked and cannot be updated by your clinicians in the application. Any associated documentation will need to be added in a new Note." %}


{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/data-import.png){:width="100%"}
{: refdef}
<br>

* * *


### 2. Write tasks to create a worklist in Canvas

The task panel is a great tool to organize work to be done. After your patients complete your online intake forms, you can leverage Tasks in Canvas to alert your team that they are ready for review.

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/work-queue.png){:width="95%"}
{: refdef}
<br>
<b>I. Super Users 🦸:</b> You will need to configure Teams and Task Labels in Canvas. 

 - [Teams]({{site.baseurl}}/documentation/teams/) are intended to group work. You may want to group specialty providers together ( `Dermatology Providers`), or set up teams that support certain times of the day (`After Hours Support`). 
 - [Task Labels]({{site.baseurl}}/documentation/task-labels/) are meant to help organize tasks and are helpful as filters within the task panel. You may need to indicate that a patient should be treated as priority and a label would be a way to do that.

<b>II. Developers 👨‍💻: </b> You can assign tasks to both indivduals and/or team, and assign labels using the [FHIR Task Create and Update]({{site.baseurl}}/api/task/) endpoints. 

- If assigning to an individual, add a practitiioner reference in the owner attribute. 
- Teams are mapped to the FHIR Group resource. Assign the Task to a Team using the Task group extension. Use the [FHIR Group Search]({{site.baseurl}}/api/group/) to find the necessary group ID. 
- Labels do not have to exist in your admin settings in order to be added through the API, however, the custom colors will only show if they have been assigned in admin. 

<b>III. Super Users 🦸</b> After the tasks have been created in Canvas, use the filters to create your worklists. You can bookmark the filtered views to save them. The page default will show tasks assigned to `Me or my teams`. The tasks assigned to your teams only show if they are not also assigned to an individual (unclaimed). If a new task comes in, you can assign it to yourself to claim it, removing it from the view of others. 


<br>
* * *

### 3. Surface recommendations based on Questionnaire responses
Async workflows may need to support a high volume of patients. Protocols are a great way to surface best practice recommendations to your treating providers so that they can work through their queues efficiently. 

<b>I. Super Users 🦸:</b> Use the framework below to define how your questionnaire responses should drive recommendations. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/protocol-framework.png){:width="60%"}
{: refdef}

An example of this would be building a protocol that surfaces relevant oral contraceptive options after a patient submits a questionnaire indicating their preference for skipping their cycles. The protocol can include prefilled commands as suggestions, making it easy for the clinican to follow care guidelines and quickly add orders or documentation to their note. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/bc-recommendation.png){:width="100%"}
{: refdef}
<br>
<br>
<b>II. Developers 👨‍💻: </b> The interview [change type]({{site.baseurl}}/sdk/change-types/) allows you to recompute a protocol after a questionnaire is recorded (either in the UI or through the API). This protocol recommends diagnosing certain conditions based on questionnaire responses, and the recommendations have one-click commands for inserting the conditions into a Canvas note. 

{% include alert.html type="info" content= "This protocol is dependent on a Questionnaire called the Diagnostic Assessment Tool with specific codings for the questionnaire and each of its questions - the loader data for this Questionnaire is below." %}

``` python
from canvas_workflow_kit import events
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.protocol import (STATUS_DUE, STATUS_SATISFIED,
                                          ClinicalQualityMeasure,
                                          ProtocolResult)
from canvas_workflow_kit.recommendation import Recommendation
from canvas_workflow_kit.value_set.value_set import ValueSet
"""
This protocol recommends diagnosing certain conditions based on questionnaire responses, 
and the recommendations have one-click commands for inserting the conditions into a Canvas note.
This is also dependent on a Questionnaire called the Diagnostic Assessment Tool with specific 
codings for the questionnaire and each of its questions - the loader data for this Questionnaire is below.
"""


class DiagnosticAssessmentQuestionnaire(ValueSet):
    VALUE_SET_NAME = 'Diagnostic Assessment Questionnaire'
    INTERNAL = {'PAT.QUESTIONNAIRE.2'}


class SenilePurpura(ValueSet):
    VALUE_SET_NAME = 'Senile purpura'
    ICD10CM = {'D692'}
    INTERNAL = {'PAT.QUES.8'}


class AhteroscleroticHeartDisease(ValueSet):
    VALUE_SET_NAME = ('Atherosclerotic heart disease of native coronary'
                      'artery with unspecified angina pectoris')
    ICD10CM = {'I25119'}
    INTERNAL = {'PAT.QUES.9'}


class AlcoholDependence(ValueSet):
    VALUE_SET_NAME = 'Alcohol dependence, in remission'
    ICD10CM = {'F1021'}
    INTERNAL = {'PAT.QUES.10'}


class MajorDepressiveDisorder(ValueSet):
    VALUE_SET_NAME = 'Major depressive disorder, single episode, in remission'
    ICD10CM = {'F325'}
    INTERNAL = {'PAT.QUES.11'}


class DiagnosticAssessment(ClinicalQualityMeasure):
    """
    A protocol that recommends diagnosing certain conditions based on questionnaire responses.
    """

    class Meta:

        title = 'Diagnostic Assessment'

        version = 'v1.0.0'

        description = ('A protocol that recommends diagnosing'
                       'certain conditions based on questionnaire responses.')

        information = 'https://canvasmedical.com/'

        identifiers = ['DiagnosticAssessment']

        types = ['Tools']

        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]
        compute_on_change_types = [
            CHANGE_TYPE.INTERVIEW, CHANGE_TYPE.CONDITION
        ]

        authors = ['Canvas Medical']

        references = ['Canvas Medical']

        funding_source = ''

    most_recent_interview = None
    positive_question_ids = set()
    conditions_to_diagnose = []

    def in_denominator(self):
        """
        Patients whose most recent Diagnostic Assessment Tool questionnaire
        has at least one "Yes" answer.
        """
        # identify all active diagnostic assessment questionnaires for the patient
        # (use the DiagnosticAssessmentQuestionnaire valueset)
        diagnostic_interviews = self.patient.interviews.find(
            DiagnosticAssessmentQuestionnaire).filter(status='AC')

        # if none, return False
        if len(diagnostic_interviews) == 0:
            return False

        # get the most recently completed diagnostic assessment questionnaire by 'created'
        most_recent = max(diagnostic_interviews, key=lambda x: x['created'])
        self.most_recent_interview = most_recent

        # determine which question_ids had a 'yes' response
        positive_question_ids = {
            response['questionResponseId']
            for response in most_recent['responses']
            if response['value'] == 'Yes'
        }
        self.positive_question_ids = positive_question_ids

        # return True if the length of question_ids > 0, otherwise False
        return len(positive_question_ids) > 0

    def in_numerator(self):
        """
        Patients that have already been diagnosed with all recommended conditions.
        """
        # create a set of the codes for positive questions
        questions = self.most_recent_interview['questions']
        positive_question_codes = {
            q['code']
            for q in questions
            if q['questionResponseId'] in self.positive_question_ids
        }

        # map over each value_set and determine (1) if it is associated with any of the
        # positive_question_codes, and (2) if the patient has not been diagnosed with it yet.
        # if both are true, recommend diagnosis

        def value_set_is_positive(value_set):
            value_set_code = list(value_set.values['internal'])[0]
            return value_set_code and value_set_code in positive_question_codes

        def patient_has_condition(value_set):
            return len(
                self.patient.conditions.find(value_set).filter(
                    clinicalStatus='active')) > 0

        def patient_should_be_diagnosed(value_set):
            return value_set_is_positive(
                value_set) and not patient_has_condition(value_set)

        value_sets = [
            SenilePurpura, AhteroscleroticHeartDisease, AlcoholDependence,
            MajorDepressiveDisorder
        ]
        conditions_to_diagnose = [
            v for v in value_sets if patient_should_be_diagnosed(v)
        ]
        self.conditions_to_diagnose = conditions_to_diagnose

        return len(conditions_to_diagnose) == 0

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator():
            if self.in_numerator():
                result.status = STATUS_SATISFIED
            else:
                result.due_in = -1
                result.status = STATUS_DUE
                result.add_narrative(
                    f'{self.patient.first_name} responded "Yes" to '
                    f'{len(self.conditions_to_diagnose)} questions in the Diagnostic Assessment '
                    f'Questionnaire, but has not been diagnosed with the associated conditions. '
                    f'Consider updating the Conditions List as clinically appropriate'
                )
                for i, vs in enumerate(self.conditions_to_diagnose):
                    result.add_recommendation(
                        Recommendation(
                            key=
                            f'DiagnosticAssessmentProtocol_RECOMMEND_DIAGNOSE_{vs.name}',
                            rank=i + 1,
                            button='Diagnose',
                            title=vs.name,
                            narrative=result.narrative,
                            command={
                                'type': 'diagnose',
                                'filter': {
                                    'coding': [{
                                        'code':
                                        list(vs.values['icd10cm']),
                                        'system':
                                        'icd10cm'
                                    }]
                                }
                            }))
        return result
```
<br>
Use the following information to add this Quesionnaire to your environment using the Questionnaire Loader in the settings menu:<br><br>
<b> Google Sheet ID or URL:</b> https://docs.google.com/spreadsheets/d/1T58Bor8vHLs5KT3V23qvG8Yx7jvS1QbTlnatCh92pF8/edit#gid=0<br>
<b> Google Sheet tab name:</b> QUES-DAT<br>

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRO5_7TTc7t5GndMjVe6fDCrXil2kKeV9800HB9fzfQlT57HDiQgZ9c0ZtByuLpqhlocphhLh0Yt1IR/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false" width="100%" height="400px"></iframe>




