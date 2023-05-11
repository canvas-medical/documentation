---
title: "Communication"
---

## Communication Create

### Getting the newly-created communication's ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header.

### Finding the message in the Canvas UI

Messages created through this endpoint will be found on the patient's chart timeline according to the `created` date. Messages that were documented using this endpoint will say: "Drafted <time since message was sent> on <sent time> by Canvas Bot". For example: "Drafted 4 months ago on Feb 10th, 2022 by Canvas Bot". 

If the sender of the message is a Practitioner, the message will be displayed as a draft, and will display on the UI as shown below: 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6a0aa00-messagedraft.png",
        "messagedraft.png",
        1488,
        754,
        "#f3f5f5"
      ]
    }
  ]
}
[/block]
Once the 'send' button is clicked on a message generated through a FHIR endpoint, it will not notify the patient via text message and it will not update Canvas's stored value for sent. Once the `send` button is clicked, the patient will be able to see the message in the [patient app](https://canvas-medical.zendesk.com/hc/en-us/articles/4403783063443-Patient-App-Instructions-for-Patients#h_01FARRDABWQFCWZ8YX94PPNKDQ) at the time the message was drafted. 

 
If the sender of the message is a patient, the message will be displayed on the patient chart as follows:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/fcf11f8-Screen_Shot_2022-06-23_at_10.30.29_AM.png",
        "Screen Shot 2022-06-23 at 10.30.29 AM.png",
        2510,
        284,
        "#f1f2f3"
      ]
    }
  ]
}
[/block]
The sent date will display along with the recipient. The message will already appear in the patient messaging app. 

### Attributes that are pulled into Canvas:

### Sent

Sent ingests the date and time in UTC that the message on the Canvas UI appears drafted if the sender is a practitioner or received if the sender is a patient. 

If sent and received are both not passed in, it will default to the current date and time. If received is provided, but sent is not, sent will be set to the same date and time as received. 
```
{
  "codes": [
    {
      "code": "\"sent\": \"2021-04-29T13:30:00.000Z\"",
      "language": "text"
    }
  ]
}
```
### Received

Received ingests the date and time in UTC that the message was sent. If no received time is included, it will not be stored in the database. 
```
{
  "codes": [
    {
      "code": "\"received\": \"2021-04-29T13:30:00.000Z\"",
      "language": "text"
    }
  ]
}
```
### Recipient [required]

Recipient ingests a patient or practitioner reference to whom the message is being sent to. Only the first item of the array is ingested by Canvas.
```
{
  "codes": [
    {
      "code": "\"recipient\": [\n     {\n         \"reference\": \"Patient/5350cd20de8a470aa570a852859ac87e\"\n     }\n],",
      "language": "text"
    }
  ]
}
```
### Sender [required]

Sender accepts the ID of the practitioner or patient that sent the message. 
```
{
  "codes": [
    {
      "code": " \"sender\": \n    {\n        \"reference\": \"Practitioner/5eede137ecfe4124b8b773040e33be14\"\n    },",
      "language": "text"
    }
  ]
}
```
### Payload [required]

The body of the message that was sent. Only the first element of the content portion is saved. The content cannot be an empty string. This will display as the message's content on the Canvas UI.
```
{
  "codes": [
    {
      "code": "\"payload\": [\n\t{\n\t\t\"content\": \"You have an upcoming appointment!\"\n\t}\n]",
      "language": "text"
    }
  ]
}
```
## Communication Search

### Patient-Practitioner Messaging in Canvas

Communication search will only return messages between a practitioner and patient, not between two practitioners. To see how to view patient messages and message patients, read this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-).

### Additional HTML formatting

With the release of [Advanced Letter Templates](https://canvas-medical.zendesk.com/hc/en-us/articles/1500003414602-Creating-letter-templates), Messages are now saved in the database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like [Interweave](https://interweave.dev/docs/#markup-) or extracting the text.  **NOTE: Messages sent before release (10/26/2022 @ 17:00 PST) will remain in plain text format**