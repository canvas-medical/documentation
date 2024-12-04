---
title: "Improve HCC Coding Accurarcy"
---

Different patients present unique challenges, and your tools should adapt to meet their specific needs.

HCC coding is a critical component of value-based care, especially for organizations serving Medicare Advantage patients. Accurate risk adjustment ensures patients receive appropriate coverage while aligning reimbursement with the complexity of their care needs. However, navigating HCC coding can feel overwhelming with so many diagnoses to consider, guidelines to follow, and tools to use.

This guide will walk you through practical steps to make HCC coding more intuitive and efficient in Canvas. You'll learn how to leverage our [HCC capture plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/hcc_capture) to do the following: 


- Create coding gaps from external data using the FHIR DetectedIssue endpoint
- Surface coding gaps as actionable protocol cards
- Address and resolve codings gaps seamlessly within the clinical workflow through streamlined commands.
- Annotate ICD-10 codes that are mapped to HCC categories 

By surfacing relevant data when and where it's needed, you can eliminate unnecessary steps, reduce cognitive load, and keep workflows aligned with patient needs.


## Create Coding Gaps via FHIR Detected Issue

The [DetectedIssue FHIR resource](/api/detectedissue)) can be used to surface an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, ineffective treatment frequency, procedure-condition conflict, gaps in care, etc. 

A key use case is surfacing potential codings gaps that come from external sources. 

The workflow within Canvas is centered around issues created with the `DetectedIssue.code` set to `CODINGGAP`. Although we are leveraging it in our R4 endpoint, `CODINGGAP` was introduced to the value set in R5, and can be used for surfacing conditions that may be present on historical claims but not yet diagnosed within the current year, suspect conditions, or condition data from external sources. The code should be structured as follows:

```
    "code": {
        "coding": [
            {
                "system": "https://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "CODINGGAP"
            }
        ]
    },
```

The ICD-10 code can be added to `DetectedIssue.evidence` attribute.

Validated coding gaps (where `DetectedIssue.status` = `preliminary`) will appear in the patient summary if the coding gap commands are enabled in your environment (see more below).


## Surface New Coding Gaps as Protocol Cards

Clinical Documentation Improvement (CDI) staff often play a crucial role in reviewing potential coding gaps, especially those added via the API using external data. 

There is no built in UI feature in Canvas that surfaces coding gaps that have yet to be reviewed for accuracy by staff members. Instead, We haven chosen to leverage plugins to allow for customization within your workflow for surfacing . The example protocol below creates a [protocol card](/sdk/effect-protocol-cards/) when a new DetectedIssue is created for a coding gap with a `registered` status. It then recommends that a staff member validates the information before presenting it to a clinician in the summary. 

The protocol will surface in each patient's chart and staff can also leverage the population page as a work list. 

``` python
from canvas_sdk.protocols.clinical_quality_measure import ClinicalQualityMeasure
from canvas_sdk.events import EventType
from canvas_sdk.effects.protocol_card import ProtocolCard
from canvas_sdk.v1.data.detected_issue import DetectedIssue
from logger import log


class SurfaceNonvalidatedCodingGaps(ClinicalQualityMeasure):
    """

    """

    class Meta:
        title = "Validate Coding Gaps"
        identifiers = ["HCCCapturev1"]
        description = "..."
        information = "https://canvasmedical.com"
        references = ["None"]
        types = ["None"]
        authors = ["Canvas Medical"]

    RESPONDS_TO = [
        EventType.Name(EventType.DETECTED_ISSUE_CREATED),
        EventType.Name(EventType.DETECTED_ISSUE_UPDATED),
    ]

    def surface_non_validated_coding_gaps(self, patient, nonvalidated_coding_gaps):
        """
        Craft a protocol card with the list of coding gaps and return an add protocol card effect
        """
        card = ProtocolCard(
            patient_id=patient.id,
            key="hcccapturev1",
            title="Coding Gaps",
            narrative="These codings gaps have not been validated.",
            status=ProtocolCard.Status.DUE,
            feedback_enabled=False,
        )

        for coding_gap in nonvalidated_coding_gaps:
            coding_gap_title_strings = []

            log.info(str(coding_gap.id))
            for evidence in coding_gap.evidence.all():
                log.info(f"{evidence.display} ({evidence.code})")
                coding_gap_title_strings.append(f"{evidence.display} ({evidence.code})")
            card.add_recommendation(
                title="\n".join(coding_gap_title_strings),
                button="Validate",
                command="validateCodingGap",
                context={"detected_issue_id": coding_gap.dbid},
            )

        return [card.apply()]

    def resolve_coding_gaps_protocol_card(self, patient):
        """
        Craft and return a remove protocol card effect
        """
        card = ProtocolCard(
            patient_id=patient.id,
            key="hcccapturev1",
            title="Coding Gaps",
            narrative="There are no non-validated coding gaps for this patient.",
            status=ProtocolCard.Status.SATISFIED,
            feedback_enabled=False,
        )

        return [card.apply()]


    def compute(self) -> list:
        """
        When a new detectedissue is created or updated, reevaluate (create/update/remove) a protocol card based on the associated evidence
        """
        detected_issue_from_the_event = DetectedIssue.objects.get(id=self.target)
        if detected_issue_from_the_event.code != "CODINGGAP":
            # This detected issue has no impact on the protocol card, so we
            # don't need to do any work.
            return []

        patient = detected_issue_from_the_event.patient
        all_of_that_patients_non_validated_detected_issues = patient.detected_issues.filter(status="registered", code="CODINGGAP")
        
        if all_of_that_patients_non_validated_detected_issues.count() > 0:
            return self.surface_non_validated_coding_gaps(patient, all_of_that_patients_non_validated_detected_issues)
        else:
            return self.resolve_coding_gaps_protocol_card(patient)
```


## Use Coding Gap Commands to Update the Patient's Record

The API can be leveraged to create coding gaps in various states. There are also 4 commands for clinicians and staff to manage coding gaps. 

- Create Coding Gap serves as a manual way to add coding gaps to the chart. Staff have the ability to create and validate in the same step. 
- Validate Coding Gap allows the care team (often CDI Reviewers) to review the external date and confirm that the gap should be surfaced to a clinician. 
- Assess Coding Gap allows clinicians to accept or refute the diagnose and choose the appropriate diagnosis to add to the visit. 
- Defer Coding Gap allows clinicians to acknowledge the gap and snooze it for a period of time so that they can return to it at a later date. This may be necessary if the patient is unable to provide enough detail or they run out of time during a visit. When recapture rate is an important metric, this allow reporting to reflect an action was taken. 

## Annotate ICD-10 Codes

Adding an HCC tag as an annotation to ICD-10 is an easy way to increase awareness for clinicians. The example protocols below leverage a static list of ICD-codes. You could also reference a file contained within the plugin pacakge. Depending on which [HCC model](https://www.cms.gov/medicare/payment/medicare-advantage-rates-statistics/risk-adjustment) you follow, you can swap out the codes accordingly. 

### Adding "HCC" to Command Search Results

The following protocol leverages [command `POST_SEARCH` lifecycle events](/sdk/events/#command-lifecycle-events) and adds an `HCC` annotation to the associated ICD-10 codes within the results for the diagnose, past medical history, create coding gap, and assess coding gap commands.  

``` python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log

ICD_CODES = {
    "HCC": {"A0103", "A0104", "A0105", "A021", "A0222", "A0223", "A0224", "A065", "A072", "A202","ADDMORECODES..."}
}

from logger import log


class AnnotateSearchResults(BaseProtocol):
    """
    You should put a helpful description of this protocol's behavior here.
    """

    RESPONDS_TO = [
        EventType.Name(EventType.DIAGNOSE__DIAGNOSE__POST_SEARCH),
        EventType.Name(EventType.MEDICAL_HISTORY__PAST_MEDICAL_HISTORY__POST_SEARCH),
        EventType.Name(EventType.CREATE_CODING_GAP__DIAGNOSE__POST_SEARCH),
        EventType.Name(EventType.ASSESS_CODING_GAP__DIAGNOSE__POST_SEARCH),
    ]

    def compute(self):
        """
        Add HCC code annotation if the HCC code is found in the search results.
        """
        results = self.context.get("results")

        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        post_processed_results = []
        for result in self.context["results"]:
            for coding in result.get("extra", {}).get("coding", []):
                if not coding.get("system") in ("http://hl7.org/fhir/sid/icd-10", "ICD-10"):
                    continue
                if coding.get("code") in ICD_CODES["HCC"]:
                    if result.get("annotations") is None:
                        result["annotations"] = []
                    result["annotations"].append("HCC")
                    break

            post_processed_results.append(result)

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]

```

### Adding "HCC" to the Condition List and on Claims

The following event/effect pairings can be leveraged to add the `HCC` tag to conditions in the patient summary as well as on the claim using the protocol code below. 

- `CLAIM__CONDITIONS` and `ANNOTATE_CLAIM_CONDITION_RESULTS`
- `PATIENT_CHART__CONDITIONS` and `ANNOTATE_PATIENT_CHART_CONDITION_RESULTS`


``` python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from logger import log


ICD_CODES = {
    "HCC": {
        "A0103", "A0104", "A0105", "A021", "A0222", "A0223", "A0224", "A065", "A072", "A202",
        ,"ADDMORECODES...", 
    }

}

HCC = "HCC"


class PatientChartConditionAnnotation(BaseProtocol):
    """
    Annotate Conditions in the Patient Chart with an HCC tag
    """

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CHART__CONDITIONS)

    def compute(self):
        """
        Annotate patient summary conditions if they match the provided set of HCC codes
        """

        hcc_codes = ICD_CODES[HCC]

        payload = {}
        for condition in self.context:
            icd10_code = next((coding.get("code") for coding in condition.get("codings", []) if coding.get("system") == ICD10), None)
            if not icd10_code:
                continue

            if icd10_code in hcc_codes:
                payload[condition["id"]] = [HCC]

        return [Effect(type=EffectType.ANNOTATE_PATIENT_CHART_CONDITION_RESULTS, payload=json.dumps(payload))]


class ClaimConditionAnnotation(BaseProtocol):
    """
    Annotate Conditions in the Claim modal with an HCC tag
    """

    RESPONDS_TO = [EventType.Name(EventType.CLAIM__CONDITIONS)]

    def compute(self):
        """
        Annotate claim conditions if they match the provided set of HCC codes
        """

        hcc_codes = ICD_CODES[HCC]

        payload = {}
        for condition in self.context:
            icd10_code = next((coding.get("code") for coding in condition.get("codings", []) if coding.get("system") == ICD10), None)
            if not icd10_code:
                continue

            if icd10_code in hcc_codes:
                payload[condition["id"]] = [HCC]

        return [Effect(type=EffectType.ANNOTATE_CLAIM_CONDITION_RESULTS, payload=json.dumps(payload))]


```
## Watch the Workflow in Action

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/076936b383aa4490b0f6e6b3bdf1bbc8?sid=b23470c4-d06b-4723-8b18-be241b8b3be1" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Conclusion

By leveraging intuitive tools and streamlined workflows, you can simplify HCC coding and focus on delivering patient-centered care. This approach ensures accuracy, efficiency, and confidence in addressing risk adjustment challenges. 
