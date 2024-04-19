---
title: "Submit a Full Vital Panel through Canvas FHIR API"
guide_for:
- /api/observation/
---

Inside of the Canvas' [Vital Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs) there are many vital signs supported to document. 

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/vital-empty.png){:width="70%"}
{: refdef}

The Canvas [FHIR Observation Create](/api/observation/#create) endpoint supports writing some of the vital signs in the command. This guide will show you all the vitals that can be documented in the Create interaction.

<br>

* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Create a vital panel via FHIR
2. Submit various vital signs into the same panel via FHIR
3. Perform a FHIR Observation Search to view the completed panel
<br>

* * *

### 1. Setup and Authentication

This guide will demonstrate many FHIR API calls into Canvas. Before we can make a FHIR request, we need to setup some imports, reusable variables, and authenticate into the instance we want to work with. 

Here is your starting point:
```python
import requests
url = "https://fumage-example.canvasmedical.com/Observation"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "content-type": "application/json"
}
```

But there are two places above to update:

1. The `url` will show `https://fumage-example.canvasmedical.com/Observation`. You will need to replace `example` with the name of the Canvas instance you are using. 

2. One of the `header` elements will be `'Authorization': 'Bearer <token>'`. You will need to create this `<token>` following our steps laid out in [Customer Authentication](/api/customer-authentication)


### 2. Understanding our Observation Payload

Before we start creating the vital panel and the associated vital signs, take some time to familiarize yourself with the [FHIR Observation Create](/api/observation/#create) endpoint. Each payload to create an observation requires `status`, `code`, and `subject`. 

In this guide the `status` will always be `final` and the `subject` will always appear as: <br>`"subject": { "reference": "Patient/$patient_id" }`.<br>When completing these steps yourself, you will want to change the `{patient_id}` to match a patient in the instance you are using (e.g `"Patient/ee8672f3497e4a83937b9e71d0a704a5"`).

The `code` attribute is the real magic that tells Canvas which vital you are creating. The coding will always be a LOINC code. 

Another thing to note is an optional `effectiveDateTime` attribute. This allows you to specify the time the vital was taken. But if omitted, it will default to the time of creation. 

### 3. Create a Vital Panel

First we will need to create the panel object to be able to save all the individual vital signs to. The important attribute is the `code.coding[0][code]` being `85353-1` to represent a vital panel. 

Here is the payload for how to create a Vital Panel (remember to set the patient_id and also update the effectiveDateTime):

```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85353-1",
                "display": "Vital Panel"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00"
}

response = requests.post(url, json=payload, headers=headers)
```

On a successful create, when the `response.status_code` equal 201. We can fetch the ID of the newly created observation in the `response.headers['location']` attribute. The value will always be in the format `{url}/{id}/_history/1`. We need to extract the `id` from the value. 

However, if the request failed it will throw an error to see what went wrong. It will also display the Correlation ID that can be given to Customer Support for help with further debugging.

```python
if response.status_code == 201:
    panel_id = response.headers['location'].replace(f"{url.replace('https', 'http')}/", '').replace('/_history/1', '')
else:
    raise Exception(f"Failed to perform {response.url}. \n Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be a Data Import note placed on that patient's timeline based on the date passed in the `effectiveDateTime` attribute with an empty Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/vital-panel-in-import-note.png){:width="80%"}
{: refdef}



### 4. Creating Individual Vital Signs

Now that we have created a Vital Panel, we will be able to use this panel_id when creating the individual vital signs to be associated with the same command by passing the `derivedFrom` attribute in the payload:
```python
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
``` 

Now we are ready to create the following vital signs in the panel that are supported via FHIR Observation Create:

- Height  
- Weight  
- Waist Circumference  
- Body Temperature  
- Blood Pressure  
- Pulse Rhythm  
- Pulse Rate  
- Respiration Rate  
- Oxygen Saturation  
- Notes  

#### Add Height

Height is denoted by the LOINC code `8302-2`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. By default if no `valueQuantity.unit` is specified, it will default to using inches, but `cm` is also supported, it will just convert it to inches on the UI and when a Read/Search is performed. 

Here is a payload to create a height of 69.0 inches:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8302-2",
                "display": "Height"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 69.0,
        "unit": "in",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Height observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be height of `69.0 in` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/height.png){:width="80%"}
{: refdef}

#### Add Weight

Weight is denoted by the LOINC code `29463-7`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. By default if no `valueQuantity.unit` is specified, it will default to using ounces, but `lb` or `kg` is also supported, it will just convert it to `oz` when a Read/Search is performed. The UI will display it in `lbs` and leftover `oz`.

Here is a payload to create a weight of 176.4 lbs:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "29463-7",
                "display": "Weight"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 176.4,
        "unit": "lb",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Weight observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be weight of `176 lbs 6.4 oz` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/weight.png){:width="80%"}
{: refdef}

#### Add Waist Circumference

Waist Circumference is denoted by the LOINC code `29463-7`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. By default if no `valueQuantity.unit` is specified, it will default to using centimeters, but `in` is also supported, it will just convert it to `cm` on the UI or when a Read/Search is performed.

Here is a payload to create a waist circumference of `98.2 cm`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "56086-2",
                "display": "Waist Circumference"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 98.2,
        "unit": "cm",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Waist Circumference observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be waist circumference of `98.2 cm` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/waist-circumference.png){:width="80%"}
{: refdef}

#### Add Body Temperature

Body Temperature is denoted by the LOINC code `8310-5`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. The only unit accepted for body temperature is `°F` and if omitted it will be default. 

Here is a payload to create a temperature of `98.4 °F`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8310-5",
                "display": "Body Temperature"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 98.4,
        "unit": "°F",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Body Temperature observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be temperature of `98.4 °F` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/body-temperature.png){:width="80%"}
{: refdef}

#### Add Blood Pressure

Blood Pressure is denoted by the LOINC code `85354-9`. In the Vital's command blood pressure is a string value that combines the systolic and diastolic components with a `/`. So the payload will pass the `valueString` component in order for the blood pressure to appear correctly in the Vitals Command. 

Since blood pressure is made up of two values, the payload will also define a `component` attribute list to pass the systolic (LOINC code `8480-6`) and diastolic (LOINC code `8462-4`) values. These two values are numeric, so they will have the `valueQuantity` attributes where the unit will be `mmHg`

Here is a payload to create a Blood Pressure of `122/68`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood Pressure"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueString": "122/68",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic blood pressure"
                    }
                ]
            },
            "valueQuantity": {
                "value": 122,
                "unit": "mmHg"
            }
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic blood pressure"
                    }
                ]
            },
            "valueQuantity": {
                "value": 68,
                "unit": "mmHg"
            }
        }
    ],
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Blood Pressure observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be blood pressure of `122/68` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/blood-pressure.png){:width="80%"}
{: refdef}

#### Add Pulse Rate

Pulse Rate is denoted by the LOINC code `8867-4`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. The only unit accepted for pulse rate is `bpm` and if omitted it will be default.

Here is a payload to create a pulse rate of `115 bpm`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8867-4",
                "display": "Pulse"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 115,
        "unit": "bpm",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Pulse Rate observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be pulse rate of `115 bpm` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/pulse-rate.png){:width="80%"}
{: refdef}

#### Add Pulse Rhythm

Pulse Rhythm is denoted by the LOINC code `8884-9`. Canvas accepts only three different string values for pulse rhythm: `Regular`, `Irregularly Irregular`, or `Regulary Irregular`. This value will be passed in the `valueString` attribute. 

Here is a payload to create a pulse rhythm of `Regular`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "8884-9",
                "display": "Pulse Rhythm"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueString": "Regular",
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Pulse rhythm observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be pulse rhythm of `Regular` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/pulse-rhythm.png){:width="80%"}
{: refdef}

#### Add Respiration Rate

Respiration Rate is denoted by the LOINC code `9279-1`. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. The only unit accepted for respiration rate is `bpm` and if omitted it will be default.

Here is a payload to create a respiration rate of `15 bpm`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "9279-1",
                "display": "Respiration Rate"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 15,
        "unit": "bpm",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Respiration Rate observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be respiration rate of `15 bpm` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/respiration-rate.png){:width="80%"}
{: refdef}

#### Add Oxygen Saturation

Oxygen Saturation is denoted by either LOINC code `2708-6` or `59408-5`. Canvas saves the oxygen saturation with both codings. Since its value is numeric, we will be able to pass the value and units through the `valueQuantity` attribute. The only unit accepted for Oxygen Saturation is `%` and if omitted it will be default.

Here is a payload to create a Oxygen Saturation of `98%`:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "2708-6",
                "display": "Oxygen Saturation Arterial"
            },
            {
                "system": "http://loinc.org",
                "code": "59408-5",
                "display": "Oxygen Saturation"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueQuantity": {
        "value": 98,
        "unit": "%",
    },
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Oxygen Saturation observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now be Oxygen Saturation of `98%` added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/oxygen-saturation.png){:width="80%"}
{: refdef}

#### Add Notes

Adding a Note is denoted by the LOINC code `80339-5`. Since this value is free text, a `valueString` attribute can be used. 

Here is a payload to create an internal Note:
```python
payload = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "80339-5",
                "display": "Note"
            }
        ]
    },
    "subject": {
        "reference": f"Patient/{patient_id}"
    },
    "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
    "valueString": "Last Blood sugar was 78",
    "derivedFrom": [
        {
            "reference": f"Observation/{panel_id}",
            "type": "Observation"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
if response.status_code == 201:
    print(f"Oxygen Saturation observation id = {response.headers['location'].replace(f'{url}/', '').replace('/_history/1', '')}")
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

Looking in the Canvas UI, there will now will be a Note added in that Vitals Command:

{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/vitals/note.png){:width="80%"}
{: refdef}

### 5. Perform FHIR Observation Read and Search

A full Vital Panel has been completed! Let's now perform a FHIR Observation Read using the `panel_id` to see all the observation members of this panel now: 

```python
from pprint import pprint
response = requests.get(f"{url}/{panel_id}", headers=headers)
if response.status_code == 200:
    pprint(response.json())
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

The output will look like:
```json
{
    "resourceType": "Observation",
    "id": "b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "Vital Signs"
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "85353-1",
                "display": "Vital Signs Panel"
            }
        ]
    },
    "subject": {
        "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
        "type": "Patient"
    },
    "effectiveDateTime": "2024-03-27T10:00:00+00:00",
    "issued": "2024-03-27T21:35:12.364027+00:00",
    "dataAbsentReason": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                "code": "not-performed",
                "display": "Not Performed"
            }
        ]
    },
    "hasMember": [
        {
            "reference": "Observation/f8facb98-b0c3-4ddc-9fad-a9a92306b04f",
            "type": "Observation"
        },
        {
            "reference": "Observation/99308606-14f8-477a-9f15-8f4b93eba560",
            "type": "Observation"
        },
        {
            "reference": "Observation/e816f764-a2b6-470d-95b0-24b5bcb10377",
            "type": "Observation"
        },
        {
            "reference": "Observation/b804767c-b713-4b5f-a61a-51fa53312807",
            "type": "Observation"
        },
        {
            "reference": "Observation/b0289af9-77c4-4d9d-8bb6-a5e860018193",
            "type": "Observation"
        },
        {
            "reference": "Observation/0deed76f-8354-459d-b2eb-58e185276b51",
            "type": "Observation"
        },
        {
            "reference": "Observation/b3b8ac48-c114-4db4-8c5a-9d856e91a5e2",
            "type": "Observation"
        },
        {
            "reference": "Observation/c745b8bd-0d2e-4145-95b6-bdc467a78584",
            "type": "Observation"
        },
        {
            "reference": "Observation/03fa41bd-37d3-42d8-b5b9-2ccf4f3bf85f",
            "type": "Observation"
        },
        {
            "reference": "Observation/29dcfac3-259f-489a-b8b6-b351c0574270",
            "type": "Observation"
        }
    ]
}
```

And finally let's perform a FHIR Observation Search to see all the vital signs that are for that patient using the derived from search parameter:

```python
from pprint import pprint
response = requests.get(f"{url}?patient=Patient/{patient_id}&category=http://terminology.hl7.org/CodeSystem/observation-category|vital-signs&derived-from=Observation/{panel_id}&_count=20", headers=headers)
if response.status_code == 200:
    pprint(response.json())
else:
    raise Exception(f"Failed to perform {response.url}. \n Fumage Correlation ID: {response.headers['fumage-correlation-id']} \n {response.text}")
```

The response will look like: 

```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 11,
    "link": [
        {
            "relation": "self",
            "url": "/Observation?patient=Patient%2Fcc95008fad96426e8e6d15e2811b8318&category=http%3A%2F%2Fterminology.hl7.org%2FCodeSystem%2Fobservation-category%7Cvital-signs&_count=50&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Observation?patient=Patient%2Fcc95008fad96426e8e6d15e2811b8318&category=http%3A%2F%2Fterminology.hl7.org%2FCodeSystem%2Fobservation-category%7Cvital-signs&_count=50&_offset=0"
        },
        {
            "relation": "last",
            "url": "/Observation?patient=Patient%2Fcc95008fad96426e8e6d15e2811b8318&category=http%3A%2F%2Fterminology.hl7.org%2FCodeSystem%2Fobservation-category%7Cvital-signs&_count=50&_offset=0"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Observation",
                "id": "f8facb98-b0c3-4ddc-9fad-a9a92306b04f",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8302-2",
                            "display": "Height"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T16:35:01.626082+00:00",
                "valueQuantity": {
                    "value": 69.0,
                    "unit": "in",
                    "system": "http://unitsofmeasure.org",
                    "code": "[in_i]"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "99308606-14f8-477a-9f15-8f4b93eba560",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "29463-7",
                            "display": "Weight"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T17:28:15.964593+00:00",
                "valueQuantity": {
                    "value": 176.4,
                    "unit": "lb",
                    "system": "http://unitsofmeasure.org",
                    "code": "[lb_av]"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "e816f764-a2b6-470d-95b0-24b5bcb10377",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "85354-9",
                            "display": "Blood Pressure"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T17:58:41.765214+00:00",
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ],
                "component": [
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "8480-6",
                                    "display": "Systolic blood pressure"
                                }
                            ]
                        },
                        "valueQuantity": {
                            "value": 122.0,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "8462-4",
                                    "display": "Diastolic blood pressure"
                                }
                            ]
                        },
                        "valueQuantity": {
                            "value": 68.0,
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "b804767c-b713-4b5f-a61a-51fa53312807",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8867-4",
                            "display": "Pulse"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T18:05:35.559963+00:00",
                "valueQuantity": {
                    "value": 115.0,
                    "unit": "bpm",
                    "system": "http://unitsofmeasure.org",
                    "code": "/min"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "85353-1",
                            "display": "Vital Signs Panel"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-27T10:00:00+00:00",
                "issued": "2024-03-27T21:35:12.364027+00:00",
                "dataAbsentReason": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/data-absent-reason",
                            "code": "not-performed",
                            "display": "Not Performed"
                        }
                    ]
                },
                "hasMember": [
                    {
                        "reference": "Observation/f8facb98-b0c3-4ddc-9fad-a9a92306b04f",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/99308606-14f8-477a-9f15-8f4b93eba560",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/e816f764-a2b6-470d-95b0-24b5bcb10377",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/b804767c-b713-4b5f-a61a-51fa53312807",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/b0289af9-77c4-4d9d-8bb6-a5e860018193",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/0deed76f-8354-459d-b2eb-58e185276b51",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/b3b8ac48-c114-4db4-8c5a-9d856e91a5e2",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/c745b8bd-0d2e-4145-95b6-bdc467a78584",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/03fa41bd-37d3-42d8-b5b9-2ccf4f3bf85f",
                        "type": "Observation"
                    },
                    {
                        "reference": "Observation/29dcfac3-259f-489a-b8b6-b351c0574270",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "b0289af9-77c4-4d9d-8bb6-a5e860018193",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "56086-2",
                            "display": "Waist Circumference"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T17:35:36.431581+00:00",
                "valueQuantity": {
                    "value": 98.2,
                    "unit": "cm",
                    "system": "http://unitsofmeasure.org",
                    "code": "cm"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "0deed76f-8354-459d-b2eb-58e185276b51",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8884-9",
                            "display": "Pulse Rhythm"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T18:32:13.486363+00:00",
                "valueString": "Regular",
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "b3b8ac48-c114-4db4-8c5a-9d856e91a5e2",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "9279-1",
                            "display": "Respiration Rate"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T18:35:48.662967+00:00",
                "valueQuantity": {
                    "value": 15.0,
                    "unit": "bpm",
                    "system": "http://unitsofmeasure.org",
                    "code": "/min"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "c745b8bd-0d2e-4145-95b6-bdc467a78584",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "2708-6",
                            "display": "Oxygen Saturation Arterial"
                        },
                        {
                            "system": "http://loinc.org",
                            "code": "59408-5",
                            "display": "Oxygen Saturation"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T18:48:39.269569+00:00",
                "valueQuantity": {
                    "value": 98.0,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "03fa41bd-37d3-42d8-b5b9-2ccf4f3bf85f",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8310-5",
                            "display": "Body Temperature"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T17:41:05.882156+00:00",
                "valueQuantity": {
                    "value": 98.4,
                    "unit": "°F",
                    "system": "http://unitsofmeasure.org",
                    "code": "[degF]"
                },
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "29dcfac3-259f-489a-b8b6-b351c0574270",
                "status": "final",
                "category": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                                "code": "vital-signs",
                                "display": "Vital Signs"
                            }
                        ]
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "80339-5",
                            "display": "Note"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/cc95008fad96426e8e6d15e2811b8318",
                    "type": "Patient"
                },
                "effectiveDateTime": "2024-03-29T08:50:24.883809+00:00",
                "issued": "2024-03-28T18:57:56.444652+00:00",
                "valueString": "Last Blood sugar was 78",
                "derivedFrom": [
                    {
                        "reference": "Observation/b7beaf7f-7c5b-4129-9c0a-8c67ddde4d98",
                        "type": "Observation"
                    }
                ]
            }
        }
    ]
}
```
