---
title: "Task Create"
slug: "task-create"
excerpt: "Create a task tied to a specific patient"
hidden: false
createdAt: "2022-05-17T14:51:16.845Z"
updatedAt: "2022-07-28T00:04:26.940Z"
---
# Getting the newly-created task's ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header.

# Attributes that are pulled into Canvas:

Tasks created through this FHIR Endpoint will display in the [patient chart via the tasks icon](https://canvas-medical.zendesk.com/hc/en-us/articles/360057545873-Tasks). Open tasks will also display in th [Task Panel ](https://canvas-medical.zendesk.com/hc/en-us/articles/360059339433-Task-List) 

## status [REQUIRED]

The current status of the task. The mapping from FHIR statuses to Canvas Task statuses is as follows:
[block:parameters]
{
  "data": {
    "h-0": "FHIR Task Status",
    "h-1": "Canvas Mapping",
    "0-0": "draft\nrequested\naccepted\nready\nin-progress\non-hold",
    "1-0": "rejected\ncancelled\nfailed\nentered-in-error",
    "2-0": "completed",
    "0-1": "open",
    "1-1": "closed",
    "2-1": "completed"
  },
  "cols": 2,
  "rows": 3
}
[/block]
These statuses are filterable on the canvas UI in the [patient chart](https://canvas-medical.zendesk.com/hc/en-us/articles/360057545873-Tasks). By default we only show open tasks. Only open tasks will show on the [Task Panel ](https://canvas-medical.zendesk.com/hc/en-us/articles/360059339433-Task-List) 
[block:code]
{
  "codes": [
    {
      "code": "\"status\": \"requested\",",
      "language": "text"
    }
  ]
}
[/block]
## requester [REQUIRED]

 The user who requested the task. This must be a practitioner reference.
[block:code]
{
  "codes": [
    {
      "code": "\"requester\": {\n\t\"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## for [REQUIRED]

 The patient reference for whom the task is being done.
[block:code]
{
  "codes": [
    {
      "code": "\"for\": {\n\t\"reference\": \"Patient/5350cd20de8a470aa570a852859ac87e\"\n},",
      "language": "text"
    }
  ]
}
[/block]
##  Description

 The title for the task. If no description is given, the Canvas UI will not display any title for the task.
[block:code]
{
  "codes": [
    {
      "code": "\"description\": \"Ask patient for new insurance information.\",",
      "language": "text"
    }
  ]
}
[/block]
## owner 

 The user that should handle the task. Must be a practitioner reference.
[block:code]
{
  "codes": [
    {
      "code": "\"owner\": {\n\t\"reference\": \"Practitioner/3640cd20de8a470aa570a852859ac87e\"\n},",
      "language": "text"
    }
  ]
}
[/block]
## authoredOn

This is the timestamp the Task was created on. If omitted from the message, it will default to the current timestamp at time of ingestion
[block:code]
{
  "codes": [
    {
      "code": "\"authoredOn\": \"2022-03-20T14:00:00.000Z\",",
      "language": "text"
    }
  ]
}
[/block]
## restriction 
[block:callout]
{
  "type": "info",
  "title": "DEPRECATED `due` attribute",
  "body": "The `due` attribute will be deprecated on July 26th, 2022 in favor of Task.restriction.period.end. Please work to utilize the new attribute. We will communicate when we plan to remove the the `due` attribute all together."
}
[/block]
This object can be used to specify the due date timestamp of the Task. The due date is taken from the `restriction.period.end` attribute
[block:code]
{
  "codes": [
    {
      "code": "\"restriction\": {\n  \"period\": {\n  \t\"end\": \"2022-08-01T04:00:00+00:00\"\n  }\n}",
      "language": "text"
    }
  ]
}
[/block]
## note 

A comment thread about the task. For each note you can specify the:

1.  comment's text [REQUIRED]
2. timestamp the comment was left (If omitted it will default to current timestamp at data ingestion)
3  reference to the practitioner that left the specific comment. [REQUIRED]
[block:code]
{
  "codes": [
    {
      "code": "\"note\": [\n  {\n    \"text\": \"Please be sure to scan them in at their next visit.\",\n    \"time\": \"2022-03-20T14:00:00.000Z\",\n    \"authorReference\": {\n    \t\"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"\n    }\n  }\n]",
      "language": "text"
    }
  ]
}
[/block]
## extension (task-group)

The team that the task is assigned to.  This optional field requires a reference to the team from the Group endpoint. In the Canvas UI, this will display under the field "team" in the task card.
[block:code]
{
  "codes": [
    {
      "code": "\"extension\": [\n  {\n    \"url\": \"http://schemas.canvasmedical.com/fhir/extensions/task-group\",\n    \"valueReference\": {\n      \"reference\": \"Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13\"\n    }\n  }\n],",
      "language": "text"
    }
  ]
}
[/block]
## input

Adds labels to the task in the Canvas UI. If the label doesn't exist in Canvas already, it will be created.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c7b907e-Screen_Shot_2022-05-17_at_10.50.12_AM.png",
        "Screen Shot 2022-05-17 at 10.50.12 AM.png",
        613,
        247,
        "#f8f8f9"
      ],
      "caption": ""
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "\"input\": [\n  {\n    \"type\": {\n      \"text\": \"label\"\n    },\n    \"valueString\": \"Urgent\"\n  }\n]  ",
      "language": "text"
    }
  ]
}
[/block]