---
title: "Care Protocols"
layout: documentation
---

## Introduction {#h_01HDPA0TP70RXZC55XHC8NZ4S3}

Protocols are available in Canvas to make care teams aware of
recommended services and interventions. The protocol icon is the first
icon located on the menu bar at the top right of the patient chart. A
red badge indicates a protocol due.

## Key Objectives: {#h_01HDPA0TP74YT4QNA1P7DZ5S1Y}

-   You will learn [who is included in a specific protocol](#h_01FBAE902KS2PNJMAQ4GCZPCVC){:target="_self"}.
-   You will learn [how a protocol is satisfied or completed](#h_01FBAE972ZKVZNA5E0B7Y0AE0W){:target="_self"}.
-   You will learn [why a report is needed](#h_01FBAE9EVTNWS86ZTRDQ1PTJ89){:target="_self"}.
-   You will learn [how to manage a protocol from the patient chart](#h_01FBAE9TGZCE2MQ408WE40AY79){:target="_self"}.
-   You will [have access to the list of protocols](#h_01FBAEB815BYVMH5ZDCRJNSQD7){:target="_self" rel="undefined"}.

## Who is Included in a Specific Protocol? {#h_01FBAE902KS2PNJMAQ4GCZPCVC}

Patients are included in a protocol if they meet certain criteria that
define the protocol population.

This may be demographic information (patient birth sex, age, etc), known
medical conditions (diabetes mellitus), prescribed medications (PrEP
treatment), risk factors, or clinical data.

For example:

-   Colon Cancer Screening population is defined as all patients between
    50-75 years of age.
-   Diabetes population is defined by age ranges AND diabetes condition
    and/or medications. 

Canvas will automatically move patients in or out of protocols based on
changes in clinical information.

## How is a Protocol Satisfied or Completed? {#h_01FBAE972ZKVZNA5E0B7Y0AE0W}

Protocols are satisfied when a specific service or intervention is
completed. Canvas updates the protocol within seconds so you have an
accurate view of which protocols need action.

Many protocols are completed as clinical documents brought into Canvas
via Data Integration (Canvas document importation application). Examples
of this include an uploaded mammogram report or stool based colorectal
cancer screening test. When these documents have been reviewed by the
responsible provider, the protocols are immediately updated.

There are also protocols that are completed automatically as laboratory
data comes into Canvas. 

For example:

-   Hemoglobin A1c
-   Creatinine value

Input through Point of Care testing can also complete protocols.

## Why Do I Need the Actual Report? Why Can\'t I Enter That Something Was Done? {#h_01FBAE9EVTNWS86ZTRDQ1PTJ89}

With the exception of immunizations, Canvas requires an actual document
to record a service such as a mammogram or a lab test.

This requirement is to ensure data accuracy and mitigate the risk
associated with inappropriately turning off a protocol.

For example:

-   The patient states they had a colonoscopy done 2 years ago but the report states that the prep was poor and a repeat was recommended in 1 year.

# Managing Protocols from the Patient Chart {#h_01FBAE9TGZCE2MQ408WE40AY79}

## Video: {#h_01HDPA0TP77YYZT29Q3T7D7S9A}

<iframe src="//www.loom.com/embed/be4644ae907e42a1aec970d7b762536a" width="560" height="315" frameborder="0" allowfullscreen=""></iframe>

## Step by Step: {#h_01HDPA0TP7BPWWW8KJV8GJJGXA}

-   Start the process by opening the desired patient\'s chart.
-   Locate the filter panel icons on your top right.
-   Locate the Protocols Icon which will have a red icon with a number
    indicating how many protocols need to be satisfied for that particular
    patient.

![Screen_Shot_2021-05-11_at_9.37.32_AM.png](/assets/images/care-protocols/protocol-header.png){:width="543" height="129"}

-   Click on the protocols icon to display the protocols modal on the right-hand side.
-   Filter through the protocols in this section by selecting a view from the drop the down menu at the top of the protocols modal.
    -   Active
    -   Pending
    -   Inactive

![j.gif](/assets/images/care-protocols/active-pending-inactive.gif){:width="511" height="302"}

***NOTE:** Active protocols are the default view after clicking on the protocols filter icon.*

-   Review Protocols by navigating to the protocol desired.
-   Each protocol card will display the following:
    -   Relevant Exams (if any)
    -   Current Screening Intervals
    -   Recommendations to fulfill the protocol which can include:
        -   [Reviewing images](/hc/en-us/articles/360057918193-Imaging-Reports){:target="_self"}
        -   [Reviewing consult reports](/hc/en-us/articles/360057088473-Consult-Report-Review){:target="_self"}
        -   [Ordering labs](/hc/en-us/articles/360056890753-Placing-a-Lab-Order){:target="_self"}
        -   [Ordering Imaging](/hc/en-us/articles/360057139093-Order-an-Imaging-Study){:target="_self"}
        -   [Completing Questionnaire](/hc/en-us/articles/360057544593-Command-Questionnaire){:target="_self"}
        -   [Provide Instruction](/hc/en-us/articles/360055309574-Command-Instruct){:target="_self"}
    -   Option to Request Records

***NOTE:** Fulfilling the recommendations for the protocol will make the protocol inactive.*

## List of Protocols: {#h_01FBAEB815BYVMH5ZDCRJNSQD7}

### Annual Wellness Visit (HCC005v1)

This is a protocol that recommends an annual wellness visit for patients 65 years and older, if they have not had one in the past year. This is determined by the presence of CPT codes G0438 and G0439.

![screenshot](/assets/images/protocols/annual-wellness-visit.png){:width="500"}

## Breast Cancer Screening (CMS125v6)

This protocol recommends a breast cancer screening for all patients born as female and that have an age between 51 inclusive and 74 exclusive, who do not have a qualifying intervention in the last 27 months. Patients with bilateral or serial right and left mastectomy (as documented in past surgical history) are excluded. Patients are considered to have satisfied this protocol if an imaging study with LOINC 24606-6 has been uploaded and reviewed. Imaging studies with this code include “mammography, diagnostic; bilateral”, “mammography, diagnostic; unilateral”, and “mammography, screening; bilateral”.

![screenshot](/assets/images/protocols/breast-cancer-screening.png){:width="500"}

### CKD Suspect (HCC002v2)

This is a protocol that recommends updating the Conditions List to include kidney related problems if a patient has two eGFR lab values lower than 60 mL/min per 1.73 m2 in the past two years. Note that the eGFR is calculated from the creatinine (not taken from the structured eGFR field).

![screenshot](/assets/images/protocols/ckd-suspect.png){:width="500"}

### Colorectal Cancer Screening

This protocol recommends colorectal cancer screening for patients 50-75 years of age who are not in hospice and who have no documentation of total colectomy or previous colorectal cancer. The protocol is considered satisfied if the patient has a stool test within the last year, flexible sigmoidoscopy within the last 5 years, or colonoscopy within the last 10 years.

![screenshot](/assets/images/protocols/colorectal-cancer-screening.png){:width="500"}

### Diabetes Mellitus With Secondary Complication Suspected (HCC003v1)

This protocol recommends updating a Diabetes without complications diagnosis to Diabetes with secondary complications for patients with an active diagnosis of Diabetes without complications who also have an active diagnosis of a condition considered secondary to or exacerbated by diabetes mellitus (including renal, retinal, neurologic or vascular complications). This update may not always be clinically necessary; this protocol functions as a prompt to consider whether the change is appropriate.

### Diabetes Mellitus: Eye Exam (CMS131v6)

This protocol recommends an eye exam for all patients with diabetes mellitus between the ages of 18 to 75 years old. The diabetes mellitus eye exam protocol excludes patients who were in hospice care during the measurement year. The interventions that will satisfy the diabetes mellitus eye exam protocol include the ordering of a Retinal or Dilated Eye Exam, a Specialist Consult Report must be uploaded/come in via Data Integration and must also be reviewed by the provider to satisfy the protocol. The integration specialty consult reports to use include: Ophthalmology: Diabetic Retinopathy Screening.

![screenshot](/assets/images/protocols/diabetes-eye-exam.png){:width="500"}

### Diabetes Mellitus: Hemoglobin HbA1c Poor Control (> 9%) (CMS122v6)

This is a protocol for patients between the ages of 18-75 years old with a diagnosis of diabetes. It identifies patients with “poor control” which is defined as either a hemoglobin A1c > 9% or no hemoglobin A1c in the last year. For those with no hemoglobin A1c in the past year, a recommendation is surfaced to check labs. For those with A1c > 9% a recommendation is surfaced for dietary changes.

### Dysrhythmia Suspects (HCC004v1)

This protocol looks for all patients with an active medication in an anti-arrhythmic drug class and identifies patients who have an active anti-arrhythmic medication without an active dysrhythmia related problem, and recommends updating the Conditions List to include dysrhythmia related problem as clinically appropriate.

![screenshot](/assets/images/protocols/dysrhythmia-suspects.png){:width="500"}

### Problem List Hygiene (HCC001v1)

This protocol looks for all patients with significant active conditions which have not been assessed in the last year, and recommends a provider Assess or resolve conditions as clinically appropriate.
