---
title: "Populating Command Fields"
last_modified_at: "2026-07-02"
guide_for:
- /sdk/commands/
- /sdk/data/
- /sdk/utils/
---

When a provider works with a command in the Canvas UI — Diagnose, Prescribe, Allergy, Refer, and the rest — most fields are backed by an interactive control. You start typing "type 2 diabetes" and the chart autocompletes to an ICD-10 code, you pick a pharmacy from a searchable list, and you choose a severity from a dropdown. The UI does the lookup for you and stores the underlying code, id, or enum value on the command.

When you build those same commands with the [commands module](/sdk/commands/) in a plugin, there is no interactive control. A command field takes the **raw value** — an FDB code, a database id, an ICD-10 code, an enum member — and it is your plugin's job to supply the correct one. This guide shows you where those values come from so your automated charting behaves like a provider working in the UI.

{% include alert.html type="info" content="Rule of thumb: if a field is an autocomplete, search box, or dropdown in the UI, it is not free text in the SDK — you must look up the value first." %}

## The three sources of command values

Every value that a UI control would supply comes from one of three places:

| In the UI it looks like… | In the SDK you get the value from… | Example |
|--------------------------|------------------------------------|---------|
| A **dropdown** of fixed choices | An **enum** under [Command Constants](/sdk/commands/#command-constants) or the command class | `AllergyCommand.Severity`, `AssigneeType`, `PulseRhythm` |
| An **autocomplete of things already on the chart** (or a reference table) | A **[data module](/sdk/data/)** query | An existing `Condition` to assess, a `Staff` key, a `TaskLabel` |
| An **autocomplete that searches a terminology** (medications, codes, contacts) | A **[utils HTTP helper](/sdk/utils/)** (Ontologies / Pharmacy / Science) | Search FDB for a drug, ICD-10 for a diagnosis, a pharmacy by name |

The rest of this guide walks through each source.

## 1. Enums and dropdowns → Command Constants

Fixed-choice fields map to Python enums. Import the enum and pass a member — don't pass a bare string, and don't invent values. The shared enums are documented under [Command Constants](/sdk/commands/#command-constants); command-specific enums are listed in each command's section.

```python
from canvas_sdk.commands import AllergyCommand

allergy = AllergyCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    allergy_id="e5f6a7b8-9c0d-4e1f-8a2b-3c4d5e6f7a8b",
    severity=AllergyCommand.Severity.MODERATE,  # a dropdown in the UI
)
```

Each enum's documentation lists both the member name and the stored value, so you can map an external system's value onto the correct member.

## 2. Chart records and reference tables → data modules

Many fields reference something that already exists in Canvas: a condition on the patient's problem list, a staff member, a questionnaire, a lab partner. In the UI these are autocompletes scoped to the chart or to a reference table. In the SDK you query the matching [data module](/sdk/data/) and pass the id it returns.

```python
from canvas_sdk.commands import AssessCommand
from canvas_sdk.v1.data import Condition

patient_id = "e5f6a7b8-9c0d-4e1f-8a2b-3c4d5e6f7a8b"

# The UI would let the provider pick from conditions already on the chart.
# In a plugin, query for it and pass its id.
condition = (
    Condition.objects.for_patient(patient_id).committed().active().first()
)

assess = AssessCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    condition_id=condition.id,
    status=AssessCommand.Status.STABLE,
)
```

The description of each command field tells you which data module it points to and whether the record has to already be on **that patient's** chart. Common cases:

- **Existing chart items** — the condition to assess or resolve, the medication to stop or change, the goal to close, the reports to review. Query the data module `for_patient(...)` and use the returned id.
- **Reference tables** — a [Staff](/sdk/data-staff/#staff) key for an ordering provider, a [Questionnaire](/sdk/data-questionnaire/#questionnaire) to answer, a [LabPartner](/sdk/data-labs/) and its tests, a [TaskLabel](/sdk/data-task/#tasklabel) to apply. These aren't patient-scoped, but the value still has to match an existing record.

## 3. Terminology search → utils HTTP helpers

The richest autocompletes in the UI search a clinical terminology in real time: FDB for medications and allergens, ICD-10 for diagnoses, SNOMED for family/surgical history, a pharmacy directory, an imaging catalog. Those searches are exposed through the [utils](/sdk/utils/) HTTP clients so your plugin can run the same lookup and pass the resulting code.

| Command field | Helper |
|---------------|--------|
| Prescribe / MedicationStatement / Refill / AdjustPrescription medication (`fdb_code`, `new_fdb_code`) | [Searching for medications](/sdk/utils/#searching-for-medications) (Ontologies) |
| Allergy allergen | [Searching for allergens](/sdk/utils/#searching-for-allergens) (Ontologies) |
| Diagnose / Assess-adjacent ICD-10 codes | [Looking up clinical codes](/sdk/utils/#looking-up-clinical-codes) (Ontologies) |
| Family History, Surgical History, Instruct concepts | [Searching clinical concepts](/sdk/utils/#searching-clinical-concepts) (Ontologies) |
| Prescribe pharmacy (`pharmacy`) | [Searching for pharmacies](/sdk/utils/#searching-for-pharmacies) (Pharmacy) |
| ImagingOrder image code | [Searching for imaging codes](/sdk/utils/#searching-for-imaging-codes) (Science) |
| Refer / ImagingOrder / care-team service providers (including imaging centers) | [Searching for contacts and service providers](/sdk/utils/#searching-for-contacts-and-service-providers) (Science) |

For example, the UI autocompletes a diagnosis; a plugin searches ICD-10 and passes the code it finds:

```python
import json
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http
from canvas_sdk.commands import DiagnoseCommand

response = ontologies_http.get(
    f"/icd/condition/?{urlencode({'search': 'type 2 diabetes'})}"
)
first = json.loads(response.text)[0]

diagnose = DiagnoseCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    icd10_code=first["icd10_code"],
)
```

See the [utils](/sdk/utils/) reference for the parameters and response shape of each endpoint.

## Putting it together

A single command often draws on more than one source. A Prescribe command, for instance, combines a terminology search, a directory search, a reference-table id, and an enum:

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.v1.data import Staff

fdb_code = "..."               # from the medication search (utils)
ncpdp_id = "..."               # from the pharmacy search (utils)
staff = Staff.objects.first()  # the prescriber

prescribe = PrescribeCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    fdb_code=fdb_code,               # utils: medication search
    icd10_codes=["E119"],            # from the patient's active problem list
    pharmacy=ncpdp_id,               # utils: pharmacy search
    prescriber_id=staff.id,          # data module: Staff reference table
    substitutions=PrescribeCommand.Substitutions.ALLOWED,  # enum
    quantity_to_dispense=30,
)
```

## Interaction screening for medication commands

In the Canvas UI, when a provider stages a medication command (such as Prescribe), Canvas automatically runs **drug–allergy** and **drug–drug** interaction screening and shows the results to the provider. When you originate or commit medication commands with the SDK — outside that interactive flow — this screening does **not** run automatically.

If you want the same safety net, you can opt in to running the checks yourself against the patient's allergy and medication lists using the ontologies screening endpoints, then act on the results before the command is committed:

| Check | Helper |
|-------|--------|
| Drug–allergy | [Screening for drug–allergy interactions](/sdk/utils/#screening-for-drugallergy-interactions) (Ontologies) |
| Drug–drug | [Screening for drug–drug interactions](/sdk/utils/#screening-for-drugdrug-interactions) (Ontologies) |

This is opt-in: only add it if your workflow charts medications programmatically and you want to reproduce the interaction warnings a provider would see in the UI.

## Tips

- **Check the field description first.** Each command field in the [Commands reference](/sdk/commands/#commands) says whether it wants a code, an id, or an enum — and links to the data module or utils endpoint that supplies it.
- **Match the UI's scoping.** If a field references something on the chart, query it `for_patient(...)` so you don't attach another patient's record.
- **Handle "no match."** A search or query can come back empty. Decide what your plugin should do (skip the field, raise, or fall back) rather than passing a guess.
- **Don't hard-code codes you can't verify.** Terminologies change; look values up so you stay in sync with what the chart would offer.

<br/>
<br/>
<br/>
