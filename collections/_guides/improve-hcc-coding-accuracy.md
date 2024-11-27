---
title: "Improve HCC Coding Accurarcy"
---

Different patients present unique challenges, and your tools should adapt to meet their specific needs.

HCC coding is a critical component of value-based care, especially for organizations serving Medicare Advantage patients. Accurate risk adjustment ensures patients receive appropriate coverage while aligning reimbursement with the complexity of their care needs. However, navigating HCC coding can feel overwhelming with so many diagnoses to consider, guidelines to follow, and tools to use.

This guide will walk you through practical steps to make HCC coding more intuitive and efficient in Canvas. You'll learn how to: 
- Annotate ICD-10 codes that are mapped to HCC categories 
- Create coding gaps frome external data using the FHIR DetectedIssue endpoint
- Surface coding gaps as actionable protocol cards
- Address and resolve codings gaps seamlessly within the clinical workflow through streamlined commands.

By focusing your tools on what's most important for the patient in front of you, you'll create a workflow that's both precise and efficient—eliminating distractions and empowering your team to deliver care with confidence.

## Annotate ICD-10 Codes
- Reference a file? 
## Create Coding Gaps via FHIR Detected Issue

CODINGGAP:  Identifies the type of detected issue is a risk adjustment coding gap. 
This can be used to surface conditions present on historical claims and not yet diagnosed during the calendar year, suspect conditions, or condition data from external sources. 

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

## Surface New Coding Gaps as Protocol Cards

## Use Coding Gap Commands to Update the Patient's Record

There are 4 commands for clinicans and staff to manage coding gaps"

- Create Coding Gap serves as a manual way to add coding gaps to the chart. Staff have the ability to create and validate in the same step. 
- Validate Coding Gap allows the care team (often CDI Reviewers) to review the external date and confirm that the gap should be surfaced to a clinican. 
- Assess Coding Gap allows clinicians to accept or refute the diagnose and choose the appropiate diagnosis to add to the visit. 
- Defer Coding Gap allows clinicians to acknowledge the gap and snooze it for a period of time so that they can return to it at a later date. This may be necessary if the patient is unable to provide enough detail or they run out of time during a visit. When recapture rate is an important metric, this allows reporting to reflect an action was taken. 

By leveraging intuitive tools and streamlined workflows, you can simplify HCC coding and focus on delivering patient-centered care. This approach ensures accuracy, efficiency, and confidence in addressing risk adjustment challenges.


