---
title: "Testing Pharmacy Workflows in a Staging Environment"
guide_for:
- /sdk/effect-surescripts/
- /api/practitioner/
- /api/patient/
---

Canvas can point a **dev** instance at our staging services so you can build and validate e-prescribing and pharmacy workflows — NewRx, eligibility, benefit, and medication-history requests — against Surescripts staging, without sending real prescriptions or touching production data.

This is a **beta** offering. It is intended for development and testing only; because it uses non-production endpoints, some edge cases may not behave exactly as they do in production.

<br>

* * *

## What you'll learn

1. How to request the staging switch for your dev instance
2. How to create the test prescriber (FHIR Practitioner)
3. How to create the Surescripts canonical test patients (FHIR Patient)
4. How to run eligibility, benefit, and medication-history requests against them

* * *

## 1. Request the staging switch

Staging setup is performed by Canvas. To get started, [submit a request to Canvas Support](https://portal.usepylon.com/canvas-medical/forms/standard) asking to switch your **dev** instance to staging pharmacy services.

{% include alert.html type="warning" content="<b>The switch is all-or-nothing — it is not scoped to pharmacy alone.</b> Pointing a dev instance at staging repoints <b>all</b> of its backend services to staging: messaging, ontologies, pharmacy, science, web-to-pdf, and the FHIR (Fumage) host. Practically, that means drug/allergy and other lookups resolve against <b>staging ontologies</b>, and your FHIR base URL becomes the <b>staging Fumage host</b>. Only request this for a dev instance you are comfortable running entirely against staging." %}

As part of the switch, Canvas Support will:

- Repoint your dev instance's service endpoints to staging.
- Register your test prescriber's Surescripts SPI for staging and map it to your instance so prescriptions route correctly. (The SPI is not part of the FHIR payloads below — Canvas handles Surescripts enrollment.)
- Confirm the **staging FHIR base URL** to use for the API calls in this guide.

The examples below use `https://fumage-staging.canvasmedical.com`. Use the exact base URL Canvas Support gives you for your instance.

* * *

## 2. Create the test prescriber

Create the prescriber with the [FHIR Practitioner Create](/api/practitioner/#create) endpoint. Use the NPI shown here — Canvas Support maps this NPI to your instance during setup, so it must match.

```sh
curl --request POST \
     --url 'https://fumage-staging.canvasmedical.com/Practitioner' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Practitioner",
    "extension": [
        {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/practitioner-user-username",
            "valueString": "wbest"
        }
    ],
    "identifier": [
        {
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": "3688523885"
        }
    ],
    "active": true,
    "name": [
        {
            "use": "usual",
            "family": "Best",
            "given": ["Wayne"]
        }
    ],
    "telecom": [
        { "system": "phone", "value": "9149603674", "use": "work", "rank": 1 },
        { "system": "fax",   "value": "9149603674", "use": "work", "rank": 1 },
        { "system": "email", "value": "wayne.best@example.com", "use": "work", "rank": 1 }
    ],
    "address": [
        {
            "use": "work",
            "type": "both",
            "line": ["150 Monument Road", "Suite 500"],
            "city": "Philadelphia",
            "state": "PA",
            "postalCode": "19019",
            "country": "United States"
        }
    ],
    "birthDate": "1966-09-09",
    "qualification": [
        {
            "identifier": [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-url",
                    "value": "A60695"
                }
            ],
            "code": { "text": "License" },
            "period": { "end": "2035-06-16" },
            "issuer": {
                "display": "Medical Board of California",
                "extension": [
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-short-name",
                        "valueString": "Medical Board of California"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/issuing-authority-state",
                        "valueString": "CA"
                    },
                    {
                        "url": "http://schemas.canvasmedical.com/fhir/extensions/license-primary",
                        "valueBoolean": true
                    }
                ]
            }
        }
    ]
}
'
```

Notes:

- The `practitioner-user-username` extension (`wbest` above) becomes the prescriber's login username. Sign and send prescriptions **as this prescriber** so the outgoing message carries the SPI that Canvas mapped for your instance.
- To let this practitioner prescribe, assign them a prescriber role. Add a `roles` extension using your instance's provider role code (for example `MD`, `DO`, or `NP`). See the `extension` attribute on the [Practitioner API](/api/practitioner/) for the exact shape.

* * *

## 3. Create the Surescripts test patients

Surescripts staging only returns data for its **canonical test patients**, and the match is strict — name, date of birth, sex, and address (especially ZIP) must match exactly. Create these three with the [FHIR Patient Create](/api/patient/#create) endpoint using the demographics below verbatim.

| Patient | Date of birth | Sex | Address |
|---|---|---|---|
| Soloman Bergamel | 1970-03-21 | M | 1948 Bainbridge St, Philadelphia, PA 19146 |
| Zachary Delaplaine | 2010-12-01 | M | 901 Sauvblanc Blvd, Petaluma, CA 94952 |
| Kara Whiteside | 1952-10-11 | F | 23230 Seaport, Akron, OH 91701 |

### Soloman Bergamel

```sh
curl --request POST \
     --url 'https://fumage-staging.canvasmedical.com/Patient' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Patient",
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "M"
        }
    ],
    "active": true,
    "name": [
        { "use": "official", "family": "Bergamel", "given": ["Soloman"] }
    ],
    "telecom": [
        { "system": "phone", "value": "0000000000", "use": "home", "rank": 1 }
    ],
    "gender": "male",
    "birthDate": "1970-03-21",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": ["1948 Bainbridge St"],
            "city": "Philadelphia",
            "state": "PA",
            "postalCode": "19146"
        }
    ]
}
'
```

### Zachary Delaplaine

```sh
curl --request POST \
     --url 'https://fumage-staging.canvasmedical.com/Patient' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Patient",
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "M"
        }
    ],
    "active": true,
    "name": [
        { "use": "official", "family": "Delaplaine", "given": ["Zachary"] }
    ],
    "telecom": [
        { "system": "phone", "value": "0000000000", "use": "home", "rank": 1 }
    ],
    "gender": "male",
    "birthDate": "2010-12-01",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": ["901 Sauvblanc Blvd"],
            "city": "Petaluma",
            "state": "CA",
            "postalCode": "94952"
        }
    ]
}
'
```

### Kara Whiteside

```sh
curl --request POST \
     --url 'https://fumage-staging.canvasmedical.com/Patient' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Patient",
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
            "valueCode": "F"
        }
    ],
    "active": true,
    "name": [
        { "use": "official", "family": "Whiteside", "given": ["Kara"] }
    ],
    "telecom": [
        { "system": "phone", "value": "1111111111", "use": "home", "rank": 1 }
    ],
    "gender": "female",
    "birthDate": "1952-10-11",
    "address": [
        {
            "use": "home",
            "type": "both",
            "line": ["23230 Seaport"],
            "city": "Akron",
            "state": "OH",
            "postalCode": "91701"
        }
    ]
}
'
```

* * *

## 4. Run eligibility, benefit, and medication-history requests

With the prescriber and a canonical test patient in place, you can exercise the three Surescripts information transactions from a plugin using the [Surescripts effects](/sdk/effect-surescripts/). All three canonical patients above return staging responses for these transactions.

{% include alert.html type="warning" content="<b>The Surescripts effects must be enabled by Canvas.</b> Ask Canvas Support to enable them for your instance in the same request — until then, the effects will not send." %}

- **Eligibility** — `SendSurescriptsEligibilityRequestEffect`. The response arrives asynchronously as a `SURESCRIPTS_ELIGIBILITY_RESPONSE` event; parse it with `SurescriptsEligibilityResponse`.
- **Benefit** — `SendSurescriptsBenefitsRequestEffect` (takes a medication description + NDC). The response arrives as a `SURESCRIPTS_BENEFITS_RESPONSE` event; parse it with `SurescriptsBenefitsResponse`.
- **Medication history** — `SendSurescriptsMedicationHistoryRequestEffect`. Canvas retrieves the patient's trailing-12-month fill history and writes it to the chart; there is no paired response event.

Each effect takes the `patient_id` of one of the test patients and the `staff_id` of the prescriber you created above. See [Surescripts Effects](/sdk/effect-surescripts/) for full request/response field references and handler examples.

* * *

## Sending a NewRx (preferred pharmacy)

To test sending a prescription (NewRx), the patient needs a **preferred pharmacy that exists in the Surescripts staging directory**. Set it via the `preferred-pharmacy` extension on the [Patient](/api/patient/#create) resource, or from the patient's chart in the UI.

{% include alert.html type="danger" content="<b>Do not use Shollenberger Pharmacy as the preferred pharmacy for these test patients.</b> Request a current canonical Surescripts staging test pharmacy from Canvas Support (in the same ticket) and use the NCPDP ID they provide." %}

* * *

## Good to know

- This is a **beta** capability for **dev** instances only. Do not request it for a production instance.
- Surescripts staging processes transactions during business hours (roughly 8 AM – 6 PM ET, Mon–Fri); requests outside that window may not receive a response.
- Because the whole instance runs against staging, ontologies (drug/allergy lookups) and other services also resolve against staging while the switch is in place.
