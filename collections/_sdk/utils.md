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

```
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

## Making requests to the Ontologies service

Plugin authors can make requests to our Ontologies service using the
`ontologies_http` wrapper.

In addition to the `json()` method of the response, which you'll use to access
the response itself, you can also access the `status_code` to verify that the
request was succcessful.

### Searching for medications

Plugin authors can search for medications by NDC code, RxNorm RXCUI, or full-text search.

```python
from urllib.parse import urlencode
from canvas_sdk.utils import ontologies_http

# full text search of the medication name, description, and synonyms
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/?{urlencode({"search": "tylenol"})}").json()

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
response_json = ontologies_http.get_json(f"/fdb/grouped-medication/?{urlencode({"rxnorm_rxcui": 313782})}").json()

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
