---
title: Letter
layout: apipage
---

This API allows customers to create letters. The effect of creating a letter is the same as creating a letter in the user interface. Content can be added using HTML & CSS. Placeholders created in Canvas will not be respected. 

## Authentication
The Letter API uses the existing Canvas OAuth authentication flow, so you can simply post to the existing auth token endpoint /auth/token/

This endpoint was built as an addition to the note API and uses the user/Note.write scope. This scope will not be in OAuth applications that were created prior to the release of the Notes API.  To get access:

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
To create a Note resource, POST to `https://<your-instance>.canvasmedical.com/core/api/letter/v1/Letter` using the supported attributes below. Letters will be staged on the patient's chart to then be faxed or printed. Furhter edits can be made in the UI as needed. 

### Attributes



<b>`patientKey`</b> text<br>
The unique key of the Patient for which this letter is written.

***

<b>`providerKey`</b> text<br>
The unique key of the Provider staff who is responsible for the letter.

***

<b>`practiceLocationKey`</b> text<br>
The unique key of the PracticeLocation for which this letter is written.

***

<b>`content`</b><br>
The contents of the letter. Supports HTML & CSS. 



### Example
``` python
import requests
import json

url = "https://<your-instance>.canvasmedical.com/core/api/letter/v1/Letter"

payload = json.dumps({
  "patientKey": "8d84776879de49518a4bc3bb81d96dd4",
  "providerKey": "5eede137ecfe4124b8b773040e33be14",
  "practiceLocationKey": "c67e0c59-d4d2-428c-bc13-b6e85d181ad0",
  "content": "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Jury Excuse Letter</title><style>body { font-family: Arial, sans-serif; margin: 20px; padding: 0; background-color: #f4f4f4; }.container { max-width: 600px; margin: auto; background: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }.header { text-align: center; }.content { margin-top: 20px; }.signature { margin-top: 30px; text-align: left; }.footer { margin-top: 30px; text-align: center; font-size: 0.9em; color: #555; }</style></head><body><div class=\"container\"><div class=\"header\"><h1>Jury Excuse Letter</h1></div><div class=\"content\"><p>To Whom It May Concern,</p><p>Letty Letters is a patient of mine at PRACTICE NAME. Due to a current medical condition, the patient is unable to fulfill the requirements for jury duty.</p><p>Thanks,</p></div><div class=\"signature\"><img src=\"https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Zhu_Zhengting_signature.jpg/1280px-Zhu_Zhengting_signature.jpg\" alt=\"Signature\" width=\"200\"></div></div></body></html>"
})
headers = {
  'Authorization': 'Bearer HqFtbSnBNX4S65VhRrg8sRxO6XcSFp',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```




