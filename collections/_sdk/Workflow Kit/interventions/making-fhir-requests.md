---
title: "Making FHIR Requests"
slug: "making-fhir-requests"
hidden: false
createdAt: "2023-03-08T17:50:10.856Z"
updatedAt: "2023-03-08T17:50:10.856Z"
---
Inside of a Canvas protocol, we allow the ability to make a FHIR request for any of our FHIR endpoints that are documented in the [Getting Started With the Canvas FHIR API](ref:getting-started-with-your-api).

You can reference [this example code](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/fhir_call_example.py) that shows using the [Change Types](doc:change-types) of Patient to make a [Patient Read](ref:patient-read) call and then send the payload to a webhook via the [Notification Protocol](doc:notification-protocol). The example also shows the fetching of the bearer token for authorization to use our FHIR endpoints that is explained in [Customer Authentication](ref:authentication) with the help of storing the Client ID and Client Secret with the SDK's [Settings/Secret Store](doc:secret-store)