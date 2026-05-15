---
title: Upcoming Breaking Change - Patient Contact Relationship
date: 2025-09-16
layout: productupdates
tags: breaking-change
---

To comply with USCDI v3, Canvas is adding FHIR read and search endpoints for the RelatedPerson resource. To achieve this, we will use FHIR RelatedPerson to represent patient contacts, an already-existing feature in Canvas. **To meet requirements, we must make several breaking changes to the user interface, data model, and existing FHIR Patient endpoints. These changes will take effect on Tuesday September 30, 2025.**


<span class="tag-ui">ui</span>

We will be deprecating the free text Relationship field on the contacts section of the patient profile page. This field will no longer be seen in the user interface. To preserve the data in the Relationship field, we will be performing a one-time data migration where the text present in the Relationship field will be appended to the Comments field in the following format `Relationship: value`

<span class="tag-api">api</span>

Patient contacts are also read and written using the FHIR Patient CRUS endpoints. The Relationship field is currently mapped to `contact[].relationship[].text`. We will be discontinuing inclusion of this value in read and search response bodies, and we will be discontinuing consumption of this value by create and update endpoints. **FHIR clients that depend on this field must be updated.**

While the data in the Relationship field will be preserved for archival purposes, the ability to store a relationship value using FHIR Patient create/update is going to be replaced by expanding the use of Contact Categories. In addition to the existing contact categories present on Canvas and custom categories that may have been added, we will also be adding categories from this [ValueSet](/https://hl7.org/fhir/R4/valueset-patient-contactrelationship.html)

Additionally, we will be removing the extension that specifies contacts as an **emergency contact** or **authorized for release of information**. Contacts can still be set as emergency contacts or authorized for release of information by providing relationship codings, as seen below. FHIR clients will need to be updated to write this information without using the extensions:

```json
{
    "resourceType": "Patient",
    "contact":
    [
        {
            "relationship":
            [
                {
                    "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                    "code": "EMC"
                },
                {
                    "system": "http://schemas.canvasmedical.com/fhir/contact-category",
                    "code": "ARI"
                }
            ]
        }
    ]
}
```

Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)






