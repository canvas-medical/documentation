---
layout: apipage
title: DocumentReference Operations
date: 2024-10-14
---
## upload-document

Upload a document via API, without parsing.<br><br>
This endpoint is a [FHIR operation](https://hl7.org/fhir/R4/operations.html), so it accepts a [Parameters](https://hl7.org/fhir/R4/parameters.html) resource in the request body. It will accept exactly one `parameter`, which represents one file to be uploaded. The parameter must have a `name`. The file that will be uploaded is provided as a `valueAttachment` with the `contentType` of `application/pdf`, and `data` must be a base64 encoded string. See the request example for more detail.

The bearer token included in requests send to this endpoint must have one of the following scopes:


- `system/DocumentReference.upload-document`
- `user/DocumentReference.upload-document`


{% tabs upload-document %}
{% tab upload-document curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/DocumentReference/$upload-document' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "UploadDocument",
            "valueAttachment": {
                "contentType": "application/pdf",
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+brikolaz",
            },
        }
    ],
}'
```

{% endtab %}
{% tab upload-document python %}

```python
import requests

url = "https://fumage-example.canvasmedical.com/DocumentReference/$upload-document"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "UploadDocument",
            "valueAttachment": {
                "contentType": "application/pdf",
                "data": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+brikolaz",
            },
        }
    ],
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
  {% endtabs %}




