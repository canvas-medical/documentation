---
title: "FHIR v2 Migration Guide"
guide_for: 
- /api/quickstart/
---

Canvas’s v2 FHIR API is a from-the-ground-up rewrite of our v1 FHIR API. We have matched and exceeded the v1 API’s capabilities, while providing improvements in performance, reliability, consistency, expandability, and general usability.

## Gradual Migration

You can control which API you use on a request-by-request basis by simply changing the subdomain. Your authentication tokens work on both versions.

## Expected General Differences in the v2 API

The goal in developing v2 FHIR API was not to match the behavior of the v1 API in all respects. The goal was to support all the same FHIR resource interactions and simultaneously make additional improvements in validation and FHIR standard compliance. Given that, it is expected that there will be differences between the old and new APIs.

### Observability

The v2 API adds a correlation ID to the headers of every response it sends.  When reporting problems, please provide Canvas with the correlation ID for the failed request, as it expedites the problem resolution process. The correlation ID streamlines our investigation process by allowing Canvas to find all linked log data for that request.

### Validation

The v2 API performs validation of request bodies for create/update interactions that is much more extensive than the old API. Strict conformance to FHIR where possible is the goal. As a result, some fields that were not required before will be required going forward.

According to the FHIR specification, string values must be at least length 1.  Empty strings may have been accepted  some create or update endpoints in the previous version of Canvas’s FHIR API, but the validation that the v2 API does will reject FHIR request bodies that do not conform to this.

### Pagination

Pagination will be turned on by default and required. It can no longer be assumed that a search-type interaction providing no search parameters will return all results in the database within a single response. Clients that want all results will need to make use of the provided links in the search bundle response to page through the data. Pagination links will not be provided for an empty result set.

There is a maximum page size that is enforced by the server. This value is at 100 at the time of writing, but can change without warning. Clients must use the links in a search bundle to paginate after an initial search request is sent.

### OperationOutcome Responses

There is a new validation and error handling framework in place that will provide more detailed error responses. As such, there will be significant departures from how the v1 API reports errors.

**Note:** The improvement of error handling is an ongoing effort that will continue after the v2 API is complete and the v1 API has been fully deprecated. Some error handling pathways from the v1 API will live on in v2 until they are updated.


## Resource-specific Differences in the v2 API

We created a diff-tool that allowed for requests sent to the v1 API to be mock-replayed in the v2 API, such that the responses from old and new can then be compared. The results of this were captured and analyzed for any differences. From there we eliminated unwanted differences and identified and explained all desired differences. The information below is the result of that analysis.

### Appointment

**Create/Update**

- Canvas’s v1 FHIR API supports an incorrect request body format for create and update interactions. The Appointment resource could be embedded in the request body under a key named `resource`. The v1 API supports both this incorrect format and the correct format, but v2 only supports the valid FHIR format.
- Per FHIR, the following applies to `contained`:
  - There must be exactly one resource, and it must be of type `Endpoint`.
  - Per FHIR, the following applies to the Endpoint resource:
    - The `status` field is required, but is not used by Canvas. Canvas recommends sending **active**.
    - The `connectionType` field is required, but is not used by Canvas. Canvas recommends sending an empty JSON object: `{}`
    - The `payloadType` field is required, but is not used by Canvas. Canvas recommends sending: `[{"coding": []}]`
- The `appointmentType` field must contain one coding, and it must be a SNOMED or INTERNAL coding.
- Per FHIR, the `status` field on `participant` elements is required, but is not used by Canvas. Canvas recommends sending **active**.

**Search**

- New parameter `status`
  - `GET /Appointment?status=proposed`
- New parameter `appointment-type`
  - `GET /Appointment?appointment-type=http://snomed.info/sct|308335008`
- New parameter `location`
  - `GET /Appointment?location=Location/6bf7d3a8-06c1-424f-a153-15e53b775769`

### CareTeam

**Update**

- Per US Core, `status` is required (e.g. `active`).
- Per US Core, `subject` is required. In Canvas each patient only has one care team, so CareTeam identifiers match Patient identifiers. The identifier in the subject reference must match the identifier URL. If provided, the value in id must also match the identifier in the URL.

### CarePlan

**Read/Search**

- Per FHIR, `category[*].code` is a list rather than an object. Instead of returning a single object, this field will now return a list of size 1 with the same object.

### Claim

**Create**

- Per FHIR, `supportingInfo` sequence must be a positive integer
- Per FHIR, `quantity` must be a `SimpleQuantity` rather than an integer.
- Per FHIR, `priority` is required. Canvas only accepts `normal` for `priority.coding[0].code` and `http://hl7.org/fhir/ValueSet/process-priority` for `priority.coding[0].system`
- Canvas previously supported identifying the `provider` by their NPI. This will no longer be supported and `provider.reference` should refer to a Practitioner reference from our Practitioner Read/Search endpoints. `provider.type` can be omitted but if valued, it should be `Practitioner`.

### Communication

**Create**

- Per FHIR, `status` is a required value, and per Canvas must be set to `unknown`.
- In the `payload`, the `content` attribute must be named `contentString`.

### Consent

**Create**

- The `scope` field is required by FHIR, but is not used by Canvas. Canvas recommends sending an empty JSON object as a value: `{}`

### Condition

**Read**

- Read must be performed using the resource `id` (a UUID) of the Condition. Read by database primary key was previously supported, but that support has been removed.
- The coding system for `code` is now set to `http://hl7.org/fhir/sid/icd-10-cm` when this code system applies; previously, the string `ICD-10` was returned.

**Search**

- New parameter `clinical-status`
  - `GET /Condition?clinical-status=active`
- New parameter `verification-status`
  - `GET /Condition?verification-status=entered-in-error`

### Coverage

**Create/Update**

- The `resourceType` field needs to be the string `Coverage` exactly, extra quotes will not be supported (e.g. `"Coverage"`).
- The optional fields `payor.display` and `class.value` do not accept empty strings anymore. If provided, they must contain a string at least of length 1.
  - These were previously returned by the Read/Search endpoints though can now be expected to be empty when a value is not present.

### CoverageEligibilityRequest

**Create**

- The `created` field is required by FHIR, but is not used by Canvas. Canvas recommends sending the current timestamp.
- The `insurer` field is required by FHIR, but is not used by Canvas. Canvas recommends sending an empty JSON object as a value: `{}`

### DiagnosticReport

**Read/Search**

- Previously, Canvas included a non-FHIR implementation of `id` in the `encounter`, `identifier`, `performer`, `result`, and `subject` fields.  These fields have been removed.

### DocumentReference

**Read/Search**

- Removed erroneous usage of `identifier.id`
- For performance reasons, search results no longer include `url`. Read will continue to include `url`.
  - Requesting authenticated, expiring URLs from AWS S3 requires making one API call per document. Only providing this on read requests ensures you only wait on this when you need to.
- Previously, content format system was set to `http://hl7.org/fhir/R4/valueset-formatcodes.html`, but now it is set to `http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem`

### Encounter

**Read/Search**

- The `appointment.reference` field now has the string `Appointment/` as a prefix (so it is in the format `Appointment/{id}` instead of just `{id}`).

### Goal

**Read/Search**

- The `startDate` field in the Goal resource will now be pulled from the `start_date` field on the Canvas Goal model. Previously, `startDate` was populated with `local_date_of_service` of the associated note.

### Location

**Read/Search**

- Per FHIR, the `active` field is now named `status`.

### Medication

**Read**

- Previously, `code.coding` repeated the RxNorm codes with display values for an internal field.  This has been corrected to remove the repetitions and include the display value for the Medication.

### MedicationRequest

**Read/Search**

- Per FHIR, the field `reasonCode.coding` is now a list rather than an object. This means instead of returning an object, the field will now return a list of size 1 with the same object.
- Dispense quantity was previously sent for both `doseAndRate.doseQuantity` and `dispenseRequest.quantity`. The `doseAndRate.doseQuantity` now represents the amount of medication per dose rather than the quantity of medication units.
- The coding system for `reasonCode` is now set to `http://hl7.org/fhir/sid/icd-10-cm` when this code system applies; previously, the string `ICD-10` was returned.

### Observation

**Create**

- Per FHIR, the `status` is required, but is not used by Canvas. Canvas recommends sending `unknown`.
- The `status` field will always be returned with the value `entered-in-error` if the Observation data instance has a value in the `entered_in_error` field in Canvas.
- `valueQuantity.value` must be provided as a number, not a string.
- Vital sign observations for composite measurements such as <u>blood pressure</u> must not use the root level `valueQuantity` field since these are instead provided as entries under the `component[*].valueQuantity` field. Blood pressure is the only observation supported by Canvas that must be sent as components.
- For non-composite measurements such as <u>weight</u> (and all other Canvas Vitals command measurements except blood pressure) the root level `valueQuantity` field should be used and no duplicate component valueQuantities should be included.

**Read/Search**

- The `status` field will always be returned with the value `entered-in-error` if the Observation data instance has a value in the `entered_in_error` field in Canvas.
- A `dataAbsentReason` entry will never be present if a valid value is provided for `valueQuantity`
- Canvas does not make use of the `interpretation` field, so this has been removed in the interest of clarity instead of returning an explicit `unknown` entry.
- Previously, for Observations where the `hasMember` field contained references to other Observations, the `code` field contained the codings for all of the members. Now, `code` will only contain the codings associated with the Observation itself, and will not include codings of the members.

### Patient

**Create/Update**

- Per FHIR, `photo` must be a list of type `Attachment` rather than a single `Attachment`. Canvas will still only utilize the first entry.
- Per FHIR, `gender` is a required field and must be one of the fields accepted by FHIR: (`male | female | other | unknown`)
- Per FHIR, `telecom` field must be a list.
- Per FHIR, `telecom[*].rank` must be an integer of value 1 or greater. 0 will no longer be accepted as a value for `telecom[*].rank`.
- The `birthDate` field must meet FHIR’s date format requirements.
- `identifier[*].use` must now be one of (`usual | official | temp | secondary | old`) if it is provided
- `contact[*].name` previously accepted a list. Now it conforms to the FHIR spec and no longer accepts a list.
- Previously, the `gender` field value was the same as the stored `birthsex` value. Now the gender field value in read and search responses is extracted from the gender identity extension value if one was passed in to create or update, or the value of the gender field if the gender identity extension was not used.
- The `birthsex` extension will now follow standard FHIR and can only be one of `(M | F | OTH | UNK | ASKU)`
- `http://schemas.canvasmedical.com/fhir/extensions/emergency-contact`, `http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information`, `http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity`, and `http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation` extensions were added.
- Previously, omitting the `telecom`, `address`, or `contact` arrays entirely would have no effect on the database values for those fields.  In the new API, omitting these fields entirely will have the same effect as sending an empty array would (i.e. removing any data currently in the database for those fields), to properly adhere to how REST APIs should handle updates.
- The race and ethnicity extensions are now specified with this format:

```json
{
    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
    "extension": [
        {
            "url": "ombCategory",
            "valueCoding": {
                "system": "urn:oid:2.16.840.1.113883.6.238",
                "code": "2028-9"
            }
        },
        {
            "url": "detailed",
            "valueCoding": {
                "system": "urn:oid:2.16.840.1.113883.6.238",
                "code": "1006-6"
            }
        }
    ]
}
```

- The structure of the race and ethnicity extensions is the same. Codings
can be obtained from the FHIR documentation for each extension:
  - [http://hl7.org/fhir/us/core/StructureDefinition-us-core-race.html](http://hl7.org/fhir/us/core/StructureDefinition-us-core-race.html)
  - [http://hl7.org/fhir/us/core/StructureDefinition-us-core-ethnicity.html](http://hl7.org/fhir/us/core/StructureDefinition-us-core-ethnicity.html)
- The `url` value for each inner extension can be: `ombCategory` or `detailed`
- The concept of unknown can be specified as follows:
  - The `url` for the ValueSet should be set to `ombCategory`.
  - The `system` for the `valueCoding` should be set to `http://terminology.hl7.org/CodeSystem/v3-NullFlavor`
  - The `code` for the `valueCoding` should be set to `UNK`
- Previously, language coding systems were set to`http://hl7.org/fhir/ValueSet/all-languages`, but now they are set to `urn:ietf:bcp:47`

**Read/Search**

- `telecom[*].period` previously contained hardcoded values not linked to any underlying data. This has been removed.
- There are some minor spacing differences in the values of the `text.div` field.
- Extensions with no `valueString` values (namely `http://schemas.canvasmedical.com/fhir/extensions/clinical-note` and `http://schemas.canvasmedical.com/fhir/extensions/administrative-note extensions`) are no longer returned.
- Previously, the `gender` field value was the same as the stored `sexAtBirth` value. Now the `gender` field value in read and search responses is extracted from the gender identity extension value if one was passed in to create or update, or the value of the gender field if the gender identity extension was not used.
- The `birthsex` extension will now follow standard FHIR and be one of `(M | F | OTH | UNK | ASKU)`
- `http://schemas.canvasmedical.com/fhir/extensions/emergency-contact`, `http://schemas.canvasmedical.com/fhir/extensions/authorized-for-release-of-information`, `http://hl7.org/fhir/us/core/StructureDefinition/us-core-genderIdentity`, and `http://schemas.canvasmedical.com/fhir/extensions/sexual-orientation` extensions were added.

**Special note regarding `telecom[*].rank`**

- Per FHIR, `telecom[*].rank` must be a positive integer. Please note that if you have `rank` values stored in your own systems from read/search responses prior to this migration, you may see a difference between some of the `rank` values received after the migration and your stored `rank` values. This is because Canvas previously allowed and returned `rank` values of 0.

### PaymentNotice

**Create**

- The `created` field is required by FHIR, but is not used by Canvas. Canvas recommends sending the current timestamp. The value returned by a read or search interaction will be the creation timestamp of the actual database record.
- The `payment` and `recipient` fields are required by FHIR, but are not used by Canvas. Canvas recommend sending empty JSON objects as values: `{}`

### Questionnaire

**Search**

- Search behavior has generally been simplified and clarified. Previously, when using search filters like `identifier`, `code`, or `name`, other search filters like `status` would be automatically and implicitly applied. Now, search results will only be filtered by what is specified by the supplied search parameters. 
- New parameter `status`
  - `GET /Questionnaire?status=active`
  - `GET /Questionnaire?status=retired`

### QuestionnaireResponse

**Create**

- Per FHIR, `status` is required, and Canvas only acknowledges `completed` status. All QuestionnaireResponse messages should contain a `status` of `completed`.
- Per FHIR, `item -> answer -> valueString`, if present, may not be an empty string. Empty text answers must be omitted.
- Per FHIR, `item -> answer -> valueCoding -> description` must not be an empty string. Coded answers must have a non-empty display value.
  - **Note:** in the rare case a database record already contains an empty string display value, it will be returned as the string `<no display available>` as a notification.

**Search**

- New parameter `questionnaire.code`
  - `GET /QuestionnaireResponse?questionnaire.code=http://loinc.org|69725-0`
- New parameter `questionnaire.item.code`
  - GET `/QuestionnaireResponse?questionnaire.item.code=http://loinc.org|69725-0`

### Task

**Create/Update**

- Per FHIR, `intent` is required, and must be set to `unknown`.
- The following incorrectly-named attributes are accepted by the old API and
will be renamed in Fumage.
  - `assignee` must be referred to as `owner`
  - `creator` must be referred to as `requester`
  - `title` must be referred to as `description`
  - `due` must be referred to as the nested value `restriction -> period -> end`
  - within a `note`, author must be referred to as `authorReference -> reference`

**Search**

- The parameter `creator` must be referred to as `requester`.
- The parameter `identifier` is no longer supported but should be replaced with `_id`, which is the functionality that `identifier` previously implemented
- New parameter `label` to filter by task label
  - `GET /Task?label=example_label`
- New ability to sort by due date
  - `GET /Task?_sort=due-date`
  - `GET /Task?_sort=-due-date`
- New parameter `description` to filter on title/description
  - `GET /Task?description=Netcare`

## Patient Scoped Tokens

Canvas has added support for patient scoped tokens. These are access tokens requested on behalf of a specific patient and have read/write access to that patient’s records only.

To acquire a patient scoped token, you will need to include some parameters in the body of your token request:
- A `client_id` and `client_secret` that your application will use to [authenticate with Canvas](/api/customer-authentication/).
- The Canvas resource id for the `patient` the token will be scoped to
- A `scope` parameter with space separated patient level scopes requested for the token.  
  - Additional requested scopes should follow the pattern `patient/<ResourceName>.<read/write/*>`
    - `patient/Appointment.*`
    - `patient/Appointment.read patient/Appointment.write`
    - `patient/Patient.read`
    - `patient/Practitioner.read`
  - Canvas provides support for the wildcard character, but highly recommends only requesting the minimal scopes and access needed and using it as a convenience when both read and write are truly required for the application.

### Example curl request

```bash
curl --location --request POST \
      'https://<your_subdomain_here>.canvasmedical.com/auth/token/' \
      --header 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'grant_type=client_credentials' \
      --data-urlencode 'client_id=<client_id_from_Canvas>' \
      --data-urlencode 'client_secret=<client_secret_from_Canvas>' \
      --data-urlencode 'patient=abc123' \
      --data-urlencode 'scope=patient/Patient.read patient/Appointment.* patient/Practitioner.read'
```

### Expected Response Body

```json
{
  "access_token": "<the_access_token_to_use_in_your_request>", 
  "expires_in": 36000, 
  "token_type": "Bearer", 
  "scope": "patient/Patient.read patient/Appointment.* patient/Practitioner.read", 
  "smart_style_url": "https://canvas-storages.s3.us-west-2.amazonaws.com/fhir-static-resources/smart-style.json", 
  "patient": "abc123", 
  "need_patient_banner": true
}
```

Using this access token in subsequent requests ensures that records referencing other patients cannot be retrieved through accidental or malicious misuse of the token. Canvas will also deny requests for any resource types which were not included in `scope` of the token request and requests for resource types which do not support patient-scoped tokens.

**Note:** A patient scoped token must include which patient scopes are being requested. Token requests that include the patient parameter but are missing scope or request invalid scopes will be rejected.

<br>
<br>
<br>
<br>
