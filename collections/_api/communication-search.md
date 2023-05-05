---
title: "Communication Search"
slug: "communication-search"
excerpt: "Search for communications between practitioners and patients"
hidden: false
createdAt: "2021-09-10T23:20:50.829Z"
updatedAt: "2022-12-12T16:49:13.075Z"
---
## Patient-Practitioner Messaging in Canvas

Communication search will only return messages between a practitioner and patient, not between two practitioners. To see how to view patient messages and message patients, read this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/1500001593221-Patient-Message-Inbox-).

## Additional HTML formatting

With the release of [Advanced Letter Templates](https://canvas-medical.zendesk.com/hc/en-us/articles/1500003414602-Creating-letter-templates), Messages are now saved in the database in HTML format. Customers using the Communication endpoint for their own patient applications will need to take this into account either by embedding the html directly using a library like [Interweave](https://interweave.dev/docs/#markup-) or extracting the text.  **NOTE: Messages sent before release (10/26/2022 @ 17:00 PST) will remain in plain text format**