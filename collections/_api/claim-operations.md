---
layout: apipage
title: Claim Operations 
date: 2023-02-12
---
## add-activity-log-item

Add an activity log item to a Claim.<br><br>
This endpoint is a [FHIR operation](https://hl7.org/fhir/R4/operations.html), so it accepts a [Parameters](https://hl7.org/fhir/R4/parameters.html) resource in the request body. It will accept one and only one parameter, which must have the name **comment**. The comment that will be added is provided as a `valueString`. See the request example for more detail.

The bearer token included in requests send to this endpoint must have one of the following scopes:


- `system/Claim.add-activity-log-item`
- `user/Claim.add-activity-log-item`





{% tabs claim-operations %}
{% tab claim-operations curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Claim/<id>/$add-activity-log-item' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "comment",
            "valueString": "Test comment"
        }
    ]
}'
```

{% endtab %}
{% tab claim-operations python %}

```python
import requests

url = "https://fumage-example.canvasmedical.com/Claim/<id>/$add-activity-log-item"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Parameters",
    "parameter": [
        {
            "name": "comment",
            "valueString": "Test comment"
        }
    ]
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
  {% endtabs %}




