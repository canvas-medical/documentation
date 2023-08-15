---
title: "Appointment Task Creator"
slug: "appointment-task-creator"
hidden: false
createdAt: "2021-12-23T22:08:04.387Z"
updatedAt: "2022-03-17T16:53:04.667Z"
---
This protocol creates a Task every time a new Appointment is booked for a patient. The task is automatically assigned to the provider with whom the Appointment is scheduled, sets the due date to 3 days before the Appointment, and asks the provider to send a reminder to the patient. 

[**Appointment Task Creator code** ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/appointment_task_creator.py)

When an appointment is booked, you can expect to see a Task show up for the patient on the right-hand-side that looks like this:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e68d34f-Screen_Shot_2021-12-23_at_2.11.18_PM.png",
        "Screen Shot 2021-12-23 at 2.11.18 PM.png",
        1158,
        736,
        "#efeff0"
      ],
      "caption": ""
    }
  ]
}
[/block]