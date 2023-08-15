---
title: "Protocol Logging Tool"
slug: "protocol-logging-tool"
excerpt: "A utility for debugging your uploaded protocols"
hidden: false
createdAt: "2022-02-03T22:38:49.443Z"
updatedAt: "2022-02-03T23:11:06.506Z"
---
Have you uploaded a protocol and want to know the results for some/all patients for which it was computed? And also catch any errors that may have occurred? Look no further than the protocol logging tool! 

In the admin settings of Canvas in the Protocol uploads section (`/admin/api/protocolupload/`), you will find that each row representing an uploaded protocol has a link on the right-most column that says `Log`. Click on this link to navigate to the logging tool. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/60b38a6-Screen_Shot_2022-02-03_at_2.43.44_PM.png",
        "Screen Shot 2022-02-03 at 2.43.44 PM.png",
        2310,
        962,
        "#edf0f3"
      ]
    }
  ]
}
[/block]
Here you will find the result of the protocol's computation for each active patient.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/13d2152-Screen_Shot_2022-02-03_at_2.47.02_PM.png",
        "Screen Shot 2022-02-03 at 2.47.02 PM.png",
        2254,
        852,
        "#d0e3d0"
      ]
    }
  ]
}
[/block]
A green header means the protocol computed successfully with no errors. The header also provides the patient key (which is a link you can click on to navigate to the patient's chart), and the UTC time at which the protocol computed. The entries on this view are sorted oldest at the top, newest at the bottom. 

If the protocol result status is `STATUS_DUE`, you will see the output of the Recommendations returned from the compute_results function. 

A red header means the protocol encountered an error when attempting to compute for that patient, and it will provide you with a stacktrace and description of the error. This can be especially helpful for debugging your custom protocol code if you're finding that you're not seeing the results you expect. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/aa93a6e-Screen_Shot_2022-02-03_at_2.54.28_PM.png",
        "Screen Shot 2022-02-03 at 2.54.28 PM.png",
        2248,
        850,
        "#edeae7"
      ]
    }
  ]
}
[/block]
There are a few other tools up at the header of the page that can be useful as you debug and check on the status of your protocol. 

The Patient Key input with the blue filter button does exactly what it looks like - it filters the entries for a specific patient. Just put in a patient key and hit the Filter button to see just the computations for that specific patient.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e8393fe-Screen_Shot_2022-02-03_at_2.58.57_PM.png",
        "Screen Shot 2022-02-03 at 2.58.57 PM.png",
        2310,
        406,
        "#cfdfd1"
      ]
    }
  ]
}
[/block]
The Run Manually dropdown provides you with a space to re-compute a specific (or all) protocol(s) for an individual patient.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/66b0817-Screen_Shot_2022-02-03_at_3.05.10_PM.png",
        "Screen Shot 2022-02-03 at 3.05.10 PM.png",
        2316,
        430,
        "#cfdfd0"
      ]
    }
  ]
}
[/block]
Paste in the patient key, and then either click Run All to compute all protocols for that patient, or click on the specific protocol you want to re-compute. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/9bd1931-Screen_Shot_2022-02-03_at_3.07.23_PM.png",
        "Screen Shot 2022-02-03 at 3.07.23 PM.png",
        2164,
        610,
        "#eef3f0"
      ]
    }
  ]
}
[/block]
Last in the header is the Clear All button, which clears all the entries from the page. This is a nice tool if you want a clean slate and don't mind losing the record of all the previous computations. Note that this will not delete the previous protocol results from the database, it just removes the log entries from this view.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6027410-Screen_Shot_2022-02-03_at_3.10.40_PM.png",
        "Screen Shot 2022-02-03 at 3.10.40 PM.png",
        2324,
        424,
        "#cfdfcf"
      ]
    }
  ]
}
[/block]