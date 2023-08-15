---
title: "Adding More Functionality to a Protocol"
slug: "sdk-adding-more-functionality-to-a-protocol"
hidden: false
createdAt: "2022-02-08T21:29:57.074Z"
updatedAt: "2023-01-12T21:33:42.160Z"
---
## Expanding a Protocol

Building on our [previous example](doc:sdk-create-a-protocol), we will now explore how to create logic to tell if a patient has or has not satisfied the requirements for fulfilling a Protocol. This is important in order to only display Protocol alerts for those that have not been satisfied. Conversely, we also want to display information about the Protocol under the _Inactive_ status if it indeed has been satisfied.

To help visualize this, let's say that we want to develop a Protocol for all patients 65 and older to be interviewed in order to screen their risk of falling. Patients who are eligible for this Protocol should be interviewed once a year.

As an example, a new patient, _John Smith_, is over 65 and thus would be due for our Fall Screening Protocol. Here is how the Protocol is displayed in John's chart when he arrives for his first appointment:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ca476a8-fall_screening_protocol_in_chart.png",
        "fall_screening_protocol_in_chart.png",
        504,
        281,
        "#f1f1f1"
      ]
    }
  ]
}
[/block]
As recommended, John's physician can then complete the Fall Questionnaire in his chart:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e4d8fa2-fall_screening_questionnaire.png",
        "fall_screening_questionnaire.png",
        720,
        185,
        "#f5f5f5"
      ]
    }
  ]
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "Questionnaires",
  "body": "_For more information on creating Questionnaires in Canvas, see [Creating a New Questionnaire](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire)._"
}
[/block]
Once the recommended Fall Screening Questionnaire has been completed, the Protocol is considered to have been satisfied. It is now moved to the _Inactive_ tab in John's chart:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8c9f063-fall_screening_satisfied.png",
        "fall_screening_satisfied.png",
        504,
        342,
        "#f0f0f0"
      ]
    }
  ]
}
[/block]
### The `in_numerator` and `in_denominator` Methods

In the context of our custom Protocol code, we want to be able to tell whether a patient such as John has completed the requirements to satisfy a Protocol, such as the completion of the Fall Screening Questionnaire. This can be done by using the `in_numerator` and `in_denominator` methods. The results of these methods can then be used with logic within `compute_results`.

Using our example above, the `in_denominator` method can be used to see if John exists in the population of patients that should receive the screening. The Fall Screening applies to all patients 65 or older, so our code for this method should look like this:

```python
def in_denominator(self):
    return self.patient.age_at(self.now) >= 65
```

Now let's compute whether or not John has already satisfied this Protocol. Since we saw above that the Fall Screening Protocol is satisfied after completion of the Fall Screening Questionnaire, we can see if John has fulfilled this requirement within the `in_numerator` method. First, import the relevant screening object from the Canvas Workflow Kit (we'll go into more detail about these shortly):

```python
from canvas_workflow_kit.value_set.v2021 import FallsScreening
from canvas_workflow_kit.timeframe import Timeframe
```

```python
def in_numerator(self):
    last_screening_timeframe = Timeframe(self.now.shift(years=-1), self.now)
    falls_screening = self.patient.interviews.find(
        FallsScreening
    ).within(last_screening_timeframe)
    return bool(falls_screening)
```

The methods above will tell us two things about our patient John:

1. The `in_denominator` method will tell us if John is an applicable candidate for this Protocol. Since he is in the 65 or older age bracket, this will return `True`.
2. The `in_numerator` method will tell us if John has completed the Fall Screening Questionnaire within the last year. Since he has, this will also return True.

### Incorporating Logic into `compute_results`

We can now use the logic from both of these methods in `compute_results`:

```python
    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator(): # Patient is 65 or older
            if self.in_numerator(): # Has completed the Screening
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    f'{self.patient.first_name} has been screened for fall risk in the past year.'
                )
            else: # Has not completed the Screening
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_recommendation(
                    InterviewRecommendation(
                        key='CMS139v9_INTERVIEW_RECOMMENDATION',
                        rank=1,
                        button='Interview',
                        patient=self.patient,
                        questionnaires=[FallsScreening],
                        title=f'Complete the Fall Screening Questionnaire',
                    )
                )
        return result
```

As you can see above, we marked the Status as `STATUS_DUE` for when John had not completed the Questionnaire, as well as a recommendation to do so. After John had completed the Questionnaire, a status of `STATUS_SATISFIED` was set.

### A Complete Example

Here is the complete example of the Protocol for the example above:

```python
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_DUE,
    STATUS_SATISFIED,
)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import InterviewRecommendation


from canvas_workflow_kit.value_set.v2021 import (
    FallsScreening
)
from canvas_workflow_kit.timeframe import Timeframe


class SeniorFallProtocol(ClinicalQualityMeasure):

    class Meta:

        title = 'Preventive Care and Screening: Fall Screening'

        description = 'Fall Screening for Patients 65 and older'

        version = '2022-02-01v7'

        information = 'https://ecqi.healthit.gov/ecqm/ep/2021/cms139v9'

        identifiers = ['CMS139v9']

        types = ['CQM']

        compute_on_change_types = [
            CHANGE_TYPE.CONDITION,
            CHANGE_TYPE.PATIENT,
        ]

        references = [
            'Falls: Screening for Future Fall Risk https://ecqi.healthit.gov/ecqm/ep/2021/cms139v9'
        ]

    def in_denominator(self):
        """
        Patients in the initial population.
        """
        return self.patient.age_at(self.now) >= 65

    def in_numerator(self):
        last_screening_timeframe = Timeframe(self.now.shift(years=-1), self.now)
        falls_screening = self.patient.interviews.find(
            FallsScreening
        ).within(last_screening_timeframe)
        return bool(falls_screening)

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator(): # Patient is 65 or older
            if self.in_numerator(): # Has completed the Screening
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    f'{self.patient.first_name} has been screened for fall risk in the past year.'
                )
            else: # Has not completed the Screening
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_recommendation(
                    InterviewRecommendation(
                        key='CMS139v9_INTERVIEW_RECOMMENDATION',
                        rank=1,
                        button='Interview',
                        patient=self.patient,
                        questionnaires=[FallsScreening],
                        title=f'Complete the Fall Screening Questionnaire',
                    )
                )
        return result
```

### Recommendations and Next Steps

You may have noticed that instead of using a generic `Recommendation` in our `add_recommendation` method, we used an `InterviewRecommendation`. The SDK includes a number of recommendation classes, which we you can explore in the [Canvas SDK Recommendation Types doc](doc:recommendationtypes)