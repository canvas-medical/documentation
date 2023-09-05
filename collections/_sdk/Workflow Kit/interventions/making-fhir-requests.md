---
title: "Making FHIR Requests"
slug: "making-fhir-requests"
hidden: false
createdAt: "2023-03-08T17:50:10.856Z"
updatedAt: "2023-03-08T17:50:10.856Z"
---
Inside of a Canvas protocol, we allow the ability to make a FHIR request for any of our FHIR endpoints that are documented in the [Getting Started With the Canvas FHIR API](/api/).

You can reference [this example code](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/fhir_call_example.py) that shows using the [Change Types](/sdk/change-types) of Patient to make a [Patient Read](/api/patient/#read) call and then send the payload to a webhook via the [Notification Protocol](/sdk/notification-protocol). The example also shows the fetching of the bearer token for authorization to use our FHIR endpoints that is explained in [Customer Authentication](/api/authentication) with the help of storing the Client ID and Client Secret with the SDK's [Settings/Secret Store](/sdk/secret-store)