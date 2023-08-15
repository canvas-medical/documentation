---
title: "Prescribe Command Recommendation"
slug: "prescribe-command-recommendation"
hidden: false
createdAt: "2022-02-08T05:25:27.510Z"
updatedAt: "2022-04-14T22:03:13.345Z"
---
This example is a protocol that recommends prescribing a specific medication for patients diagnosed with nausea, and includes a button that inserts a fully completed Prescribe command into the Canvas note.

[**Prescribe Command Recommendation code**
](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/prescribe_command_recommendation.py)

After everything is uploaded a set up properly, once a patient is diagnosed with `R11.2`, the protocol card should appear on the right-hand-side.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ae0c929-Screen_Shot_2022-02-07_at_9.40.56_PM.png",
        "Screen Shot 2022-02-07 at 9.40.56 PM.png",
        2392,
        742,
        "#f1f1f3"
      ]
    }
  ]
}
[/block]
Click the blue Prescribe button in the recommendation, and a prescribe command will insert into the note with all fields filled out according to what we specified in the protocol! 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ba12051-Screen_Shot_2022-02-07_at_9.43.01_PM.png",
        "Screen Shot 2022-02-07 at 9.43.01 PM.png",
        1510,
        664,
        "#f3f4f5"
      ]
    }
  ]
}
[/block]
Simply click Review and Save (or Send) to commit the command. Once committed, the protocol will be satisfied and the protocol card will disappear from the right-hand-side. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/7093359-Screen_Shot_2022-02-07_at_9.46.53_PM.png",
        "Screen Shot 2022-02-07 at 9.46.53 PM.png",
        2186,
        1114,
        "#f2f3f4"
      ]
    }
  ]
}
[/block]