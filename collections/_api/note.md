---
title: Note
layout: apipage
---

This API allows customers to create and update notes. The effect of creating a note is the same as creating a note in the user interface (for example for a note with category “encounter” will create an encounter, a note that is billable will create a claim). Not all note attributes can be modified on update. For example, note type cannot be changed after note creation.

## Authentication
The Note API uses the existing OAuth authentication flow from the FHIR API, so you can simply post to the existing auth token endpoint /auth/token/

New scopes are introduced: user/Note.read and user/Note.write. These scopes will not be in OAuth applications that were created prior to the release of this feature. Therefore to get access, you have two options:

- Create a new [OAuth application](/api/customer-authentication)
- Ask Canvas to add the new scopes to an existing OAuth application 

{:refdef: style="text-align: center;"}
![description](/assets/images/allowed-scopes.png){:width="70%"}
{: refdef}


``` python
import requests

url = "https://<your-instance>.canvasmedical.com/auth/token/"

payload = 'grant_type=client_credentials&client_id=canvas&client_secret=canvas'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

<br>
Then use your token in the request headers as you do with the FHIR API:

{:refdef: style="text-align: center;"}
![description](/assets/images/note-api-token.png){:width="100%"}
{: refdef}


<br>

## Create
To create a Note resource, POST to `https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note` using the supported attributes below. Notes will be created with the state “NEW” by default.

### Attributes


<b>`title`</b> text<br>
The user-defined title of the Note.

***

<b>`encounterStartTime`</b> datetime<br>
The datetime of the encounter. This will display in the datetimeOfService.

***

<b>`patientKey`</b> text<br>
The unique key of the Patient for which this Note is written.

***

<b>`providerKey`</b> text<br>
The unique key of the Provider staff who is writing the Note.

***

<b>`practiceLocationKey`</b> text<br>
The unique key of the PracticeLocation for which this Note is written.

***

<b>`noteTypeName text`</b><br>
Represents the note type in a human-readable format.

***

<b>`noteTypeSystem`</b> text<br>
Defines a coding system for the note type, to be used with the paired noteTypeCoding.

***

<b>`noteTypeCoding`</b> text<br>
Defines a code for the note type, to be used with the paired noteTypeSystem.

### Example
``` python
import requests
import json

url = "https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note"

payload = json.dumps({
  "title": "Some Custom Title",
  "noteTypeName": "Office visit",
  "patientKey": "8d84776879de49518a4bc3bb81d96dd4",
  "providerKey": "5eede137ecfe4124b8b773040e33be14",
  "practiceLocationKey": "c67e0c59-d4d2-428c-bc13-b6e85d181ad0",
  "encounterStartTime": "2023-11-28T19:00:00.016852Z"
})
headers = {
  'Authorization': 'Bearer HqFtbSnBNX4S65VhRrg8sRxO6XcSFp',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

<br>

## Read
To read a Note resource, request a GET from <br>
`https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note/{noteKey}`

### Attributes

<b>`noteKey`</b> string<br>
The unique key of the Note.

***

<b>`title`</b> text<br>
The user-defined title of the Note.

***

<b>`datetimeOfService`</b> datetime<br>
The datetime of the service, as defined as encounter start time for encounters, appointment datetime for appointments, or the created datetime for other note types.

***

<b>`titleDisplay`</b> text<br>
Represents the computed title of the Note, as displayed in the UI. If a user-defined title is not provided, this defaults to other display logic.

***

<b>`currentState`</b> text<br>
The most recent state of the Note.

***

<b>`patientKey`</b> text<br>
The unique key of the Patient for which this Note was written.

***

<b>`providerKey`</b> text<br>
The unique key of the Provider staff who wrote the Note.

***

<b>`practiceLocationKey`</b> text<br>
The unique key of the PracticeLocation for which this Note was written.

***

<b>`noteTypeName text`</b><br>
Represents the note type in a human-readable format.

***

<b>`noteTypeSystem`</b> text<br>
Defines a coding system for the note type, to be used with the paired noteTypeCoding.

***

<b>`noteTypeCoding`</b> text<br>
Defines a code for the note type, to be used with the paired noteTypeSystem.

### Example
```python
import requests

url = "https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note/4a6064e9-293c-4541-b1cc-515f81435e74"

payload = ""
headers = {
  'Authorization': 'Bearer QdPhY9QLIs4zlawv5UG42JDASGqX0l'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
<br>

## Update
To update an existing Note resource, `PATCH` to <br>
`https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note/{noteKey}` 
<br> using any of the following allowed attributes. 

### Attributes

<b>`title`</b> text<br>
The user-defined title of the Note.

***

<b>`providerKey`</b> text<br>
The unique key of the Provider staff who is writing the Note.

***

<b>`practiceLocationKey`</b> text<br>
The unique key of the PracticeLocation for which this Note is written.

***

<b>`stateChange`</b> text <br>
The new note state to be set. Allowed transitions in v1 include:

Locking an unlocked note (excluding DATA notes)<br>
“ULK” → “LKD”, “NEW” → “LKD”, “CVD” → “LKD”<br><br>
Unlocking a locked note (excluding DATA notes)<br>
“LKD” → “ULK”<br><br>
Marking an appointment as a no show <br>
"BKD" → "NSW" & "RVT" → "NSW"<br><br>
Checking in an appointment<br>
"BKD" → "CVD", "NSW" → "CVD", "RVT" → "CVD"

### Example

``` python
import requests
import json

url = "https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note/4a6064e9-293c-4541-b1cc-515f81435e74"

payload = json.dumps({
  "stateChange": "LKD",
  "providerKey": "4150cd20de8a470aa570a852859ac87e",
  "practiceLocationKey": "c67e0c59-d4d2-428c-bc13-b6e85d181ad0",
  "title": "New Custom Title"
})
headers = {
  'Authorization': 'Bearer QdPhY9QLIs4zlawv5UG42JDASGqX0l',
  'Content-Type': 'application/json'
}

response = requests.request("PATCH", url, headers=headers, data=payload)

print(response.text)
```


<br>

## Search
To search for Note resources, request a `GET` from <br>
`https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note` <br>and append your search criteria as URL parameters. 

### Query Params
**patient_key** text 
filters to this patient’s notes only

**provider_key** text
filters to this provider’s notes only

**note_type_name** text
filters to this type of note (human-readable)

**note_type_system** and **note_type_coding** text
filters to this type of note with system/code pair

**datetime_of_service** datetime
filters the service datetime with the following options:
- = (exact)
- lte (less than or equal to)
- gte (greater than or equal to)
- lt (less than)
- gt (greater than)

`&datetime_of_service__gte=2023-12-06T19:10:56.115532Z`

### Pagination
To paginate your requests, simply add a limit query parameter, e.g. `GET` from `https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note?limit=10`. You can also page through the results with the offset parameter, e.g. `https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note?limit=10&offset=10`. The response will include a record count, as well as **next**, and **previous** URLs for convenience, and the note data will be contained in the **results** value.

### Ordering
To order your results, simply add an ordering query parameter, e.g. `GET` from `https://<your-instance>.canvasmedical.com/core/api/notes/v1/Note?ordering=datetime_of_service`. To reverse the sort order, prepend the field with a hyphen, e.g. `?ordering=-datetime_of_service`. Available ordering fields include:
- created (the datetime the note was created)
- modified (the datetime the note was last updated)
- datetime_of_service (the datetime of the actual service associated with the note)

### Example

``` python
import requests

url = "https://<your_instance>.canvasmedical.com/core/api/notes/v1/Note?patient_key=8d84776879de49518a4bc3bb81d96dd4&note_type_name=Office%20visit"

payload = ""
headers = {
  'Authorization': 'Bearer QdPhY9QLIs4zlawv5UG42JDASGqX0l'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
