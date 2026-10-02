---
title: "Quickstart"
layout: apipage
---
<!-- source: discussion #1355 -->
<!-- source: discussion #784 -->
## Base URL and finding your sandbox name

FHIR API requests must be made against the `fumage-` subdomain for your instance, using the pattern `https://fumage-<sandbox-name>.canvasmedical.com`. The `<sandbox-name>` is the same name that appears in the URL when you log in to your Canvas instance (e.g. for `https://example-dev.canvasmedical.com` the sandbox name is `example-dev`, and the FHIR base URL is `https://fumage-example-dev.canvasmedical.com`).

The regular instance subdomain (`https://<sandbox-name>.canvasmedical.com`) does not serve FHIR endpoints — requests there return HTML 404 pages rather than FHIR responses. The FHIR API is available on development environments as well, with no additional provisioning required beyond OAuth client credentials.

If you do not have your own instance yet, hobbyists and developers can use the shared `xpc-dev` developer sandbox, which has a FHIR base URL of `https://fumage-xpc-dev.canvasmedical.com`.

## Authentication

To access our FHIR API, you will need to request an access token and refresh it periodically. You can refer to our [Authentication Documentation](/api/customer-authentication) and [Authentication Best Practices](/api/authentication-best-practices) to get you set up. Access tokens expire 10 hours after they are created. You can and should reuse access tokens to reduce the number of tokens that are valid at any given time.

<!-- source: discussion #1566 -->
{% include alert.html type="info" content="The OAuth token endpoint (<code>/auth/token/</code>) lives on the regular instance host, not the fumage- FHIR host. Request tokens from <code>https://&lt;sandbox-name&gt;.canvasmedical.com/auth/token/</code> — requesting them against the fumage- subdomain returns a <code>Not Found</code> error. The legacy Notes API (<code>/core/api/notes/v1/Note</code>) is also served from the regular instance host, not the fumage- host. That Notes API is deprecated; use the Plugin SDK (for example the <a href='/sdk/effect-notes/'>Note effect</a>) to create and manage notes instead." %}

<!-- source: discussion #1532 -->
{% include alert.html type="info" content="There are currently no fixed rate limits on the FHIR API or on SDK SimpleAPI endpoints. However, because FHIR requests are served by your underlying Canvas instance, very high-volume polling can affect the stability of that instance. Caching access tokens and using webhooks instead of polling are recommended to keep request volume manageable." %}

## Create a patient

Let's start by creating a patient. we've gone ahead and generated some boilerplate Patient info that includes all of the minimum required parameters for a Create a Patient request. 

```shell
curl -i --location 'https://fumage-<sandbox-name>.canvasmedical.com/Patient' \
     --header 'Authorization: Bearer <bearer-token>' \
     --header 'Content-Type: application/json' \
     --data '{
        "resourceType": "Patient",
        "extension": [
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                "valueCode": "F"
            }
        ],
        "gender": "female",
        "active": true,
        "name": [
            {
                "use": "official",
                "family": "Mitko",
                "given": [
                    "Salina"
                ]
            }
        ],
        "birthDate": "1949-11-13"
    }'
```



To execute this command, first:

Replace <sandbox-name> with your sandbox name  
Replace <bearer-token> with your Bearer token you learned about above in the Authentication Section  
Hit enter and your first patient, Salina Mitko, is created!

Navigate to the Canvas UI (sandbox or production instance) and log in using the credentials provided, search for Salina in the top-left search box and visit the first search result to find her chart.

For more detail about making Patient Create requests, check out the API documentation for Patient Create.

{% include alert.html type="info" content="As part of the request's response, you will see a patient ID within the location: header. Copy the ID value between Patient/ and / history - you will need it to create an appointment in the next step.<br><br> Also to note that ID will match the ID you will find in your browser when you navigate to the patient's chart: https://{customer}.canvasmedical.com/patient/{patientID}" %} 


## Create an Appointment

We have our first patient and now want to book their first appointment. But before we can book their appointment we will need to find a practitioner.

If you are using one of our canvas sandboxes, there will already be a demo staff member loaded in the instance. 

Run the following request to find the list of Practitioners in your organization. Again you will need to replace the <sandbox-name> and <bearer-token> with the same values you used to create your patient above. 

```shell
curl --location 'https://fumage-<sandbox-name>.canvasmedical.com/Practitioner' \
--header 'Content-Type: application/fhir+json' \
--header 'Authorization: Bearer <bearer-token>' | jq
```

You will then get a response similar to: 

```shell
{
  "resourceType" : "Bundle",
  "type" : "searchset",
  "total" : 1,
  "entry" : [
    {
      "resource" : {
        "resourceType" : "Practitioner",
        "id" : "e766816672f34a5b866771c773e38f3c",
        "identifier" : [
          {
            "system" : "http://hl7.org/fhir/sid/us-npi",
            "value" : "1834494258"
          }
        ],
        "name" : [
          {
            "use" : "usual",
            "text" : "Youta Priti MD",
            "family" : "Priti",
            "given" : [
              "Youta"
            ]
          }
        ]
      }
    }
  ]
}
```



Copy down the value for "id". This is the Practitioner ID you will need to create your first appointment.

Now we have our Patient ID and Practitioner ID. We're ready to create our first appointment.

Now lets set up the cURL command to create the appointment. Again you will need to replace the <sandbox-name> and <bearer-token>. Then replace <practitioner-id> and <patient-id> with the values copied in the last two requests. This appointment will create a Telehealth Appointment. You might want to update the start and end dates to be today's date for easy find-ability on the calendar view.  

```shell
curl -i --location 'https://fumage-<sandbox-name>.canvasmedical.com/Appointment' \
  --header 'Authorization: Bearer <bearer-token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "resourceType": "Appointment",
    "status": "booked",
    "appointmentType": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "448337001",
                "display": "Telemedicine consultation with patient (procedure)"
            }
        ]
    },
    "description": "Weekly check-in.",
    "supportingInformation" : [
      {
        "reference" : "Location/1"
      }
    ],
    "start": "2022-02-19T13:30:00.000Z",
    "end": "2022-02-19T14:00:00.000Z",
    "participant": [
        {
            "actor": {
                "reference": "Practitioner/<practitioner-id>"
            },
            "status": "accepted"
        },
        {
            "actor": {
                "reference": "Patient/<patient-id>"
            },
            "status": "accepted"
        }
    ]
}'
```



If you navigate to the correct date you used for start and end in the request above on the Schedule of your Canvas home page, you will see your first appointment. You should also be able to see the appointment when navigating to the patient's chart. 

For more detail about making Appointment Create requests, check out the API documentation for [Appointment Create](ref:create) .
