---
title: "Configuring Questionnaires"
layout: documentation
---
Our **Questionnaire, ROS, Physical Exam, and Structured Assessment Commands** are all built on our interview model. They can be created by your admin team and/or supers users in order to support many use cases within your charting workflows. They are a great way to create custom templates, capture discreet data, and extend Canvas's data model to meet the needs of your care model.

## Building a Questionnaire

Questionnaires are created using a Google Sheet template that was shared with you during your onboarding. Please reach out to your internal administrators first, and then our support team if you need help locating this template. The template allows you to configure your own questionnaires without needing code. 

{% include alert.html type="info" content=" <b>Questionnaires (blue)</b> are built as a series of <b>Questions (red),</b> each having associated <b>Question Responses (green)</b>." %}
<br>
<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRO5_7TTc7t5GndMjVe6fDCrXil2kKeV9800HB9fzfQlT57HDiQgZ9c0ZtByuLpqhlocphhLh0Yt1IR/pubhtml?gid=211293692&amp;single=true&amp;widget=true&amp;headers=false" width="99%" height="400px"></iframe>


## Questionnaire Types

The "use case in charting" field within the template will determine which Command the template is associated with. 

| Command | Use Case | Use Cases & What is Different |
| ------- | -------- | ----------------------------- |
| Questionnaire | QUES | Questionnaires can be used for many things including intake forms, social history questionnaires, screening questionnaires, and general charting templates. |
| Review of Systems (ROS) | ROS | A toggle to the left of each system will allow you to skip system and hide them from your documentation |
| Physical Exam (PE) | EXAM | A toggle to the left of each system will allow you to skip system and hide them from your documentation |
| Structured Assessment | SA | Adding ICD-10 and CPT backed responses can replace the need to use the Diagnose, Assess, or Perform Commands. Selecting these responses will add the appropriate codes to the billing footer. |



{% include alert.html type="info" content=" We recommend naming your tabs using the use case as prefixes to keep track of the different templates." %}


## Codes

All questionnaires, questions, and question responses must be code backed. We allow you to use the following standard code systems: **CPT, LOINC, SNOMED, or ICD-10**. or you can leverage an custom code system by indicating that it is **INTERNAL. CANVAS** is used by our team for specific Canvas concepts. These are case sensitive. 

When loading a questionnaire, the following must be true:
<ul>
<li>For a given questionnaire, all question codings should be unique.</li>
	<ul>
	<li>A coding is defined by system + code. So if two questions both have system = LOINC and code = 87245, this would return an error upon trying to upload the questionnaire.</li>
	<li>It is ok to have the same coding for two questions in different questionnaires. The recommendation would be to do this only when they are the same question, representing the same conceptual information.</li>
	</ul>
<li>For a given question, all response codings should be unique.
A coding is defined by system + code. So if two question responses both have system = LOINC and code = 87245, this would return an error upon trying to upload the questionnaire. </li>
	<ul>
	<li>It is ok to have the same coding for responses in different questions within the same questionnaire. The recommendation would be to do this only when the responses represent the same conceptual information.</li>
	<li>It is ok to have the same coding for responses in different questionnaires. The recommendation would be to do this only when they are the same question, representing the same conceptual information.</li>
	</ul>
</ul>

Use the following sites to leverage these code systems <br>
SNOMED: <https://snomed.terminology.tools/terminology-ui/index.html#/terminology> <br>
LOINC: <https://www.findacode.com/loinc/> <br>
ICD-10: <https://icd.who.int/browse10/2010/en> <br>
CPT: <https://www.ama-assn.org/practice-management/cpt> <br>

## Settings

These are set by updating the appropriate columns within the row for each Questionnaire and Question.

**Questionniare Settings**

| use_case_in_charting            	| QUES, ROS, EXAM, or SA                          	| Indicates the Questionnaire Type                                                                                                                                                                      	|
| scoring_function_js             	| Default_Score or Custom                         	| Selecting Default_Score will sum the values associated with each selected answer. Custom scoring needs to be built by Canvas.                                                                         	|
| can_originate_in_charting (REQ) 	| TRUE or FALSE                                   	| Determines whether the questionnaire can selected within a Command when charting. You may choose false if you only want to interact with it through the API and want to hide it from your clinicians. 	|
| expected_completion_time        	| NUMBER                                          	| How long (in minutes) should this questionnaire take to complete?                                                                                                                                     	|
| search_tags                     	| STRING                                          	| Alternative search terms, separated by commas, (e.g. 'depression' to find a PHQ-9)                                                                                                                    	|
| scoring_code_system             	| SNOMED, LOINC, ICD-10, CPT, INTERNAL, or CANVAS 	| What scoring system is being used?                                                                                                                                                                    	|
| content                         	|                                                 	|                                                                                                                                                                                                       	|
| prologue                        	| STRING                                          	| This text will display prior to the questions once the Questionnaire is selected within the Command. You can use this to provide guidance.                                                            	|
| use_in_shx (REQ)                	| TRUE or FALSE                                   	| Selecting True will display the questionnaire name and the date that the questionnaire was last recorded within the Social Determinants section of the Patient Summary                                	|

**Question Settings**

| question_name 					| STRING        	| Name of question. Typically the same as content below but you can create shorthand here if desired, as the content will display in the UI               	|
| content       					| STRING        	| What will display on screen when the command is selected                                                                                                	|
| use_in_shx    					| TRUE or FALSE 	| Selecting True will display the question and the date that the question was last recorded within the Social Determinants section of the Patient Summary 	|

## Question Response Types
**Single Select** (SING): The end user selects one response from a dropdown <br>
**Multi Select** (MULT): The end user can select multiple responses (pills) associated with one question <br>
**Free Text** (TXT): The end user can type in their free text response. There is a character limit of X characters <br>

## Questionnaire Scoring
**Default Scoring:** Select 'Default_Scoring" to leverage this functionality. The questionnaire will be scored by summing the values associated with each answer (Score Value) The score values must be numerical and can include decimals. <br>
**Custom Scoring:** This allows a narrative such as "a score of ## means..." This has to be completed by Canvas Engineering. Please create a Support request with the scoring scale and details. 

## Uploading Questionnaires
The Questionnaire loader is available to you in your {%glossary admin settings%}  menu. Paste in the URL of your Questionnaires-for-Loader Spreadsheet and the name of the tab you wish to load. A preview will appear for you to confirm that the questionnaire has been built correctly. You can choose to cancel the upload if you need to fix anything within the Google Sheet and reupload it as needed. If everything looks good, click load to make available for use in Canvas. 

We have enforced some validation in creating the questionnaires In order to ensure data is captured in a consistent way and can be used programmatically once collected.

You may see the following errors when loading questionnaires. Here is some troubleshooting advice:


## Questionniare Versioning 


## Video Tutorial
<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/23763052d54d4a7b8ec00c2d3e508c9f?sid=15104e87-2fb1-44b7-9e9f-af31967a1618" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>



