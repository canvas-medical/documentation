---
title: "Appointment Updater"
slug: "appointment-updater"
hidden: false
createdAt: "2021-12-23T22:32:12.647Z"
updatedAt: "2022-03-17T16:53:52.729Z"
---
This protocol updates the meeting link of an Appointment right after it is created. This is very helpful for telehealth appointments. 

**[Appointment Updater code ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/appointment_updater.py)**

Every time an Appointment is created, a dynamically generated meeting link will be stored to the Appointment. You'll know it worked when you check in the appointment and the blue meeting button on the top right of the Appointment header is clickable, and takes you to the url you assigned in the protocol. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/01cf41e-Screen_Shot_2021-12-23_at_2.26.36_PM.png",
        "Screen Shot 2021-12-23 at 2.26.36 PM.png",
        1612,
        414,
        "#f1f3f4"
      ]
    }
  ]
}
[/block]