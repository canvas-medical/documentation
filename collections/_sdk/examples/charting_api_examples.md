---
title: 'Charting API Examples'
slug: 'example-charting_api_examples'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/charting_api_examples' target='_blank'>View the source</a> for this plugin on GitHub." %}

This example plugin provides several examples of APIs you might define when
automating charting in Canvas.

- Notes
  - Creating a note
  - Getting information about a note
  - Searching for notes by patient, type, and date of service
  - Adding billing line items to a note
- Commands
  - Creating a command
  - Creating multiple commands from a single request
  - Creating a command and committing it in a single request

## Configuration

All of the example endpoints in this plugin are protected with [API key
authentication](https://docs.canvasmedical.com/sdk/handlers-simple-api-http/#api-key-1).
Once installed, you'll need to set the `simpleapi-api-key` value on the plugin's
configuration page in your EHR.

## Endpoint Documentation

### Search Notes

`GET /plugin-io/api/charting_api_examples/notes/`

This endpoint allows the retrieval of an optionally filtered set of notes. The results are paginated, and the client can exert some control over the page size. The response body will include an attribute, `next_page`, which will either contain a URL to the next page of the same filtered set or be `null`, indicating there are no more records to fetch.

#### Optional query parameters:

##### limit

*int*

Determines the number of results to return per page.

- If unspecified, the default is 10.
- If a number less than 1 is specified, 1 will be used.
- If a number greate than 100 is specified, 100 will be used.

##### offset

*int*

Number of records to skip with returning results. When used with **limit**, this enables the pagination of results.

- If unspecified, the default is 0.
- If a number less than 0 is specified, 0 will be used.


##### patient_id

*str*

Filters the notes returned to just those associated with the given patient.

##### note_type

*coding*

You can search by just the code value or you can search by the
system and code in the format "system|code" (e.g. `http://snomed.info/sct|308335008`).

##### datetime_of_service

*iso8601 formatted datetime string*

Exact match for notes with the given datetime.

##### datetime_of_service__gt

*iso8601 formatted datetime string*

Filter to notes occurring after the given datetime.

##### datetime_of_service__gte

*iso8601 formatted datetime string*

Filter to notes occurring at or after the given datetime.

##### datetime_of_service__lt

*iso8601 formatted datetime string*

Filter to notes occurring before the given datetime.

##### datetime_of_service__lte

*iso8601 formatted datetime string*

Filter to notes occurring at or before the given datetime.

#### Example Request

```bash
curl --request GET \
  --url 'https://training.canvasmedical.com/plugin-io/api/charting_api_examples/notes/?limit=2&offset=4' \
  --header 'Authorization: <your-api-key-goes-here>'
```

#### Example Response

```json
{
  "next_page": "https://training.canvasmedical.com/plugin-io/api/charting_api_examples/notes/?limit=2&offset=6",
  "count": 2,
  "notes": [
    {
      "id": "10ff2047-6301-4ab4-81cd-b500e7df8ef7",
      "patient_id": "5350cd20de8a470aa570a852859ac87e",
      "provider_id": "5843991a8c934118ab4f424c839b340f",
      "datetime_of_service": "2025-02-21 23:31:45.627894+00:00",
      "note_type": {
        "id": "c5df4f03-58e4-442b-ad6c-0d3dadc6b726",
        "name": "Office visit",
        "coding": {
          "display": "Office Visit",
          "code": "308335008",
          "system": "http://snomed.info/sct"
        }
      }
    },
    {
      "id": "4dba128f-96cc-4dd0-814b-a064bfdcde7e",
      "patient_id": "5350cd20de8a470aa570a852859ac87e",
      "provider_id": "336159560091471cb6b0e149d9054697",
      "datetime_of_service": "2025-02-21 23:31:45.928071+00:00",
      "note_type": {
        "id": "c5df4f03-58e4-442b-ad6c-0d3dadc6b726",
        "name": "Office visit",
        "coding": {
          "display": "Office Visit",
          "code": "308335008",
          "system": "http://snomed.info/sct"
        }
      }
    }
  ]
}
```

### Read a Note

`GET /plugin-io/api/charting_api_examples/notes/<note-id>/`

#### Example Response

```json
{
  "note": {
    "id": "1490b8db-00a9-47d9-9170-ec142460b586",
    "patient_id": "5350cd20de8a470aa570a852859ac87e",
    "provider_id": "6b33e69474234f299a56d480b03476d3",
    "datetime_of_service": "2025-10-02 23:30:00+00:00",
    "state": "NEW",
    "note_type": {
      "id": "c5df4f03-58e4-442b-ad6c-0d3dadc6b726",
      "name": "Office visit",
      "coding": {
        "display": "Office Visit",
        "code": "308335008",
        "system": "http://snomed.info/sct"
      }
    }
  }
}
```

### Create a Note

`POST /plugin-io/api/charting_api_examples/notes/`

#### Example Request Body

```json
{
  "practice_location_id": "306b19f0-231a-4cd4-ad2d-a55c885fd9f8",
  "note_type_id": "c5df4f03-58e4-442b-ad6c-0d3dadc6b726",
  "patient_id": "5350cd20de8a470aa570a852859ac87e",
  "provider_id": "6b33e69474234f299a56d480b03476d3",
  "datetime_of_service": "2025-10-04 23:30:00",
  "title": "My cool note"
}
```

### Add Billing Line Item to a Note

`POST /plugin-io/api/charting_api_examples/notes/<note-id>/billing_line_items/`

#### Example Request Body

```json
{
  "cpt_code": "98008"
}
```

### Add a Diagnose Command to a Note

`POST /plugin-io/api/charting_api_examples/notes/<note-id>/diagnose/`

`icd10_code` is required, but `committed` may be true, false, or omitted entirely.

#### Example Request Body

```json
{
  "icd10_code": "E119",
  "committed": true
}
```

### Add Multiple Commands to a Note

`POST /plugin-io/api/charting_api_examples/notes/<note-id>/prechart/`

#### Example Request Body

```json
null
```

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "charting_api_examples",
    "description": "A series of custom API routes that showcase SDK charting functionality",
    "components": {
        "protocols": [
            {
                "class": "charting_api_examples.routes.notes:NoteAPI",
                "description": "Endpoints that showcase interactions with notes.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            },
            {
                "class": "charting_api_examples.routes.billing_line_items:BillingLineItemAPI",
                "description": "Endpoints for interacting with billing line items on a note.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            },
            {
                "class": "charting_api_examples.routes.commands:CommandAPI",
                "description": "Endpoints for interacting with commands on a note.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": ["simpleapi-api-key"],
    "tags": {},
    "references": [],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## routes/

### commands.py

This file provides an example of how to define REST API endpoints in a Canvas-based plugin for inserting medical charting commands to clinical notes, with validation, error handling, and support for both single and batch command operations.

**Endpoints**

1. `/notes/<id>/diagnose/` (POST):  
   - Adds a DiagnoseCommand to the specified note.
   - Expects a JSON body with at least an "icd10_code" parameter, and optionally "committed" (boolean).
   - If "committed" is true, the diagnose command is also committed immediately after being originated.
   - Handles missing attribute errors and note-not-found situations gracefully, responding with appropriate error messages and status codes.

2. `/notes/<id>/prechart/` (POST):  
   - Initiates (originates) several commands at once for a note: ReasonForVisitCommand, PhysicalExamCommand, DiagnoseCommand, and PlanCommand.
   - Designed to quickly set up the structure for clinical pre-charting with a single request.

**Implementation Highlights**

- The API is protected with API key authentication via `APIKeyAuthMixin`.
- Uses utility functions (`get_note_from_path_params`, `note_not_found_response`) to locate notes and standardize error responses.
- Returns both command effects (operations that are intended to be executed in the Canvas system) and standard JSON responses.
- Uses status codes according to best practices, addressing Python version differences by using explicit numeric codes where needed.

**Canvas SDK Features Used**

- Commands: `DiagnoseCommand`, `PhysicalExamCommand`, `PlanCommand`, `ReasonForVisitCommand` — each representing an action to be performed on a note.
- Effects: Chainable "originate" (create/begin the command) and "commit" (finalize/commit the command).


```python
from http import HTTPStatus
from uuid import uuid4

from canvas_sdk.commands import (
    DiagnoseCommand,
    PhysicalExamCommand,
    PlanCommand,
    ReasonForVisitCommand,
)
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPI, api
from canvas_sdk.v1.data.note import Note

from charting_api_examples.util import get_note_from_path_params, note_not_found_response


class CommandAPI(APIKeyAuthMixin, SimpleAPI):
    PREFIX = "/notes"

    """
    This shows how you can create an endpoint to insert a particular type of
    command. In this example, it's a diagnose command. It can be committed or
    left uncommitted.

    POST /plugin-io/api/charting_api_examples/notes/<note-id>/diagnose/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    Body: {
        "icd10_code": "E11.9",
        "committed": false
    }
    """
    @api.post("/<id>/diagnose/")
    def add_diagnose_command(self) -> list[Response | Effect]:
        required_attributes = {"icd10_code",}
        request_body = self.request.json()
        missing_attributes = required_attributes - request_body.keys()
        if len(missing_attributes) > 0:
            return [
                JSONResponse(
                    {"error": f"Missing required attribute(s): {', '.join(missing_attributes)}"},
                    # Normally you should use a constant, but this status
                    # code's constant changes in 3.13 from
                    # UNPROCESSABLE_ENTITY to UNPROCESSABLE_CONTENT. Using the
                    # number directly here avoids that future breakage.
                    status_code=422,
                )
            ]

        note = get_note_from_path_params(self.request.path_params)
        if not note:
            return note_not_found_response()

        diagnose_command = DiagnoseCommand(
            note_uuid=str(note.id),
            icd10_code=request_body["icd10_code"].upper(),
        )

        if request_body.get("committed"):
            # To chain command effects, you must know what the command's id
            # is. To accomplish that, we set the id ourselves rather than
            # allow the database to assign one.
            diagnose_command.command_uuid = str(uuid4())
            command_effects = [diagnose_command.originate(), diagnose_command.commit()]
        else:
            command_effects = [diagnose_command.originate()]

        return [
            *command_effects,
            JSONResponse({"message": "Command data accepted for creation"}, status_code=HTTPStatus.ACCEPTED)
        ]

    """
    This shows how you can originate many commands from the same request.

    POST /plugin-io/api/charting_api_examples/notes/<note-id>/prechart/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    Body: {
    }
    """
    @api.post("/<id>/prechart/")
    def add_precharting_commands(self) -> list[Response | Effect]:
        request_body = self.request.json()

        note = get_note_from_path_params(self.request.path_params)
        if not note:
            return note_not_found_response()

        rfv = ReasonForVisitCommand(note_uuid=str(note.id))
        exam = PhysicalExamCommand(note_uuid=str(note.id))
        diagnose = DiagnoseCommand(note_uuid=str(note.id))
        plan = PlanCommand(note_uuid=str(note.id))
        return [
            rfv.originate(),
            exam.originate(),
            diagnose.originate(),
            plan.originate(),
            JSONResponse({"message": "Command data accepted for creation"}, status_code=HTTPStatus.ACCEPTED)
        ]
```

### notes.py

Defines an API endpoint for working with clinical notes. The API supports listing, creating, and retrieving notes, with filtering and pagination features. Authentication is handled through an API key.

**Endpoints**

- **GET /notes/**
  - Returns a paginated list of notes.
  - Supports filters:
    - `patient_id`: Filter notes for a specific patient.
    - `note_type`: Filter by note type (by code or by system|code).
    - `datetime_of_service`, `datetime_of_service__gt`, `datetime_of_service__gte`, `datetime_of_service__lt`, `datetime_of_service__lte`: Date/time based filters.
  - Pagination:
    - `limit`: Number of results (default 10, min 1, max 100).
    - `offset`: Pagination offset (default 0, min 0).
  - If more results exist after the current page, a `next_page` link is included.
  - Returns a JSON object with `notes` (list), `count` (number of notes returned), and `next_page` (URL or None).

- **POST /notes/**
  - Creates a new note.
  - Requires a JSON body with:
    - `note_type_id`, `datetime_of_service` (as string), `patient_id`, `practice_location_id`, `provider_id`, `title`
  - If required fields are missing, returns an error with status 422.
  - Otherwise, initiates note creation and immediately returns an accepted response (`202 Accepted`) with a confirmation message.

- **GET /notes/\<note-id\>/**
  - Returns details for a specific note by its ID.
  - If the note doesn't exist, returns a "not found" response.
  - If found, returns note details, including its state (from `CurrentNoteStateEvent`), patient/provider IDs, datetime, and type info (id, name, coding).

**Helpers and Utilities**

- Uses utilities such as `get_note_from_path_params` and `note_not_found_response` for ID lookup and error handling.
- Uses Django-style ORM filters and queryset slicing.
- Uses the `arrow` library for date parsing.
- All endpoints expect authentication via the `simpleapi-api-key`.


```python
import arrow
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.note import Note as NoteEffect
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPI, api
from canvas_sdk.v1.data.note import Note, CurrentNoteStateEvent

from charting_api_examples.util import get_note_from_path_params, note_not_found_response

class NoteAPI(APIKeyAuthMixin, SimpleAPI):
    PREFIX = "/notes"

    """
    GET /plugin-io/api/charting_api_examples/notes/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    """
    @api.get("/")
    def index(self) -> list[Response | Effect]:
        notes = Note.objects.select_related('patient', 'provider', 'note_type_version').order_by("dbid")
        query_params = self.request.query_params

        # User specified, default 10, min 1, max 100
        limit = min(max(int(query_params.get("limit", 10)), 1), 100)
        # User specified, default 0, min 0, no max
        offset = max(int(query_params.get("offset", 0)), 0)

        if "patient_id" in query_params:
            notes = notes.filter(patient__id=query_params["patient_id"])
        if "note_type" in query_params:
            # You can search by just the code value or you can search by the
            # system and code in the format system|code (e.g
            # http://snomed.info/sct|308335008).
            if "|" in query_params["note_type"]:
                system, code = query_params["note_type"].split("|")
                notes = notes.filter(note_type_version__system=system, note_type_version__code=code)
            else:
                notes = notes.filter(note_type_version__code=query_params["note_type"])
        if "datetime_of_service" in query_params:
            notes = notes.filter(datetime_of_service=query_params["datetime_of_service"])
        if "datetime_of_service__gt" in query_params:
            notes = notes.filter(datetime_of_service__gt=query_params["datetime_of_service__gt"])
        if "datetime_of_service__gte" in query_params:
            notes = notes.filter(datetime_of_service__gte=query_params["datetime_of_service__gte"])
        if "datetime_of_service__lt" in query_params:
            notes = notes.filter(datetime_of_service__lt=query_params["datetime_of_service__lt"])
        if "datetime_of_service__lte" in query_params:
            notes = notes.filter(datetime_of_service__lte=query_params["datetime_of_service__lte"])

        # If there are more results matching the filter after the ones we're
        # returning, provide the link to the next page with the proper offset.
        # If there aren't any more results, return None so the client can tell
        # that there are no more results to fetch.
        link_to_next = None
        if notes[offset+limit:].count() > 0:
            requested_uri = self.context.get("absolute_uri")
            if "offset" in query_params:
                link_to_next = requested_uri.replace(f"offset={offset}", f"offset={offset+limit}")
            else:
                param_separator = "?" if len(query_params) == 0 else "&"
                link_to_next = requested_uri + f"{param_separator}offset={offset+limit}"

        # Apply limit and offset
        notes = notes[offset:offset+limit]

        count = len(notes)
        return [
            JSONResponse({
                "next_page": link_to_next,
                "count": count,
                "notes": [{
                    "id": str(note.id),
                    "patient_id": str(note.patient.id),
                    "provider_id": str(note.provider.id),
                    "datetime_of_service": str(note.datetime_of_service),
                    "note_type": {
                        "id": str(note.note_type_version.id),
                        "name": note.note_type_version.name,
                        "coding": {
                            "display": note.note_type_version.display,
                            "code": note.note_type_version.code,
                            "system": note.note_type_version.system,
                        },
                    },
                } for note in notes]
            })
        ]

    """
    POST /plugin-io/api/charting_api_examples/notes/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    Body: {
		"note_type_id": "c5df4f03-58e4-442b-ad6c-0d3dadc6b726",
        "datetime_of_service": "2025-02-21 23:31:42",
		"patient_id": "5350cd20de8a470aa570a852859ac87e",
		"practice_location_id": "306b19f0-231a-4cd4-ad2d-a55c885fd9f8",
		"provider_id": "6b33e69474234f299a56d480b03476d3",
		"title": "My Note Title",
    }
    """
    @api.post("/")
    def create(self) -> list[Response | Effect]:
        required_attributes = {
            "note_type_id",
            "datetime_of_service",
            "patient_id",
            "practice_location_id",
            "provider_id",
            "title",
        }
        request_body = self.request.json()
        missing_attributes = required_attributes - request_body.keys()
        if len(missing_attributes) > 0:
            return [
                JSONResponse(
                    {"error": f"Missing required attribute(s): {', '.join(missing_attributes)}"},
                    # Normally you should use a constant, but this status
                    # code's constant changes in 3.13 from
                    # UNPROCESSABLE_ENTITY to UNPROCESSABLE_CONTENT. Using the
                    # number directly here avoids that future breakage.
                    status_code=422,
                )
            ]

        note_type_id = request_body["note_type_id"]
        datetime_of_service = arrow.get(request_body["datetime_of_service"]).datetime
        patient_id = request_body["patient_id"]
        practice_location_id = request_body["practice_location_id"]
        provider_id = request_body["provider_id"]
        title = request_body["title"]

        note_effect = NoteEffect(
            note_type_id=note_type_id,
            datetime_of_service=datetime_of_service,
            patient_id=patient_id,
            practice_location_id=practice_location_id,
            provider_id=provider_id,
            title=title,
        )

        return [
            note_effect.create(),
            JSONResponse({"message": "Note data accepted for creation"}, status_code=HTTPStatus.ACCEPTED)
        ]

    """
    GET /plugin-io/api/charting_api_examples/notes/<note-id>/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    """
    @api.get("/<id>/")
    def read(self) -> list[Response | Effect]:
        note = get_note_from_path_params(self.request.path_params)
        if not note:
            return note_not_found_response()

        status_code = HTTPStatus.OK
        current_note_state = CurrentNoteStateEvent.objects.get(note=note).state
        response = {
            "note": {
                "id": str(note.id),
                "patient_id": str(note.patient.id),
                "provider_id": str(note.provider.id),
                "datetime_of_service": str(note.datetime_of_service),
                "state": current_note_state,
                "note_type": {
                    "id": str(note.note_type_version.id),
                    "name": note.note_type_version.name,
                    "coding": {
                        "display": note.note_type_version.display,
                        "code": note.note_type_version.code,
                        "system": note.note_type_version.system,
                    },
                },
            },
        }

        return [JSONResponse(response, status_code=status_code)]
```

### billing_line_items.py

This file defines an API endpoint for adding billing line items (represented by CPT codes) to a note.

**Key Components**

- Imports utility and SDK classes for effects, API handling, and response generation.
- Defines a class, `BillingLineItemAPI`, which inherits API authentication and handling functionalities.
- Registers an HTTP POST endpoint at `/notes/<note-id>/billing_line_items/`.
- Expects an API key in the request header for authentication.
- Expects the request body to be JSON with a "cpt_code" attribute.

```python
from http import HTTPStatus

from canvas_sdk.effects import Effect
from canvas_sdk.effects.billing_line_item import AddBillingLineItem
from canvas_sdk.effects.simple_api import JSONResponse, Response
from canvas_sdk.handlers.simple_api import APIKeyAuthMixin, SimpleAPI, api
from canvas_sdk.v1.data.note import Note

from charting_api_examples.util import get_note_from_path_params, note_not_found_response


class BillingLineItemAPI(APIKeyAuthMixin, SimpleAPI):
    PREFIX = "/notes"

    """
    POST /plugin-io/api/charting_api_examples/notes/<note-id>/billing_line_items/
    Headers: "Authorization <your value for 'simpleapi-api-key'>"
    Body: {
        "cpt_code": "98006"
    }
    """
    @api.post("/<id>/billing_line_items/")
    def add_billing_line_item(self) -> list[Response | Effect]:
        required_attributes = {"cpt_code",}
        request_body = self.request.json()
        missing_attributes = required_attributes - request_body.keys()
        if len(missing_attributes) > 0:
            return [
                JSONResponse(
                    {"error": f"Missing required attribute(s): {', '.join(missing_attributes)}"},
                    # Normally you should use a constant, but this status
                    # code's constant changes in 3.13 from
                    # UNPROCESSABLE_ENTITY to UNPROCESSABLE_CONTENT. Using the
                    # number directly here avoids that future breakage.
                    status_code=422,
                )
            ]

        note = get_note_from_path_params(self.request.path_params)
        if not note:
            return note_not_found_response()

        # To see what else you can do with billing line items, visit our docs:
        # https://docs.canvasmedical.com/sdk/effect-billing-line-items/#adding-a-billing-line-item
        effect = AddBillingLineItem(
            note_id=str(note.id),
            cpt=request_body["cpt_code"],
        )

        return [
            effect.apply(),
            JSONResponse({"message": "Billing line item data accepted for creation"}, status_code=HTTPStatus.ACCEPTED)
        ]
```

## util.py

This file provides utility functions for working with Note objects. The utilities include input validation, standard JSON error responses, and fetching Note objects by ID.


**Function: is_valid_uuid**

This function checks whether a given string is a valid UUID (specifically version 4).  
- Takes a single string argument.
- Returns True if the string is a properly formatted version 4 UUID, False otherwise.


**Function: note_not_found_response**

This function returns a standardized JSON error response indicating that a requested Note was not found.  
- Uses JSONResponse from the SDK.
- Sets the response status to HTTP 404 (NOT FOUND) and the body to {"error": "Note not found."}.


**Function: get_note_from_path_params**

This function attempts to retrieve a Note object using a dictionary of path parameters.  
- Extracts the "id" from path_params.
- Validates the ID as a UUID using is_valid_uuid.
- If invalid, returns None.
- If valid, attempts to retrieve a Note object with the given ID (using Note.objects.get).
- If the Note does not exist, catches the DoesNotExist exception and returns None.
- Returns the Note object if found, or None if not found/invalid.


**Imports and External Dependencies**

- uuid.UUID: For validating UUIDs.
- http.HTTPStatus: For standardized HTTP status codes.
- canvas_sdk.effects.simple_api.JSONResponse: For returning consistent API responses.
- canvas_sdk.v1.data.note.Note: For interacting with Note objects from the Canvas SDK.

```python
from uuid import UUID
from http import HTTPStatus

from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data.note import Note


def is_valid_uuid(possible_uuid):
    try:
        uuid_obj = UUID(possible_uuid, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == possible_uuid


def note_not_found_response():
    return JSONResponse(
        {"error": "Note not found."},
        status_code=HTTPStatus.NOT_FOUND,
    )


def get_note_from_path_params(path_params) -> Note | None:
    note_id = path_params["id"]
    # Ensure the note id is a valid UUID
    if not is_valid_uuid(note_id):
        return None

    try:
        note = Note.objects.get(id=note_id)
    except (Note.DoesNotExist):
        return None
    return note
```

<br/>
<br/>
<br/>
