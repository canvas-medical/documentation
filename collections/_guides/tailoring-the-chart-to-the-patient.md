---
title: "Tailoring the Chart to the Patient"
guide_for:
- /sdk/layout-effect/
---

Different patients have different needs, and your tools should reflect that.
EMRs are able to be used in a wide variety of scenarios. In order to be able to
do just about anything, your EMR is packed to the gills with features and
options. While you might need all of these features for all of your patients,
you almost certainly don't need _every_ feature for _each_ of your patients.

This guide shows a few examples of using a patient's data to customize their
chart so the EMR features most relevant to them are front-and-center, while
minimizing or hiding what you don't need in the moment. Tailoring the
interface based on the patient in front of you creates a focused environment
for you to deliver care without irrelevant options getting between you and
your patient.

{% include alert.html type="info" content="This guide assumes pre-existing
knowledge of the Canvas SDK. If you're starting from scratch, you may want to
read and implement <a href='/guides/your-first-plugin/'>Your First Plugin</a> before
working through this exercise." %}


## Chart Customizations for Pediatric Patients

We will make two simple changes to the charting interface when the selected
patient is a child:

1. Move the Immunization list to the top of the patient summary
2. Prevent adult-only diagnosis choices from appearing in searches

First, we'll need to initialize a new plugin.

The Canvas CLI gives you a great head start when creating a plugin. Simply
run `canvas init`, and answer the prompt to name your plugin.

```
$ canvas init
  [1/1] project_name (My Cool Plugin): Pediatric Patient Chart Customizations
Project created in /Users/andrew/src/canvas-plugins/pediatric_patient_chart_customizations
```

This output shows the location of our freshly generated plugin. In this
directory, you'll see a default class (`protocols/my_protocol.py`) provided as a starting point for your
code.

```
$ tree pediatric_patient_chart_customizations/
pediatric_patient_chart_customizations/
├── CANVAS_MANIFEST.json
├── README.md
└── protocols
    ├── __init__.py
    └── my_protocol.py

2 directories, 4 files
```

You can use this file as a starting point, or you can start fresh with a new
file. At minimum, I recommend renaming `my_protocol.py` to something more
descriptive, and you'll need to update the references to the file in
`CANVAS_MANIFEST.json` as well.

### Move Immunizations to the Top of the Patient Summary

I've created a new file, `protocols/pediatric_chart_layout.py`, and I've
updated my `CANVAS_MANIFEST.json` to reflect it.

```
$ tree pediatric_patient_chart_customizations/
pediatric_patient_chart_customizations/
├── CANVAS_MANIFEST.json
├── README.md
└── protocols
    ├── __init__.py
    └── pediatric_chart_layout.py

2 directories, 4 files
```

Here is a pretty empty class with some comments that will guide our
development:

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class PediatricChartLayout(BaseHandler):
    """
    This event handler rearranges the patient summary section to focus on the
    parts most relevant to pediatric patients when it detects that the patient
    for the current chart is <= 17 years old.
    """

    # This event fires when a patient chart's summary section is loading.
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)

    def compute(self):
        """
        Check to see if the patient is <= 17 years old. If so, move their
        immunization list to the top of the patient summary.
        """

        # Look up the patient whose chart is being loaded right now

        # See if the patient is younger than 18 years old
        
        # If they are not younger than 18, do nothing
        
        # If they are younger than 18, re-arrange the layout of their summary
        # sections to put immunizations at the top.

        # BaseHandler subclasses must return a list, but it can be empty. It
        # is empty here since we aren't doing anything just yet.
        return []
```

Pretty straightforward logic. Do nothing or do something based on their age.

#### Looking Up the Patient

In order to determine if we are on a pediatric chart, we'll need to know the
patient and their birth date. We can use the
[Patient class](/sdk/data-patient/) in the [Data Module](/sdk/data/) for this.

The `PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION` event is accompanied by the
id of the patient whose chart is being loaded. You can find it using
`self.target`. The patient is the target of the event.

```python
import arrow

from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.patient import Patient


class PediatricChartLayout(BaseHandler):
    """
    This event handler rearranges the patient summary section to focus on the
    parts most relevant to pediatric patients when it detects that the patient
    for the current chart is <= 17 years old.
    """

    # This event fires when a patient chart's summary section is loading.
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)

    def compute(self):
        """
        Check to see if the patient is <= 17 years old. If so, move their
        immunization list to the top of the patient summary.
        """

        eighteen_years_ago = arrow.now().shift(years=-18).date().isoformat()
        patient_is_pediatric = Patient.objects.filter(
            id=self.target, birth_date__gt=eighteen_years_ago).exists()

        # If the patient is not pediatric, do not alter the layout.
        if not patient_is_pediatric:
            return []

        # TODO: Alter the layout
        return []
```

In the code above, you'll see I didn't actually retrieve the patient's
information. Since I don't plan to use any of the data from the patient
record, I instead let the database answer the question: "Does the patient with
this id have a birth date more recent than 18 years ago?" This is a
performance optimization. The less data transmitted, the faster your plugins
execute, and the faster your charts load. This is not strictly necessary, but
over time and with enough plugins installed the inefficiencies could add up.
If you'd like you could alternately retrieve the patient and make a direct
comparison to their `birth_date` attribute.


#### Altering the Layout

When loading the patient's summary, the front-end consults a list of sections
to retrieve data for and render. Our plugin influences this list, and it does
so using the [`PatientChartSummaryConfiguration`](https://github.com/canvas-medical/canvas-plugins/blob/main/canvas_sdk/effects/patient_chart_summary_configuration.py) effect.
Using the list of possible sections, we construct the ordered list of sections
we want to see. In this example we're just moving one to the top, but you
could also omit sections to hide them entirely if there are sections you do
not use or need for your [Care Model](https://www.canvasmedical.com/articles/care-modeling-the-secret-to-success-in-care-delivery).

```python
import arrow

from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.effects.patient_chart_summary_configuration import PatientChartSummaryConfiguration
from canvas_sdk.v1.data.patient import Patient


class PediatricChartLayout(BaseHandler):
    """
    This event handler rearranges the patient summary section to focus on the
    parts most relevant to pediatric patients when it detects that the patient
    for the current chart is <= 17 years old.
    """

    # This event fires when a patient chart's summary section is loading.
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION)

    def compute(self):
        """
        Check to see if the patient is <= 17 years old. If so, move their
        immunization list to the top of the patient summary.
        """

        eighteen_years_ago = arrow.now().shift(years=-18).date().isoformat()
        patient_is_pediatric = Patient.objects.filter(
            id=self.target, birth_date__gt=eighteen_years_ago).exists()

        # If the patient is not pediatric, do not alter the layout.
        if not patient_is_pediatric:
            return []

        layout = PatientChartSummaryConfiguration(sections=[
          PatientChartSummaryConfiguration.Section.IMMUNIZATIONS,
          PatientChartSummaryConfiguration.Section.SOCIAL_DETERMINANTS,
          PatientChartSummaryConfiguration.Section.GOALS,
          PatientChartSummaryConfiguration.Section.CONDITIONS,
          PatientChartSummaryConfiguration.Section.MEDICATIONS,
          PatientChartSummaryConfiguration.Section.ALLERGIES,
          PatientChartSummaryConfiguration.Section.CARE_TEAMS,
          PatientChartSummaryConfiguration.Section.VITALS,
          PatientChartSummaryConfiguration.Section.SURGICAL_HISTORY,
          PatientChartSummaryConfiguration.Section.FAMILY_HISTORY,
        ])

        return [layout.apply()]
```

Once installed, pediatric patients will have their immunization section at the
top of their summary, while adult patients will continue to have social
determinants as their initial section.

### Prevent adult-only diagnosis choices from appearing in searches

Some diagnosis codes are restricted to adult patients. CMS provides a [list](https://www.cms.gov/Medicare/Coding/OutpatientCodeEdit/Downloads/ICD-10-IOCE-Code-Lists.pdf)
of these "Adult Diagnoses". We can reference this list and filter them out of
the diagnosis search results for pediatric patients. This increases the
quality of your search and makes it easier for you to find the right choice.

I've created a new file, `protocols/pediatric_condition_search.py`, and I've
updated my `CANVAS_MANIFEST.json` to reflect it.

Here's the updated plugin file structure:

```
$ tree pediatric_patient_chart_customizations/
pediatric_patient_chart_customizations/
├── CANVAS_MANIFEST.json
├── README.md
└── protocols
    ├── __init__.py
    ├── pediatric_chart_layout.py
    └── pediatric_condition_search.py

2 directories, 5 files
```

And here's the updated `CANVAS_MANIFEST.json`:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "pediatric_patient_chart_customizations",
    "description": "Customizations for pediatric patients",
    "components": {
        "protocols": [
            {
                "class": "pediatric_patient_chart_customizations.protocols.pediatric_chart_layout:PediatricChartLayout",
                "description": "Moves the immunization section to the top of the patient summary on pediatric charts.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            },
            {
                "class": "pediatric_patient_chart_customizations.protocols.pediatric_condition_search:PediatricConditionSearch",
                "description": "Filters the condition search to eliminate adult-only conditions on pediatric charts.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

And here's the very basic outline we'll start out with:

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler

ADULT_ONLY_ICD_CODES = {
    # There are many, many more. Limiting this example for brevity.
    # ...
    "Z561",   # Change of job
    "Z5682",  # Military deployment status
    # ...
}


class PediatricConditionSearch(BaseHandler):
    """
    Filter condition searches for pediatric patients.
    """

    RESPONDS_TO = [
        EventType.Name(EventType.DIAGNOSE__DIAGNOSE__POST_SEARCH),
        EventType.Name(EventType.MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH),
    ]

    def compute(self):
        """
        Remove condition search results representing codings that are resevered
        for adults if the patient is <= 15 years old.
        """

        # This event's target is the command we are searching within. Look up
        # the patient id from the command, and use that to look up the patient.

        # If the patient is not pediatric, do not alter the search.

        # If the patient is pediatric, loop through the search results, and
        # compare the codings of the options with our list of adult-only
        # diagnosis codes. If it's an adult only code, remove it from the
        # list.
        
        return []
```

Using the list provided by CMS, we can create a set of ICD-10 codes that
should be restricted to adults. According to CMS, these diagnoses are only
relevant to patients 15 or older.

While the layout altering class responded to a single event, we're listening
for two different events here: diagnose command search and past medical
history command search. Both of these commands include a diagnosis code search
box, so we'll want to affect both. We wouldn't want to impact a family history
command diagnosis search, since the family members recorded there are often
adults.

#### Looking Up the Patient

In the previous example, the target of the `PATIENT_CHART_SUMMARY__SECTION_CONFIGURATION` event was the patient.
For the events we're responding to here, the target is the [command](/sdk/data-command/)
that the search is occurring within. In order to determine if the patient is
young enough for our code to be invoked, we'll first look up the patient's id
from the command, then assess their age in a similar manner as before.

```python
import arrow

from canvas_sdk.v1.data.command import Command
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler

ADULT_ONLY_ICD_CODES = {
    # There are many, many more. Limiting this example for brevity.
    # ...
    "Z561",   # Change of job
    "Z5682",  # Military deployment status
    # ...
}


class PediatricConditionSearch(BaseHandler):
    """
    Filter condition searches for pediatric patients.
    """

    RESPONDS_TO = [
        EventType.Name(EventType.DIAGNOSE__DIAGNOSE__POST_SEARCH),
        EventType.Name(EventType.MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH),
    ]

    def compute(self):
        """
        Remove condition search results representing codings that are resevered
        for adults if the patient is <= 15 years old.
        """

        # This event's target is the command we are searching within. Look up
        # the patient id from the command.
        patient_id = Command.objects.filter(id=self.target).values_list('patient__id', flat=True).first()

        fifteen_years_ago = arrow.now().shift(years=-15).date().isoformat()
        patient_is_pediatric = Patient.objects.filter(
            id=patient_id, birth_date__gt=fifteen_years_ago).exists()

        # If the patient is not pediatric, do not alter the search.

        # If the patient is pediatric, loop through the search results, and
        # compare the codings of the options with our list of adult-only
        # diagnosis codes. If it's an adult only code, remove it from the
        # list.
        
        return []
```

Once again you see some code that optimizes for performance over readability.
If you're not familiar with the Django ORM, this code:

```python
patient_id = Command.objects.filter(id=self.target).values_list('patient__id', flat=True).first()
```

Is equivalent to this code, which you may find more readable:

```python
command = Command.objects.get(id=self.target)
patient_id = command.patient.id
```

However you get to the patient's id is up to you. Once you have it, the code
is nearly identical to the previous example, the only difference being the age
we're targeting. We are asking the database "Does the patient with this id
have a birth date more recent than 15 years ago?"

#### Altering the Layout

Now that we know when we should act, we need to write the code for filtering
the list of search results. When the search is performed, the raw results are
sent to our code before being ultimately delivered to the dropdown box in the
front-end. We have the opportunity to modify that list before it hits the
dropdown. While we're focused on removing irrelevant choices, you could also
add labels to certain ones you wish to highlight or alter the search order to
guide users to preferred options.

Our code loops through the ICD-10 codes associated with the search results,
checks for their presence in the set of adult ICD-10 codes, and only includes
them in the post-processed set if they are not in the adult code list. The
raw search results are in the event's context object under the `results` key.

Here's the full code:

```python
import json
import arrow

from canvas_sdk.v1.data.command import Command
from canvas_sdk.v1.data.patient import Patient
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler

ADULT_ONLY_ICD_CODES = {
    # There are many, many more. Limiting this example for brevity.
    # ...
    "Z561",   # Change of job
    "Z5682",  # Military deployment status
    # ...
}


class PediatricConditionSearch(BaseHandler):
    """
    Filter condition searches for pediatric patients.
    """

    RESPONDS_TO = [
        EventType.Name(EventType.DIAGNOSE__DIAGNOSE__POST_SEARCH),
        EventType.Name(EventType.MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH),
    ]

    def compute(self):
        """
        Remove condition search results representing codings that are resevered
        for adults if the patient is <= 15 years old.
        """
        results = self.context.get("results")

        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        # This event's target is the command we are searching within. Look up
        # the patient id from the command.
        patient_id = Command.objects.filter(id=self.target).values_list('patient__id', flat=True).first()

        fifteen_years_ago = arrow.now().shift(years=-15).date().isoformat()
        patient_is_pediatric = Patient.objects.filter(
            id=patient_id, birth_date__gt=fifteen_years_ago).exists()

        # If the patient is not pediatric, do not alter the search.
        if not patient_is_pediatric:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        # Create our container for modified search results
        post_processed_results = []

        # Loop through the ICD 10 codes associated with the results
        for result in self.context["results"]:
            for coding in result.get("extra", {}).get("coding", []):
                if not coding.get("system") in ("http://hl7.org/fhir/sid/icd-10", "ICD-10"):
                    continue
                # If the ICD 10 code is not in the list of Adult-only codes,
                # we can add this result to what will ultimately be returned.
                if coding.get("code") not in ADULT_ONLY_ICD_CODES:
                    post_processed_results.append(result)
                    break

        # Return our modified search results
        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

Once installed, certain diagnosis codes will not clutter up search results
in commands for pediatric patients, but will continue to show as expected for
patients over the age of 15.

## Watch the Workflow in Action

<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/ab4a7517b1e846f981d9a3f86b157910?sid=a1a2c26c-13c7-40f5-842c-7fde52b20762" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

View and deploy the Pediatric Patient Chart Customization Extension [here](https://www.canvasmedical.com/extensions/pediatric-patient-chart-customizations).

## Conclusion

Age is one differentiator that changes the relevance of EMR features, but
there are many, many others. Using the Canvas SDK can help keep clinicians
focused, with the features they need front-and-center and the ones they don't
need out of the way.

<br/>
<br/>
<br/>
