---
title: "Survey-Driven Diagnosis"
slug: "survey-driven-diagnosis"
hidden: false
createdAt: "2021-12-27T19:33:19.817Z"
updatedAt: "2022-04-14T22:03:34.641Z"
---
This protocol recommends diagnosing certain conditions based on questionnaire responses, and the recommendations have one-click commands for inserting the conditions into a Canvas note. 

**[Survey Driven Diagnosis code ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/survey_driven_diagnosis.py)**

This protocol is dependent on a Questionnaire called the `Diagnostic Assessment Tool` with specific codings for the questionnaire and each of its questions - the loader data for this Questionnaire is below. 
[block:parameters]
{
  "data": {
    "h-0": "QUESTIONNAIRE",
    "h-1": "name",
    "h-2": "use_case_in_charting",
    "h-3": "code_system",
    "h-4": "code",
    "h-5": "scoring_function_js",
    "h-6": "can_originate_in_charting",
    "h-7": "expected_completion_time",
    "h-8": "search_tags",
    "h-9": "scoring_code_system",
    "h-10": "scoring_code",
    "h-11": "content",
    "h-12": "prologue",
    "h-13": "use_in_shx",
    "0-0": "**QUESTION**",
    "0-2": "**name** ",
    "0-3": "**code_system** ",
    "0-4": "**code**",
    "0-5": "**code_description**",
    "0-6": "**content** ",
    "0-7": "**responses_code_system** ",
    "0-8": "**responses_type** ",
    "0-9": "**use_in_shx** ",
    "1-3": "**name**",
    "1-4": "**code**",
    "1-5": "**code_description**",
    "1-6": "**value**",
    "1-0": "**RESPONSE**",
    "2-0": "**QUESTIONNAIRE**",
    "2-1": "Diagnostic Assessment Tool",
    "2-2": "QUES",
    "2-3": "INTERNAL",
    "2-4": "PAT.QUESTIONNAIRE.2",
    "2-5": "Code for diagnostic assessment questionnaire",
    "2-6": "TRUE",
    "2-7": "1",
    "2-8": "diagnostic, assessment, diagnose, assess",
    "2-13": "",
    "3-0": "**QUESTION**",
    "4-0": "**RESPONSE**",
    "5-0": "**RESPONSE**",
    "3-1": "",
    "3-2": "Do you notice that your hands or arms bruise or bleed easily?",
    "4-2": "",
    "5-2": "",
    "3-3": "INTERNAL",
    "4-3": "Yes",
    "5-3": "No",
    "3-4": "PAT.QUES.8",
    "4-4": "PAT.RES.1",
    "5-4": "PAT.RES.2",
    "3-5": "Question 8",
    "3-6": "Do you notice that your hands or arms bruise or bleed easily?",
    "3-7": "INTERNAL",
    "3-8": "SING",
    "6-0": "**QUESTION**",
    "7-0": "**RESPONSE**",
    "8-0": "**RESPONSE**",
    "6-2": "Have you ever had a stent placed in your heart?",
    "4-5": "Response 1 (Yes)",
    "5-5": "Response 2 (No)",
    "6-3": "INTERNAL",
    "7-3": "Yes",
    "8-3": "No",
    "6-4": "PAT.QUES.9",
    "7-4": "PAT.RES.1",
    "8-4": "PAT.RES.2",
    "7-5": "Response 1 (Yes)",
    "8-5": "Response 2 (No)",
    "6-5": "Question 9",
    "6-6": "Have you ever had a stent placed in your heart?",
    "6-7": "INTERNAL",
    "6-8": "SING",
    "9-0": "**QUESTION**",
    "10-0": "**RESPONSE**",
    "11-0": "**RESPONSE**",
    "9-2": "Have you ever had a problem with alcohol in the past?",
    "9-3": "INTERNAL",
    "10-3": "Yes",
    "11-3": "No",
    "9-4": "PAT.QUES.10",
    "10-4": "PAT.RES.1",
    "11-4": "PAT.RES.2",
    "9-5": "Question 10",
    "10-5": "Response 1 (Yes)",
    "11-5": "Response 2 (No)",
    "9-6": "Have you ever had a problem with alcohol in the past?",
    "9-7": "INTERNAL",
    "9-8": "SING",
    "12-0": "**QUESTION**",
    "13-0": "**RESPONSE**",
    "14-0": "**RESPONSE**",
    "12-2": "Have you ever had a time when you were down or struggling and you were told it was depression?",
    "12-6": "Have you ever had a time when you were down or struggling and you were told it was depression?",
    "12-3": "INTERNAL",
    "13-3": "Yes",
    "14-3": "No",
    "13-4": "PAT.RES.1",
    "14-4": "PAT.RES.2",
    "12-4": "PAT.QUES.11",
    "12-5": "Question 11",
    "13-5": "Response 1 (Yes)",
    "14-5": "Response 2 (No)",
    "12-7": "INTERNAL",
    "12-8": "SING"
  },
  "cols": 14,
  "rows": 15
}
[/block]
After uploading this Questionnaire (via the questionnaire loader in settings --> more detailed instructions can be found [here](https://canvas-medical.zendesk.com/hc/en-us/articles/4403561447827-Creating-a-New-Questionnaire)) and the protocol (via the command line), you now should be able to fill out the Diagnostic Assessment Tool. If any of your responses are "Yes", you should see a new protocol card show up on the right-hand-side with recommendations for each "Yes" answer. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b5b3347-Screen_Shot_2021-12-23_at_2.50.28_PM.png",
        "Screen Shot 2021-12-23 at 2.50.28 PM.png",
        2462,
        1154,
        "#f2f1f1"
      ]
    }
  ]
}
[/block]
To test out the command-insertion, click on any of the `Diagnose` buttons next to the recommended conditions. A diagnose command should be inserted into your note with all of the required fields filled out for you already. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/043fecc-Screen_Shot_2021-12-23_at_2.51.48_PM.png",
        "Screen Shot 2021-12-23 at 2.51.48 PM.png",
        2478,
        1134,
        "#f1f0ef"
      ]
    }
  ]
}
[/block]
At this point, all you need to do is commit the command (click the Diagnose button in the note command). You should notice that the protocol card on the right-hand-side immediately recalculates and removes that recommended condition. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/5430cdf-Screen_Shot_2021-12-23_at_2.52.40_PM.png",
        "Screen Shot 2021-12-23 at 2.52.40 PM.png",
        2464,
        1046,
        "#f1f0f0"
      ]
    }
  ]
}
[/block]
If you insert and commit all the commands, the protocol card should disappear from the right-hand-side as all recommendations have been satisfied.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e76cfc2-Screen_Shot_2021-12-23_at_2.53.26_PM.png",
        "Screen Shot 2021-12-23 at 2.53.26 PM.png",
        2486,
        1248,
        "#f2f3f3"
      ]
    }
  ]
}
[/block]