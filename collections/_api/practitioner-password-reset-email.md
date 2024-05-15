---
layout: apipage
title: Send reset password email to Practitioner
date: 2024-05-15
---
## send-reset-password-email

Send reset password email to Practitioner by the given ID.<br><br>
This endpoint is a [FHIR operation](https://hl7.org/fhir/R4/operations.html), so it accepts a [Parameters](https://hl7.org/fhir/R4/parameters.html) resource in the request body. It doesn't accept any specific parameters but requires a payload that states the resource type. See the request example for more detail.

The bearer token included in requests send to this endpoint must have one of the following scopes:


- `system/Staff.send-reset-password-email`
- `user/Staff.send-reset-password-email`


{% tabs send-reset-password-to-practitioner %}
{% tab send-reset-password-to-practitioner curl %}
```shell
curl --request POST \
     --url 'https://fumage-example.canvasmedical.com/Practitioner/<id>/$send-reset-password-email' \
     --header 'Authorization: Bearer <token>' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
    "resourceType": "Parameters"
}'
```

{% endtab %}
{% tab send-reset-password-to-practitioner python %}

```python
import requests

url = "https://fumage-example.canvasmedical.com/Practitioner/<id>/$send-reset-password-email"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}

payload = {
    "resourceType": "Parameters"
}
response = requests.put(url, json=payload, headers=headers)

print(response.text)
```
{% endtab %}
  {% endtabs %}




