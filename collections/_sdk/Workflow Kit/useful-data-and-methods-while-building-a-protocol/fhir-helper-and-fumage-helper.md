---
title: "FHIRHelper and FumageHelper"
slug: "fhir-helper-and-fumage-helper"
excerpt: "Helper classes that send requests to your FHIR or Fumage API."
hidden: false
createdAt: "2023-10-02T23:54:42.436Z"
updatedAt: "2023-10-02T23:54:42.436Z"
---
If you wish to send FHIR API requests within a protocol, there is a nifty helper class that can do the work for you - including requesting a bearer token and sending create / search / read / update requests.

You can refer to the [FHIR API Reference docs](/api) for which FHIR resources allow which kinds of requests.

## One-time set up

In order to use the FHIRHelper or FumageHelper class, you will need to do some initial setup within your ProtocolSettings first. 

Navigate to the ProtocolSettings admin page: <b>https\://{instance-name}.canvasmedical.com/admin/api/protocolsetting/<b>

Create these three protocol settings, if they don't already exist (note: the keys must be spelled and capitalized exactly as below):

- `CLIENT_ID`
- `CLIENT_SECRET`
- `INSTANCE_NAME`

If you need help finding the values for `CLIENT_ID` and `CLIENT_SECRET`, refer to the [authentication documentation](/api/customer-authentication/).

## Import and instantiate the helper class

To get started in your protocol, import the appropriate helper class. 

- If you send requests to FHIR: `from canvas_workflow_kit.fhir import FHIRHelper`
- If you send requests to Fumage: `from canvas_workflow_kit.fhir import FumageHelper`

Next, you will instantiate the class within the `compute_results` method and pass in the protocol settings as an argument. 

`fhir = FHIRHelper(self.settings)`

## Request a bearer token

If you wish to request a token and keep track of it yourself, you can do so with:

`token = fhir.get_fhir_api_token()`

This step is not necessary though if you plan to do all your requests using the helper class. (This method will get called automatically within the class before doing any requests).

## Create

**Description**: Given a resource_type (str) and FHIR resource payload (dict), creates a FHIR resource and returns the response.

**Parameters**:

| Name            | Type     | Required | Description                                                                                                                                                                                          |
| :-------------- | :------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type` | _string_ | `true`   | The type of resource you wish to create. All possible resource types can be found in the [FHIR API Reference documentation](/api). |
| `payload`       | _dict_   | `true`   | The body of the resource you wish to create.                                                                                                                                                         |

**Example**:

```python

  fhir = FHIRHelper(self.settings)
  payload = {
    "resourceType": "Patient",
    "extension": [
      {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
        "valueCode": "M",
      }
    ],
    "active": True,
    "name": [{"use": "official", "family": "Bean", "given": ["Jelly"]}],
    "birthDate": "2000-11-13",
  }
  response = fhir.create("Patient", payload)
  if response.status_code == 201:
    response_json = response.json()
  
```

## Search

**Description**: Given a resource_type (str) and search_params (dict), searches and returns a response with bundle of FHIR resources. 

**Parameters**:

| Name            | Type     | Required | Description                                                                                                                                                                                          |
| :-------------- | :------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type` | _string_ | `true`   | The type of resource you wish to search. All possible resource types can be found in the [FHIR API Reference documentation](/api). |
| `search_params` | _dict_   | `false`  | The search params you wish to use. If none, will return a Bundle of all resources for the given resource_type.                                                                                       |

**Example**:

```python

  fhir = FHIRHelper(self.settings)
  response = fhir.search("Patient", {"name": "Jelly", "birthdate": "2000-11-13"})
  if response.status_code == 200:
  	response_json = response.json()
  
```

## Update

**Description**: Given a resource_type (str), resource_id (str), and FHIR resource payload (dict), updates a FHIR resource and returns the response.

**Parameters**:

| Name            | Type     | Required | Description                                                                                                                                                                                          |
| :-------------- | :------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type` | _string_ | `true`   | The type of resource you wish to update. All possible resource types can be found in the [FHIR API Reference documentation](/api). |
| `resource_id`   | _string_ | `true`   | The id of the resource you are updating.                                                                                                                                                             |
| `payload`       | _dict_   | `true`   | The body of the resource you are updating.                                                                                                                                                           |

**Example**:

```python

  fhir = FHIRHelper(self.settings)
  payload = {
    "resourceType": "Patient",
    "id": "4d9eef48972e42adbde3adec68e5182d",
    "extension": [
      {
        "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
        "valueCode": "M",
      }
    ],
    "active": False,
    "name": [{"use": "official", "family": "Bean", "given": ["Butter"]}],
    "birthDate": "2001-12-14",
  }
  response = fhir.update("Patient", "4d9eef48972e42adbde3adec68e5182d", payload)
  if response.status_code == 200:
    response_json = response.json()
  
```

## Read

**Description**: Given a resource_type (str) and resource_id (str), returns a response with the requested FHIR resource.

**Parameters**:

| Name            | Type     | Required | Description                                                                                                                                                                                        |
| :-------------- | :------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resource_type` | _string_ | `true`   | The type of resource you wish to read. All possible resource types can be found in the [FHIR API Reference documentation](/api). |
| `resource_id`   | _string_ | `true`   | The id of the resource you are reading.                                                                                                                                                            |

**Example**:

```python

  fhir = FHIRHelper(self.settings)
  response = fhir.read("Patient", "4d9eef48972e42adbde3adec68e5182d")
  if response.status_code == 200:
    response_json = response.json()
  
```

