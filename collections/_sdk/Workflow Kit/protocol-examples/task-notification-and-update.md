---
title: "Task Notification and Update"
slug: "task-notification-and-update"
hidden: false
createdAt: "2023-04-06T17:59:40.865Z"
updatedAt: "2023-04-06T17:59:40.865Z"
---
This protocol [example](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/task_notification_and_update.py) demonstrates the use of our [Notification Functionality](doc:notification-protocol) and [Making FHIR Requests](doc:making-fhir-requests). 

The protocol will listen to a Task being created for the first time and send a notification out to a webhook of your choosing. 

The payload sent to the webhook is to demonstrate the different data forms you have for a Task

1. There is a call to our FHIR [Task Search](ref:task-search) endpoint to get the FHIR payload of the Task that was created
2. There is a filter to find the Task in the patient object the SDK directly has access to. 

These forms will demonstrate the two different serializations we have to Tasks. 

To go even further with this example, once the notification payload was successfully sent out, we use the FHIR [Task Update](ref:task-update) endpoint to add a comment to the Task to let the clinicians on the Canvas UI that it was successfully sent over.