---
title: "Build a Safety Framework"
guide_for:
---

Healthcare has come a long way since the US Institute of Medicine published its landmark To Err is Human report in 1999. While patients are safer, practicing evidence-based medicine is often still too hard. Canvas was designed to leverage data to better inform your workflows. 
<br>
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Suggest an alternative intervention
2. Track performance and outcomes
<br>
<br>

* * *


### 1. Suggest an alternative interventions

Our Workflow Kit allows you to program complex clinical logic into the point of care. Recommendations, presented as either protocol cards or banners, allow you to implement evidence-based-care in your clinical workflows. Possible use cases include recommending interventions with less side effects, suggesting preferred internal programs or partners that deliver better outcomes, or alerting providers to possible contraindications. 

You can leverage the framework below to help build these workflow helpers into the platform. Make sure to reference what change types, data, and interventions are available to support your custom protocols. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/protocol-framework.png){:width="60%"}
{: refdef}

The example below surfaces a recommendation to switch a patient’s schizophrenia medication from Olanzapine to Ziprasidone if diabetes is added to the condition list.
{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/alternative-med.png){:width="60%"}
{: refdef}

To ensure your clinicians have the appropriate context, you can use the narrative to provide background and then surface the relevant studies or guidelines in the info button. 
<br>

```python
from canvas_workflow_kit.protocol import (ClinicalQualityMeasure,
                                          ProtocolResult, STATUS_DUE,
                                          STATUS_SATISFIED)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import PrescribeRecommendation
from canvas_workflow_kit.value_set.value_set import ValueSet

from canvas_workflow_kit.value_set.v2021 import Diabetes


class ZiprasidoneNewRx(ValueSet):
    VALUE_SET_NAME = 'ziprasidone 20 mg capsule'
    FDB = {'222887'}

class ZiprasidoneMed(ValueSet):
    VALUE_SET_NAME = 'Ziprasidone'
    RXNORM = {
        '314286', # ziprasidone 20 mg capsule / Geodon 20 mg capsule
        '313776', # ziprasidone 40 mg capsule / Geodon 40 mg capsule
        '313777', # ziprasidone 60 mg capsule / Geodon 60 mg capsule
        '313778', # ziprasidone 80 mg capsule / Geodon 80 mg capsule
    }

class Olanzapine(ValueSet):
    VALUE_SET_NAME = 'Olanzapine'
    RXNORM = {
        '314154', # olanzapine 10 mg tablet / Zyprexa 10 mg tablet
        '312078', # olanzapine 5 mg tablet / Zyprexa 5 mg tablet
        '283639', # olanzapine 20 mg tablet / Zyprexa 20 mg tablet
    }

class ZiprasidoneRx(ClinicalQualityMeasure):
    """
    A protocol with a prescribe button recommendation that inserts a
    completed prescribe command
    """

    class Meta:
        title = 'Ziprasidone recommendation'
        version = 'v1.0.0'
        description = 'If a patient on olanzapine has diabetes, recommend ziprasidone'
        compute_on_change_types = [
            CHANGE_TYPE.MEDICATION, CHANGE_TYPE.CONDITION
        ]
        types = ['Safety Recommendation']

    diabetes = None

    def in_denominator(self):
        """
        Return True if patient has an active Diabetes condition and an active Olanzapine medication
        If either are not active, return False
        """
        diabetes_conditions = self.patient.conditions.find(Diabetes).filter(
            clinicalStatus='active')

        if not diabetes_conditions:
            return False

        active_olanzapine = self.patient.medications.find(Olanzapine).filter(status='active')

        if not len(active_olanzapine):
            return False

        self.diabetes = diabetes_conditions[0]
        return True

    def in_numerator(self):
        """
        Return True if patient already has an active ziprasidone medication
        """
        return len(
            self.patient.medications.find(ZiprasidoneMed).filter(status='active')) > 0

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator():
            if self.in_numerator():
                result.status = STATUS_SATISFIED
            else:
                result.due_in = -1
                result.status = STATUS_DUE
                result.add_narrative(
                    'Ziprasidone may be preferred to Olanzapine in patients with diabetes.')
                prescribe_recommendation = PrescribeRecommendation(
                    key='RECOMMEND_ZIPRASIDONE',
                    rank=1,
                    button='Prescribe',
                    patient=self.patient,
                    prescription=ZiprasidoneNewRx,
                    title='Ziprasidone 20 mg tablet',
                    narrative=result.narrative,
                    context={
                        'conditions': [[
                            coding for coding in self.diabetes['coding']
                            if coding['system'] == 'ICD-10'
                        ]],
                        'dosage_form': 'capsule',
                        'sig_original_input': '1 tab by mouth twice per day',
                        'duration_in_days': 30,
                        'dispense_quantity': 60,
                        'count_of_refills_allowed': 2,
                        'generic_substitutions_allowed': True,
                        'note_to_pharmacist': ''
                    }
                )
                result.add_recommendation(prescribe_recommendation)

        return result
```



<br><br>
* * *
### 2. Track Performance and Outcomes
An essential aspect of preventing medical errors and improving patient safety is using data effectively to understand, track and communicate performance on patient safety metrics. 
<br><br>
You can leverage your read-only replica to report on outcomes and iterate on your Care Model.  