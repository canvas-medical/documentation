---
title: "Plan Command Recommendation"
slug: "plan-command-recommendation"
hidden: false
createdAt: "2022-02-18T05:07:58.122Z"
updatedAt: "2022-04-14T22:03:07.238Z"
---
This example is a protocol that recommends inserting a Plan command to a Canvas note for patients diagnosed with obesity.

**[Plan Command Recommendation code ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/plan_command_recommendation.py)**

After everything is uploaded and set up properly, once a patient is diagnosed with obesity (`E66.01` for example), the protocol card should appear on the right-hand-side.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1218133-Screen_Shot_2022-02-17_at_9.39.43_PM.png",
        "Screen Shot 2022-02-17 at 9.39.43 PM.png",
        2390,
        710,
        "#f1f1f2"
      ]
    }
  ]
}
[/block]
Click the blue Plan button in the recommendation, and a plan command will insert into the note with the field pre-populated with what we specified in the protocol. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c68ff3e-Screen_Shot_2022-02-17_at_9.41.40_PM.png",
        "Screen Shot 2022-02-17 at 9.41.40 PM.png",
        1506,
        436,
        "#f5f6f7"
      ]
    }
  ]
}
[/block]