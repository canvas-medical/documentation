---
title: "Utils"
---

## Making requests with Http

The Canvas SDK offers a helper class for completing HTTP calls.

```python
from canvas_sdk.utils import Http

http = Http()
```

### get

Sends a GET request.

**Parameters**:

| Name      | Type     | Required | Description                            |
| :-------- | :------- | :------- | :------------------------------------- |
| `url`     | _string_ | `true`   | The url of the request.                |
| `headers` | _dict_   | `false`  | The headers to include in the request. |

**Example**:

```python
from canvas_sdk.utils import Http

http = Http()
http.get("https://my-url.com/", headers={"Authorization": f"Bearer token"})
```

### post

Sends a POST request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
from canvas_sdk.utils import Http

http = Http()
http.post(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"post": "json"},
    data="this-is-my-data"
)
```

### put

Sends a PUT request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
from canvas_sdk.utils import Http

http = Http()
http.put(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"put": "json"},
    data="this-is-my-data"
)
```

### patch

Sends a PATCH request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
from canvas_sdk.utils import Http

http = Http()
http.patch(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"patch": "json"},
    data="this-is-my-data"
)
```

## Making concurrent requests with Http

There is an interface for executing HTTP requests in parallel.

The `batch_requests` method will execute the requests in parallel using multithreading, and return once all the requests
have completed.

The first parameter to the method is an iterable of `BatchableRequest` objects. These can be created with the following
helper functions:

```generic
batch_get
batch_post
batch_put
batch_patch
```

The parameters that these helper functions accept match what the corresponding single-request methods accept.

The `timeout` parameter allows for specifying a timeout value in seconds; if a request has not completed before the
timeout value, an error will be returned for that request. The maximum allowed value for `timeout` is 30 seconds. If
`timeout` is not specified, it will be set to the maximum value.

The return value will be a list of responses to the requests. The order of the return value will correspond to the order
of the provided requests.

**Parameters**:

| Name             | Type                         | Required | Description                   |
|:-----------------|:-----------------------------|:---------|:------------------------------|
| `batch_requests` | _Iterable[BatchableRequest]_ | `true`   | The list of batched requests. |
| `timeout`        | _integer_                    | `false`  | The timeout value in seconds. |

**Example**:

```python
from canvas_sdk.utils import Http, batch_get, batch_post, batch_put, batch_patch

http = Http()

requests = [
    batch_get("https://my-url.com/", headers={"Authorization": f"Bearer token"}),
    batch_post("https://my-url.com/", headers={"Authorization": f"Bearer token"}, json={"post": "json"}),
    batch_put("https://my-url.com/", headers={"Authorization": f"Bearer token"}, data="this-is-my-data"),
    batch_patch("https://my-url.com/", headers={"Authorization": f"Bearer token"}, json={"patch": "json"})
]

responses = http.batch_requests(requests, timeout=10)
```

## Generating PDFs

Plugin authors can generate PDFs using the `pdf_generator` client. There are two approaches: generating from a URL that serves HTML, or generating directly from an HTML string. Both methods upload the resulting PDF to S3 and return a presigned URL.

```python
from canvas_sdk.utils.pdf import pdf_generator
```

The client exposes only `from_url` and `from_html`. Direct HTTP methods (get, post, put, patch) are not available.

### from_url

Generates a PDF from a URL that returns HTML. The service fetches the HTML from the given URL, converts it to PDF, uploads it to S3, and returns a presigned URL.

**Parameters**:

| Name        | Type             | Required | Description                                                                       |
|:------------|:-----------------|:---------|:----------------------------------------------------------------------------------|
| `print_url` | _string_         | `true`   | The path to the HTML endpoint.                                                    |
| `auth`      | _PdfAuthRequest_ | `false`  | Credentials forwarded to the PDF service so it can fetch authenticated endpoints. |

**Returns**: `PdfUrlResponse | None` — `None` if PDF generation failed.

When using `from_url`, the PDF service fetches the HTML from your endpoint directly. If that endpoint requires authentication, the SimpleAPI serving the HTML should use [`BasicAuthMixin`](/sdk/handlers/simple-api/api/#basic) and pass the credentials via `PdfAuthRequest`.

**Example**:

```python
from canvas_sdk.utils.pdf import PdfAuthRequest, pdf_generator

# The PDF service will fetch this endpoint to get the HTML.
# Because the endpoint uses BasicAuthMixin, we pass credentials
# so the service can authenticate on our behalf.
auth = PdfAuthRequest(
    username="user",
    password="password",
)

response = pdf_generator.from_url(
    print_url="plugin-io/api/my_plugin/printout/html?note_uuid=abc-123",
    auth=auth,
)

if response and response.url:
    # response.url is a presigned S3 URL to the generated PDF
    pdf_url = response.url
```

### from_html

Generates a PDF from a raw HTML string. Use this when you already have the HTML content and don't need the service to fetch it from a URL.

**Parameters**:

| Name      | Type     | Required | Description                  |
|:----------|:---------|:---------|:-----------------------------|
| `content` | _string_ | `true`   | The HTML content to convert. |

**Returns**: `PdfUrlResponse | None` — `None` if PDF generation failed.

**Example**:

```python
from canvas_sdk.templates import render_to_string
from canvas_sdk.utils.pdf import pdf_generator

html = render_to_string("templates/note_printout.html", {
    "patient_name": "Jane Doe",
    "note_type": "Office Visit",
})

response = pdf_generator.from_html(content=html)

if response and response.url:
    pdf_url = response.url
```

### PdfUrlResponse

Both methods return a `PdfUrlResponse` on success, or `None` on failure.

| Attribute | Type     | Description                            |
|:----------|:---------|:---------------------------------------|
| `url`     | _string_ | Presigned S3 URL to the generated PDF. |

### Choosing between the two methods

| Use case                                                                  | Method                              |
|:--------------------------------------------------------------------------|:------------------------------------|
| Plugin serves an HTML page via SimpleAPI that requires authentication     | `from_url` with `PdfAuthRequest`    |
| You already have the HTML string in memory (e.g. from `render_to_string`) | `from_html`                         |

## Making requests to the Ontologies service

Plugin authors can make requests to our Ontologies service using the
`ontologies_http` wrapper.

In addition to the `json()` method of the response, which you'll use to access
the response itself, you can also access the `status_code` to verify that the
request was succcessful.

> **Use these endpoints for chart-parity lookups.** The medication and allergen
> search endpoints below back the autocompletes providers use in the chart. Use
> them — not the FHIR `/Medication` or `/Allergen` search endpoints — when you
> need a code that will resolve when used in a command. FHIR `/Medication` and
> `/Allergen` search different, narrower interoperability catalogs and can return
> codes the chart can't resolve (or omit ones it can); a code returned by the
> endpoints below resolves consistently with what the picker shows.

> **Tip:** The Medical Software Foundation's [`coding_lookup`](https://github.com/Medical-Software-Foundation/canvas/tree/main/data-migrations/data_migrations/plugins/coding_lookup) reference plugin wraps the medication and allergen lookups below as ready-made SimpleAPI endpoints (`/medication_search`, `/allergy_search`) returning a clean `{count, results}` shape. Install it as-is, or use it as a template for calling `ontologies_http` from your own plugin.

### Searching for medications

Plugin authors can search for medications by NDC code, RxNorm RXCUI, FDB code, or full-text search.

#### `fdb_code`

Elsewhere in the SDK there are commands that take an `fdb_code` or `new_fdb_code`, some examples being [`AdjustPrescriptionCommand`](/sdk/commands/#adjustprescription), [`MedicationStatementCommand`](/sdk/commands/#medicationstatement),  [`PrescribeCommand`](/sdk/commands/#prescribe), and [`RefillCommand`](/sdk/commands/#refill). The value to be sent as the `fdb_code` is returned in the search payloads below as the `med_medication_id`.

#### `GET /fdb/grouped-medication/` — text and RxNorm search

**Used by:** [Prescribe](/sdk/commands/#prescribe), [MedicationStatement](/sdk/commands/#medicationstatement), and [Refill](/sdk/commands/#refill) (`fdb_code`), and [Adjust Prescription](/sdk/commands/#adjustprescription) (`new_fdb_code`).

Search the medication catalog by full-text query or exact RxNorm RXCUI. Query parameters:

| Parameter      | Type            | Description                                                              |
|----------------|-----------------|--------------------------------------------------------------------------|
| `search`       | string          | Full-text search over the medication name, description, and synonyms.    |
| `rxnorm_rxcui` | string or int   | Match a specific RxNorm RXCUI.                                           |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http

# full-text search of the medication name, description, and synonyms
response_json = ontologies_http.get_json(
    f"/fdb/grouped-medication/?{urlencode({'search': 'tylenol'})}"
).json()

# search by a specific RxNorm RXCUI (same response shape)
response_json = ontologies_http.get_json(
    f"/fdb/grouped-medication/?{urlencode({'rxnorm_rxcui': 313782})}"
).json()
```

The response contains a `results` list; each entry looks like:

```json
{
  "results": [
    {
      "description_and_quantity": "Athenol 325 mg tablet",
      "med_medication_id": 436095,
      "search_rank": 0.082745634,
      "search_terms": "Athenol 325 mg tablet|ACETAMINOPHEN ORAL|...|TYLENOL|...",
      "med_medication_description": "Athenol 325 mg tablet",
      "clinical_quantities": [
        {
          "erx_quantity": "1.0000000",
          "representative_ndc": "11822317640",
          "clinical_quantity_description": "tablet",
          "erx_ncpdp_script_quantity_qualifier_code": "C48542",
          "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
        }
      ],
      "etc_path_id": [3645, 574, 578, 577],
      "etc_path_name": [
        "Analgesic, Anti-inflammatory or Antipyretic",
        "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
        "Analgesic or Antipyretic Non-Opioid and Combinations",
        "Analgesic or Antipyretic Non-Opioid"
      ],
      "rxnorm_rxcui": "313782"
    }
  ]
}
```

Each result's `clinical_quantities` array supplies the values for a [`ClinicalQuantity`](/sdk/commands/#clinicalquantity) on prescribe commands — `representative_ndc`, `erx_ncpdp_script_quantity_qualifier_code` → `ncpdp_quantity_qualifier_code`, and `clinical_quantity_description` → `description`.

#### `GET /fdb/grouped-medication/{med_medication_id}/` — look up by FDB code

Fetch one or more medications by FDB code. Pass a single `med_medication_id`, or a comma-separated list of ids, as the path segment.

| Parameter                   | Type                          | Description                        |
|-----------------------------|-------------------------------|------------------------------------|
| `med_medication_id` (path)  | int, or comma-separated ints  | One or more FDB medication ids.    |

```python
# single FDB code
response_json = ontologies_http.get_json("/fdb/grouped-medication/123456/").json()

# multiple FDB codes
med_medication_ids = ["123456", "123457"]
response_json = ontologies_http.get_json(
    f"/fdb/grouped-medication/{','.join(med_medication_ids)}/"
).json()
```

Returns the same full `results` shape as the text/RxNorm search above — each entry includes every field, including `clinical_quantities`:

```json
{
  "results": [
    {
      "description_and_quantity": "Athenol 325 mg tablet",
      "med_medication_id": 123456,
      "search_terms": "Athenol 325 mg tablet|ACETAMINOPHEN ORAL|...|TYLENOL|...",
      "med_medication_description": "Athenol 325 mg tablet",
      "clinical_quantities": [
        {
          "erx_quantity": "1.0000000",
          "representative_ndc": "11822317640",
          "clinical_quantity_description": "tablet",
          "erx_ncpdp_script_quantity_qualifier_code": "C48542",
          "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
        }
      ],
      "etc_path_id": [3645, 574, 578, 577],
      "etc_path_name": [
        "Analgesic, Anti-inflammatory or Antipyretic",
        "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
        "Analgesic or Antipyretic Non-Opioid and Combinations",
        "Analgesic or Antipyretic Non-Opioid"
      ],
      "rxnorm_rxcui": "313782"
    }
  ]
}
```

#### `GET /fdb/ndc-to-medication/{ndc}/` — look up by NDC

Resolve a single NDC to its medication.

| Parameter    | Type   | Description             |
|--------------|--------|-------------------------|
| `ndc` (path) | string | The NDC to resolve.     |

```python
response_json = ontologies_http.get_json("/fdb/ndc-to-medication/76420037215/").json()
```

The response is a single medication object:

```json
{
  "description_and_quantity": "Aphen 325 mg tablet",
  "med_medication_id": 572345,
  "search_terms": "Aphen 325 mg tablet|APHEN 325 MG TABLET|ACETAMINOPHEN 325 MG TABLET",
  "med_medication_description": "Aphen 325 mg tablet",
  "clinical_quantities": [
    {
      "erx_quantity": "1.0000000",
      "representative_ndc": "76420037215",
      "clinical_quantity_description": "tablet",
      "erx_ncpdp_script_quantity_qualifier_code": "C48542",
      "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
    }
  ],
  "etc_path_id": [3645, 574, 578, 577],
  "etc_path_name": [
    "Analgesic, Anti-inflammatory or Antipyretic",
    "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
    "Analgesic or Antipyretic Non-Opioid and Combinations",
    "Analgesic or Antipyretic Non-Opioid"
  ],
  "rxnorm_rxcui": "313782"
}
```

#### `GET /fdb/ndcs-to-medications/{ndcs}/` — look up by multiple NDCs

Resolve several NDCs at once. Pass a comma-separated list of NDCs as the path segment.

| Parameter     | Type                       | Description             |
|---------------|----------------------------|-------------------------|
| `ndcs` (path) | comma-separated strings    | The NDCs to resolve.    |

```python
response_json = ontologies_http.get_json(
    "/fdb/ndcs-to-medications/76420037215,11822317640/"
).json()
```

The response is a dictionary keyed by NDC; each value is the full medication object (same shape as the single-NDC lookup above), including `clinical_quantities`:

```json
{
  "76420037215": {
    "description_and_quantity": "Aphen 325 mg tablet",
    "med_medication_id": 572345,
    "search_terms": "Aphen 325 mg tablet|APHEN 325 MG TABLET|ACETAMINOPHEN 325 MG TABLET",
    "med_medication_description": "Aphen 325 mg tablet",
    "clinical_quantities": [
      {
        "erx_quantity": "1.0000000",
        "representative_ndc": "76420037215",
        "clinical_quantity_description": "tablet",
        "erx_ncpdp_script_quantity_qualifier_code": "C48542",
        "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
      }
    ],
    "etc_path_id": [3645, 574, 578, 577],
    "etc_path_name": [
      "Analgesic, Anti-inflammatory or Antipyretic",
      "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
      "Analgesic or Antipyretic Non-Opioid and Combinations",
      "Analgesic or Antipyretic Non-Opioid"
    ],
    "rxnorm_rxcui": "313782"
  },
  "11822317640": {
    "description_and_quantity": "Athenol 325 mg tablet",
    "med_medication_id": 436095,
    "search_terms": "Athenol 325 mg tablet|ACETAMINOPHEN ORAL|...|TYLENOL|...",
    "med_medication_description": "Athenol 325 mg tablet",
    "clinical_quantities": [
      {
        "erx_quantity": "1.0000000",
        "representative_ndc": "11822317640",
        "clinical_quantity_description": "tablet",
        "erx_ncpdp_script_quantity_qualifier_code": "C48542",
        "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
      }
    ],
    "etc_path_id": [3645, 574, 578, 577],
    "etc_path_name": [
      "Analgesic, Anti-inflammatory or Antipyretic",
      "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
      "Analgesic or Antipyretic Non-Opioid and Combinations",
      "Analgesic or Antipyretic Non-Opioid"
    ],
    "rxnorm_rxcui": "313782"
  }
}
```

**Codes that resolve vs. free text.** A `med_medication_id` returned above resolves cleanly when passed as an `fdb_code` to a command. Some FDB entries — for example the `THSC …`-prefixed results the FHIR `/Medication` search can return — are not in this catalog and will render with a **blank medication name** if used. To record a historical or non-catalog medication as free text instead, pass a `Coding` with `system=CodeSystems.UNSTRUCTURED` (its `display` is used as-is) — see [MedicationStatement](/sdk/commands/#medicationstatement).

### Searching for allergens

Plugin authors can search the allergen catalog — the same catalog behind the chart's allergen autocomplete — by full-text or by RxNorm code.

#### `GET /fdb/allergy` — full-text search

**Used by:** [Allergy](/sdk/commands/#allergy) (`allergy` — the allergen `concept_id` + `concept_type`).

Full-text search of the allergen catalog. Query parameters:

| Parameter                                  | Type   | Description                                                |
|--------------------------------------------|--------|------------------------------------------------------------|
| `dam_allergen_concept_id_description__fts` | string | Full-text search over the allergen concept description.    |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http

response_json = ontologies_http.get_json(
    f"/fdb/allergy?{urlencode({'dam_allergen_concept_id_description__fts': 'chocolate'})}"
).json()
```

The response contains a `results` list of allergen concepts:

```json
{
  "results": [
    {
      "dam_allergen_concept_id": 19561,
      "dam_allergen_concept_id_description": "chocolate",
      "concept_type": "ingredient"
    }
  ]
}
```

#### `GET /fdb/allergen` — RxNorm lookup

Look up allergen concepts mapped to an external code. Query parameters:

| Parameter | Type   | Description                                                                       |
|-----------|--------|-----------------------------------------------------------------------------------|
| `code`    | string | The external code to match, in `{system}\|{code}` form — e.g. `rxnorm\|217013`.   |

```python
response_json = ontologies_http.get_json(
    f"/fdb/allergen?{urlencode({'code': 'rxnorm|217013'})}"
).json()
```

Each result carries the FDB vocabulary type and id:

```json
{
  "results": [
    {
      "evd_fdb_vocabulary_type_identifier": 104,
      "imk_fdb_vocabulary_no_identifier": 19561,
      "imk_fdb_vocabulary_description": "chocolate"
    }
  ]
}
```

#### `GET /fdb/allergy/` — look up by concept id

Resolve a specific allergen concept by id — for example, to confirm a stored allergy. Query parameters:

| Parameter                      | Type | Description                                                                     |
|--------------------------------|------|---------------------------------------------------------------------------------|
| `dam_allergen_concept_id`      | int  | The FDB allergen concept id.                                                    |
| `dam_allergen_concept_id_type` | int  | The allergen category — `1` (allergy group), `2` (medication), or `6` (ingredient). |

```python
response_json = ontologies_http.get_json(
    f"/fdb/allergy/?{urlencode({'dam_allergen_concept_id': 19561, 'dam_allergen_concept_id_type': 6})}"
).json()
```

Returns a `results` list containing the matching allergen concept (same fields as the full-text search above):

```json
{
  "results": [
    {
      "dam_allergen_concept_id": 19561,
      "dam_allergen_concept_id_description": "chocolate",
      "concept_type": "ingredient"
    }
  ]
}
```

#### Mapping results to `AllergyCommand`

To record one of these on a patient, pass the concept id and its type to [`AllergyCommand`](/sdk/commands/#allergy) as `concept_id` and `concept_type`. The catalog's allergen type maps to the command's category as follows:

| Allergen type | `concept_type` (text search) | FDB vocabulary type (RxNorm search) | `AllergyCommand` category |
|---------------|------------------------------|-------------------------------------|---------------------------|
| Allergy group | `allergy group`              | `110`                               | `1`                       |
| Medication    | `medication`                 | `1`                                 | `2`                       |
| Ingredient    | `ingredient`                 | `104`                               | `6`                       |

For example, an allergy to chocolate is ingredient concept `19561` → category `6`.

### Looking up clinical codes

Beyond medications and allergens, the ontologies service resolves coded concepts that back several commands — ICD-10 conditions and CVX immunizations. (SNOMED concept searches are under [Searching clinical concepts](#searching-clinical-concepts).)

#### `GET /icd/condition/` — ICD-10 conditions

**Used by:** [Diagnose](/sdk/commands/#diagnose) (`icd10_code`), [Medical History](/sdk/commands/#medicalhistory) (`past_medical_history`), and the `diagnosis_codes` fields on [Refer](/sdk/commands/#refer), [Imaging Order](/sdk/commands/#imagingorder), and other diagnosis-code commands. _(Prescribe/Refill `icd10_codes` come from the patient's active conditions, not this search.)_

Search ICD-10 conditions by text, or resolve a specific code. This backs the condition/diagnosis autocompletes on commands such as [Diagnose](/sdk/commands/#diagnose), [Assess](/sdk/commands/#assess), and [Medical History](/sdk/commands/#medicalhistory). Query parameters:

| Parameter    | Type   | Description                                                                        |
|--------------|--------|-----------------------------------------------------------------------------------|
| `search`     | string | Full-text search over ICD-10 conditions.                                          |
| `icd10_code` | string | Resolve an exact ICD-10 code instead of searching. Dots optional (`E119` / `E11.9`). |
| `date`       | string | Optional. `YYYY-MM-DD`; resolves codes as of that date.                           |
| `limit`      | int    | Optional. Maximum number of results.                                              |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http

# full-text search
response_json = ontologies_http.get_json(
    f"/icd/condition/?{urlencode({'search': 'type 2 diabetes'})}"
).json()

# resolve a specific code
response_json = ontologies_http.get_json(
    f"/icd/condition/?{urlencode({'icd10_code': 'E119'})}"
).json()
```

Returns a `results` list of matching conditions:

```json
{
  "results": [
    {
      "icd10_code": "E11.9",
      "icd10_text": "Type 2 diabetes mellitus without complications",
      "snomed_concept_id": "44054006",
      "preferred_snomed_term": "Type 2 diabetes mellitus"
    }
  ]
}
```

#### `GET /cpt/immunization/` — search immunizations

**Used by:** [Immunization Statement](/sdk/commands/#immunizationstatement) (`cvx_code` / `cpt_code`).

Search vaccines by name or code. Query parameters:

| Parameter      | Type   | Description                                           |
|----------------|--------|-------------------------------------------------------|
| `name_or_code` | string | A vaccine code, or a text fragment of its name.       |
| `cvx_code`     | string | Optional. Filter to a specific CVX code.              |

```python
response_json = ontologies_http.get_json(
    f"/cpt/immunization/?{urlencode({'name_or_code': 'influenza'})}"
).json()
```

The response contains a `results` list of matching vaccines:

```json
{
  "results": [
    {
      "medium_name": "influenza, injectable, quadrivalent",
      "cpt_code": "90686",
      "cvx_code": "150",
      "cvx_description": "Influenza, injectable, quadrivalent"
    }
  ]
}
```

### Searching clinical concepts

These endpoints back the concept autocompletes on several commands. Each returns a `results` list of matching concepts.

#### `GET /snomed/family-history/` — family-history conditions

**Used by:** [Family History](/sdk/commands/#familyhistory) (`family_history`).

Search SNOMED family-history conditions.

| Parameter | Type   | Description                                        |
|-----------|--------|----------------------------------------------------|
| `search`  | string | Full-text search over family-history conditions.   |
| `limit`   | int    | Optional. Maximum number of results.               |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http

response_json = ontologies_http.get_json(
    f"/snomed/family-history/?{urlencode({'search': 'diabetes'})}"
).json()
```

The response contains a `results` list of SNOMED concepts:

```json
{
  "results": [
    {
      "concept_id": "73211009",
      "term": "Diabetes mellitus"
    }
  ]
}
```

#### `GET /snomed/family-relation/` — family relationships

**Used by:** [Family History](/sdk/commands/#familyhistory) (`relative`).

Search SNOMED family relationships (mother, father, sibling, …).

| Parameter         | Type   | Description                                                  |
|-------------------|--------|--------------------------------------------------------------|
| `term__icontains` | string | Case-insensitive substring match on the relationship term.   |

```python
response_json = ontologies_http.get_json(
    f"/snomed/family-relation/?{urlencode({'term__icontains': 'mother'})}"
).json()
```

The response contains a `results` list of SNOMED concepts:

```json
{
  "results": [
    {
      "concept_id": "72705000",
      "term": "Mother"
    }
  ]
}
```

#### `GET /snomed/instruction/` — instructions

**Used by:** [Instruct](/sdk/commands/#instruct) (`coding`).

Search SNOMED instructions.

| Parameter         | Type   | Description                                                 |
|-------------------|--------|-------------------------------------------------------------|
| `term__icontains` | string | Case-insensitive substring match on the instruction term.   |

```python
response_json = ontologies_http.get_json(
    f"/snomed/instruction/?{urlencode({'term__icontains': 'physical therapy'})}"
).json()
```

The response contains a `results` list of SNOMED concepts:

```json
{
  "results": [
    {
      "concept_id": "229065009",
      "term": "Physical therapy"
    }
  ]
}
```

#### `GET /snomed/procedures/` — surgical-history procedures

**Used by:** [Surgical History](/sdk/commands/#surgicalhistory) (`past_surgical_history`).

Search SNOMED procedures.

| Parameter | Type   | Description                            |
|-----------|--------|----------------------------------------|
| `search`  | string | Full-text search over procedures.      |
| `limit`   | int    | Optional. Maximum number of results.   |

```python
response_json = ontologies_http.get_json(
    f"/snomed/procedures/?{urlencode({'search': 'appendectomy'})}"
).json()
```

The response contains a `results` list of SNOMED concepts:

```json
{
  "results": [
    {
      "concept_id": "80146002",
      "term": "Appendectomy"
    }
  ]
}
```

### Screening for drug–allergy interactions

**Used by:** the [Prescribe](/sdk/commands/#prescribe) safety screening; also callable directly from a plugin (it is not tied to a command field).

{% include alert.html type="info" content="Canvas runs this screening automatically on staged medication commands in the UI and displays the results to the provider. If you are using the SDK to automate the charting of these commands, that interactive screening may not surface — you may want to run this check yourself." %}

Canvas's drug–allergy screening — the same FDB-backed check the chart runs when a provider adds a medication — is available through `ontologies_http`.

`GET /fdb/medication-allergy/` takes a candidate medication and the patient's allergy list, both as JSON-encoded query parameters:

| Parameter              | Type        | Description                                                                                                                                        |
|------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `consideredMedication` | JSON string | The candidate drug's FDB codings as a flat list of `[code, "FDB"]` pairs, e.g. `[["217012", "FDB"]]`.                                              |
| `allergyList`          | JSON string | The patient's allergies as `[code, category]` pairs, where `category` is the FDB allergen-concept type carried on the allergy record, e.g. `[["476", 1], ["1886", 6]]`. |

```python
import json
from urllib.parse import urlencode

from canvas_sdk.commands.constants import CodeSystems
from canvas_sdk.utils.http import ontologies_http
from canvas_sdk.v1.data import Medication, Patient


def fdb_codings(med: Medication) -> list[list[str]]:
    """The medication's FDB codings as [code, "FDB"] pairs."""
    return [
        [c.code, "FDB"]
        for c in med.codings.all()
        if c.code and c.system == CodeSystems.FDB
    ]


def screen_medication_against_allergies(patient: Patient, considered_med: Medication) -> list[dict]:
    # Candidate medication: [[code, "FDB"], ...]
    considered_codings = fdb_codings(considered_med)

    # Patient's allergies: [[fdb_allergen_code, category], ...]
    allergy_ids = []
    for allergy in patient.allergy_intolerances.committed():
        fdb_coding = next(
            (c for c in allergy.codings.all() if c.code and c.system == CodeSystems.FDB),
            None,
        )
        if fdb_coding:
            allergy_ids.append([fdb_coding.code, allergy.category])

    if not considered_codings or not allergy_ids:
        return []  # nothing to screen → "all clear"

    return ontologies_http.get_json(
        f"/fdb/medication-allergy/?{urlencode({
            'consideredMedication': json.dumps(considered_codings),
            'allergyList': json.dumps(allergy_ids),
        })}"
    ).json()
```

The response is a list of interaction objects — one per matched allergy, distinguishing a direct match from a cross-sensitive one (e.g. a penicillin allergy against a cephalosporin). An empty list `[]` means no interactions (all clear):

```json
[
  {
    "drug": { "...": "full FDB medication payload" },
    "allergy_concept": {
      "dam_allergen_concept_id": 476,
      "dam_allergen_concept_id_type": 1,
      "dam_allergen_concept_id_description": "Penicillins"
    },
    "specific_ingredients": [],
    "cross_sensitive_ingredients": []
  }
]
```

### Screening for drug–drug interactions

**Used by:** the [Prescribe](/sdk/commands/#prescribe) safety screening; also callable directly from a plugin (it is not tied to a command field).

{% include alert.html type="info" content="Canvas runs this screening automatically on staged medication commands in the UI and displays the results to the provider. If you are using the SDK to automate the charting of these commands, that interactive screening may not surface — you may want to run this check yourself." %}

The sibling `GET /fdb/medication-list-interaction/` endpoint checks a single candidate medication against the patient's existing medication list. It checks the candidate against each existing med — it does **not** check the existing meds against each other. Both inputs are JSON-encoded query parameters:

| Parameter              | Type        | Description                                                                                                                        |
|------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `consideredMedication` | JSON string | The candidate drug's FDB codings as a flat list of `[code, "FDB"]` pairs, e.g. `[["217012", "FDB"]]`.                              |
| `medicationList`       | JSON string | The patient's existing meds as a list of per-drug coding lists — **one inner list per drug**, e.g. `[[["155744", "FDB"]], [["261266", "FDB"]]]`. |

> **Group `medicationList` one inner list per drug.** If you flatten it to one entry per coding row, a multi-coding drug can appear to interact with itself and produce false positives.

```python
import json
from urllib.parse import urlencode

from canvas_sdk.utils.http import ontologies_http
from canvas_sdk.v1.data import Medication, Patient
# reuse fdb_codings() from the drug–allergy example above


def screen_drug_drug(patient: Patient, considered_med: Medication) -> list[dict]:
    considered_medication = fdb_codings(considered_med)

    # One inner list per existing drug; exclude the candidate itself.
    medication_list = [
        fdb_codings(med)
        for med in Medication.objects.for_patient(patient).active()
        if med.id != considered_med.id
    ]
    medication_list = [codings for codings in medication_list if codings]

    if not considered_medication or not medication_list:
        return []

    return ontologies_http.get_json(
        f"/fdb/medication-list-interaction/?{urlencode({
            'consideredMedication': json.dumps(considered_medication),
            'medicationList': json.dumps(medication_list),
        })}"
    ).json()
```

The response is a list of interaction objects, one per interacting pair:

```json
[
  {
    "existing_medication": 155744,
    "considered_medication": 217012,
    "existing_medication_description": "metformin 500 mg tablet",
    "severity": 2,
    "severity_text": "Severe Interaction: Action is required to reduce the risk of severe adverse interaction.",
    "monograph_text": ["Drug A / Drug B", "Clinical Effects: ...", "..."]
  }
]
```

`severity` uses FDB's DDIM scale — **lower number = more clinically significant** (the chart uses the same scale):

| `severity` | Meaning                                        |
|------------|------------------------------------------------|
| `1`        | Contraindicated drug combination               |
| `2`        | Severe interaction                             |
| `3`        | Moderate interaction                           |
| `9`        | Undetermined severity / alternative therapy    |

**Screening several new medications at once:** checking each new med only against the patient's *current* list misses interactions *between* the new meds. Accumulate — after screening each new med, add it to the list you screen the next one against:

```python
existing = list(Medication.objects.for_patient(patient).active())
for new_med in new_meds:
    # screen new_med against `existing`, then:
    existing.append(new_med)  # so the next new med is checked against it too
```

## Making requests to the Pharmacy service

Plugin authors can make requests to our Pharmacy service using the `PharmacyHttp` client. 
This client provides a simplified interface for searching pharmacies and retrieving pharmacy details.

```python
from canvas_sdk.utils.http import pharmacy_http
```

Unlike the general Http client, PharmacyHttp only provides two specific methods for pharmacy operations. 
Direct HTTP methods (get, post, put, patch) are not available.

### Searching for pharmacies

Search for pharmacies using full-text search, specific field filters, or location-based ordering.

**Parameters**:

| Name                | Type      | Required | Description                                                       |
| :------------------ | :-------- | :------- | :---------------------------------------------------------------- |
| `search_term`       | _string_  | `false`  | Full-text search across name, address, city, state, zip, and NCPDP ID. |
| `latitude`          | _string_  | `false`  | Latitude coordinate for location-based ordering.                  |
| `longitude`         | _string_  | `false`  | Longitude coordinate for location-based ordering.                 |
| `id`                | _integer_ | `false`  | Exact pharmacy ID match.                                          |
| `ncpdp_id`          | _string_  | `false`  | Exact NCPDP ID match.                                             |
| `organization_name` | _string_  | `false`  | Case-insensitive contains match on organization name.             |
| `specialty_type`    | _string_  | `false`  | Case-insensitive contains match on specialty type (e.g. "Retail"). |
| `state`             | _string_  | `false`  | Case-insensitive exact match on state (e.g. "NY").                |
| `zip_code_prefix`   | _string_  | `false`  | One or more comma-separated zip code prefixes (e.g. "100,902").   |

**Example**:

```python
from canvas_sdk.utils.http import pharmacy_http

# Full-text search by name
results = pharmacy_http.search_pharmacies("CVS")

# Search with location-based ordering
results = pharmacy_http.search_pharmacies(
    "pharmacy",
    latitude="40.7128",
    longitude="-74.0060"
)

# Filter by state and specialty type
results = pharmacy_http.search_pharmacies(state="NY", specialty_type="Retail")

# Filter by zip code prefixes
results = pharmacy_http.search_pharmacies(zip_code_prefix="100,902")

# Look up by exact NCPDP ID
results = pharmacy_http.search_pharmacies(ncpdp_id="1234567")

# The results list contains pharmacy objects like:
# [
#   {
#     "id": 123456,
#     "distance_miles": 0.8,
#     "ncpdp_id": "1234567",
#     "store_number": "#1234",
#     "organization_name": "CVS Pharmacy #1234",
#     "address_line_1": "123 MAIN ST",
#     "address_line_2": "",
#     "city": "New York",
#     "state": "NY",
#     "zip_code": "10001",
#     "phone_primary": "2125551234",
#     "fax": "2125555678",
#     "latitude": 40.7128,
#     "longitude": -74.0060,
#     "npi": "1234567890",
#     "specialty_type": "Retail",
#     ...
#   },
#   ...
# ]
```

### Looking up a pharmacy by NCPDP ID

Retrieve detailed information about a specific pharmacy using its NCPDP (National Council for Prescription Drug Programs) identifier.

**Parameters**:

| Name        | Type     | Required | Description                          |
| :---------- | :------- | :------- | :----------------------------------- |
| `ncpdp_id`  | _string_ | `true`   | The NCPDP identifier of the pharmacy.|

**Example**:

```python
from canvas_sdk.utils.http import pharmacy_http

# Look up a specific pharmacy
pharmacy = pharmacy_http.get_pharmacy_by_ncpdp_id("1234567")

# The response contains detailed pharmacy information:
# {
#   "id": 123456,
#   "ncpdp_id": "1234567",
#   "store_number": "#1234",
#   "organization_name": "Example Pharmacy #1234",
#   "address_line_1": "123 MAIN ST",
#   "address_line_2": "",
#   "city": "New York",
#   "state": "NY",
#   "zip_code": "10001",
#   "country": "US",
#   "standardized_address_line_1": "123 Main St",
#   "standardized_city": "New York",
#   "standardized_state": "NY",
#   "standardized_zip_code": "100010000",
#   "phone_primary": "2125551234",
#   "fax": "2125555678",
#   "email": "",
#   "active_start_time": "2020-01-01T00:00:00Z",
#   "active_end_time": "2099-12-31T23:59:59Z",
#   "service_level": "New~Refill~Change~Cancel~ControlledSubstance",
#   "npi": "1234567890",
#   "specialty_type": "Retail",
#   "dea_number": "",
#   "organization_type": "Pharmacy",
#   "organization_id": 1234567,
#   "latitude": 40.7128,
#   "longitude": -74.0060,
#   ...
# }
```

### Response fields

Both methods return pharmacy objects with the following key fields:

- `ncpdp_id`: Unique NCPDP identifier for the pharmacy
- `organization_name`: Name of the pharmacy
- `address_line_1`, `address_line_2`, `city`, `state`, `zip_code`: Physical address
- `phone_primary`: Primary phone number
- `fax`: Fax number
- `npi`: National Provider Identifier
- `specialty_type`: Type of pharmacy (e.g., "Retail", "Mail Order")
- `service_level`: Services available (e.g., "New~Refill~Change~Cancel~ControlledSubstance")
- `latitude`, `longitude`: Geographic coordinates
- `distance_miles`: Distance from search location (only present in search results when location is provided)

## Making requests to the Science service

Plugin authors can make requests to our Science service using the
`science_http` wrapper. The Science service backs autocomplete behavior in
the Canvas note UI for imaging order codes (via parse templates) and for
imaging centers and other clinical contacts.

```python
from canvas_sdk.utils.http import science_http
```

Like `ontologies_http` and `pharmacy_http`, `science_http` is a JSON-only
client. You can call `get_json()` and access the response with `json()` and
`status_code`. Direct `get`/`post`/`put`/`patch` methods are not available.

### Searching for imaging codes

Use this to populate the `image_code` field of [`ImagingOrderCommand`](/sdk/commands/#imagingorder). `GET /parse-templates/imaging-reports/` accepts these query parameters:

| Parameter | Type   | Description                                       |
|-----------|--------|---------------------------------------------------|
| `query`   | string | Full-text search over imaging report templates.   |
| `format`  | string | Response format; pass `json`.                     |
| `limit`   | int    | Maximum number of results to return.              |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import science_http

params = {"query": "chest x-ray", "format": "json", "limit": 10}
response_json = science_http.get_json(f"/parse-templates/imaging-reports/?{urlencode(params)}").json()
```

The response contains a `results` list of imaging report templates:

```json
{
  "results": [
    {
      "code": "71046",
      "name": "X-ray of chest, 2 views",
      "code_system": "CPT"
    }
  ]
}
```

Use the returned `code` on the command:

```python
from canvas_sdk.commands import ImagingOrderCommand

command = ImagingOrderCommand(
    note_uuid="8f4b1e2c-9a3d-4c7e-b1f6-2d5a8c0e3b47",
    image_code=response_json["results"][0]["code"],
    diagnosis_codes=["R05"],
)
```

### Searching for contacts and service providers

`GET /contacts/` searches the external contact directory — referring providers, specialists, imaging centers, and other service providers. Use it to populate a `ServiceProvider` on commands such as [Refer](/sdk/commands/#refer) and [Imaging Order](/sdk/commands/#imagingorder), to add external care-team members, or to look up a fax number for outbound faxing. Imaging centers are just contacts with a radiology job title — filter for them with `job_title__icontains=radiology`.

Query parameters (all optional; combine as needed):

| Parameter                                          | Type   | Description                                                                                     |
|----------------------------------------------------|--------|-------------------------------------------------------------------------------------------------|
| `search` (or `query`)                              | string | Full-text search over first/last name, practice name, job title, business address, phone, and fax. |
| `job_title__icontains`                             | string | Filter by job-title substring — pass `radiology` to limit results to imaging centers.           |
| `business_postal_code__in`                         | string | Comma-separated ZIP codes to bias toward local results.                                         |
| `first_name__icontains`, `last_name__icontains`    | string | Filter by contact name.                                                                         |
| `practice_name__icontains`                         | string | Filter by practice name.                                                                        |
| `business_fax__icontains`, `business_fax`          | string | Filter by fax number (substring, or exact match).                                               |
| `format`                                           | string | Response format; pass `json`.                                                                   |

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import science_http

# General service-provider search (e.g. for a referral)
params = {"search": "cardiology", "format": "json"}
response_json = science_http.get_json(f"/contacts/?{urlencode(params)}").json()

# Imaging centers: narrow to a radiology job title
params = {
    "search": "advanced imaging",
    "job_title__icontains": "radiology",
    "format": "json",
    # Optional location filter:
    # "business_postal_code__in": "10001,10002",
}
response_json = science_http.get_json(f"/contacts/?{urlencode(params)}").json()
```

The response contains a `results` list of contact objects:

```json
{
  "results": [
    {
      "firstName": "...",
      "lastName": "...",
      "practiceName": "Advanced Imaging Center",
      "specialty": "Radiology",
      "businessPhone": "2125551234",
      "businessFax": "2125555678",
      "businessAddress": "123 Main St, New York, NY 10001",
      "notes": "..."
    }
  ]
}
```

Pass a selected contact as the `service_provider` on [Refer](/sdk/commands/#refer), [Imaging Order](/sdk/commands/#imagingorder), or other commands that accept a `ServiceProvider`; its `businessFax` and `businessAddress` also drive outbound faxing.

<br/>
<br/>
<br/>
