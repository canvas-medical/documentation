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

### `fdb_code`

Elsewhere in the SDK there are commands that take an `fdb_code` or `new_fdb_code`, some examples being [`AdjustPrescriptionCommand`](/sdk/commands/#adjustprescription), [`MedicationStatementCommand`](/sdk/commands/#medicationstatement),  [`PrescribeCommand`](/sdk/commands/#prescribe), and [`RefillCommand`](/sdk/commands/#refill). The value to be sent as the `fdb_code` is returned in the search payloads below as the `med_medication_id`.

### Searching for medications

Plugin authors can search for medications by NDC code, RxNorm RXCUI, FDB code, or full-text search.

```python
from urllib.parse import urlencode
from canvas_sdk.utils.http import ontologies_http

# full text search of the medication name, description, and synonyms
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/?{urlencode({'search': 'tylenol'})}").json()

# response_json contains a "results" key with this object as the first result:
# {
#   "results": [
#     {
#       "description_and_quantity": "Athenol 325 mg tablet",
#       "med_medication_id": 436095,
#       "search_rank": 0.082745634,
#       "search_terms": "Athenol 325 mg tablet|ACETAMINOPHEN ORAL|ACETAMINOPHEN PO|ACETAMINOPHEN VIA FEEDING TUBE|TYLENOL|TYLENOL ORAL|TYLENOL PO|APAP|APAP ORAL|APAP PO|PANADOL|PANADOL ORAL|PANADOL PO|ATHENOL 325 MG TABLET|ACETAMINOPHEN 325 MG TABLET",
#       "med_medication_description": "Athenol 325 mg tablet",
#       "clinical_quantities": [
#         {
#           "erx_quantity": "1.0000000",
#           "representative_ndc": "11822317640",
#           "clinical_quantity_description": "tablet",
#           "erx_ncpdp_script_quantity_qualifier_code": "C48542",
#           "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
#         }
#       ],
#       "etc_path_id": [
#         3645,
#         574,
#         578,
#         577
#       ],
#       "etc_path_name": [
#         "Analgesic, Anti-inflammatory or Antipyretic",
#         "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
#         "Analgesic or Antipyretic Non-Opioid and Combinations",
#         "Analgesic or Antipyretic Non-Opioid"
#       ],
#       "rxnorm_rxcui": "313782"
#     },
#     ...
#   ]
# }

# search for a specific RxNorm RXCUI
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/?{urlencode({'rxnorm_rxcui': 313782})}").json()

# response_json contains the same general format as above

# search for a specific FDB code (med_medication_id)
med_medication_id = 123456
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/{med_medication_id}/").json()

# response_json contains the same general format as above

# search for multiple FDB codes (med_medication_ids)
med_medication_ids = [123456, 123457]
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/{','.join(med_medication_ids)}/").json()

# response_json contains the same general format as above

# look up by NDC
response_json = ontologies_http.get_json(f"/fdb/ndc-to-medication/76420037215/").json()

# response_json contains this object:
# {
#   "description_and_quantity": "Aphen 325 mg tablet",
#   "med_medication_id": 572345,
#   "search_terms": "Aphen 325 mg tablet|APHEN 325 MG TABLET|ACETAMINOPHEN 325 MG TABLET",
#   "med_medication_description": "Aphen 325 mg tablet",
#   "clinical_quantities": [
#     {
#       "erx_quantity": "1.0000000",
#       "representative_ndc": "76420037215",
#       "clinical_quantity_description": "tablet",
#       "erx_ncpdp_script_quantity_qualifier_code": "C48542",
#       "erx_ncpdp_script_quantity_qualifier_description": "Tablet"
#     }
#   ],
#   "etc_path_id": [
#     3645,
#     574,
#     578,
#     577
#   ],
#   "etc_path_name": [
#     "Analgesic, Anti-inflammatory or Antipyretic",
#     "Analgesic, Anti-inflammatory or Antipyretic - Non-Opioid",
#     "Analgesic or Antipyretic Non-Opioid and Combinations",
#     "Analgesic or Antipyretic Non-Opioid"
#   ],
#   "rxnorm_rxcui": "313782"
# }

# look up multiple NDCs
response_json = ontologies_http.get_json(f"/fdb/ndcs-to-medications/76420037215,11822317640/").json()

# response_json is a dictionary where each key is an NDC and each each attribute contains the
# object formatted as the individual ndc-to-medication search above

# look up by RxNorm RXCUI

# response_json is a list containing objects of this type:
# [
#   {
#     "med_medication_id": 156060,
#     "clinical_formulation_id": {
#       "clinical_formulation_id": 4489.0,
#       "hierarchical_specific_therapeutic_class_code": "H3E",
#       "dosage_form_code_2_character": "TA",
#       "route_of_administration_code_1_character": "1",
#       "drug_strength_description": "325 MG",
#       "therapeutic_class_code_generic": 2.0,
#       "therapeutic_class_code_standard": 41.0,
#       "drug_category_code": "0",
#       "gcn_seqno_level_multi_source_single_source_indicator": "1",
#       "gender_specific_drug_indicator": "0",
#       "hierarchical_specific_therapeutic_class_code_sequence_number": 271.0,
#       "drug_strength_description_60": "325 mg",
#       "ingredient_list_description": 1866.0,
#       "interactions": [
#         1674.0,
#         27763.0,
#         29424.0,
#         30280.0,
#         30534.0
#       ]
#     },
#     "clinical_quantities": [
#
#     ],
#     "med_routed_dosage_form_medication_id": 12758.0,
#     "med_strength": "325",
#     "med_strength_unit_of_measure": "mg",
#     "med_medication_description": "Dolono 325 mg tablet",
#     "med_gcn_seqno_assignment_code": "1",
#     "med_medication_name_source_code": "1",
#     "med_reference_federal_legend_indicator": "2",
#     "med_reference_federal_dea_class_code": "0",
#     "med_reference_multi_source_code": "1",
#     "med_reference_generic_medication_name_code": "2",
#     "med_reference_generic_comparative_price_code": "9",
#     "med_reference_generic_price_spread_code": "9",
#     "med_reference_innovator_indicator": "0",
#     "med_reference_generic_therapeutic_equivalence_code": "4",
#     "med_reference_desi_indicator": "9",
#     "med_reference_desi2_indicator": "9",
#     "med_medication_status_code": "3",
#     "med_generic_medication_identifier": 160401.0
#   },
#   ...
# ]
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
