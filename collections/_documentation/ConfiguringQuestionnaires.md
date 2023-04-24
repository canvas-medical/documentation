---
layout: documentation
title: "Configuring Questionnaires"
categories: cat1 cat2
tags: tag1 tag2
request_sample: It may be difficult to display code blocks in front-matter
---

## **Configuring Questionnaires**

Our Questionnaire, ROS, Physical Exam, and Structured Assessment Commands are all built on our interview model. They can be created by your admin team / supers users in order to support many use cases within your charting workflows. They are a great way to create custom templates, capture discreet data, and extend Canvas's data model to meet your needs.

### Building a Questionnaire

Questionnaires are created using a Google Sheet template that was shared with you during your onboarding. Please reach out to your internal administrators or our support team if you need help locating this template. The template allows you to configure your own questionnaires without needing code. We have enforced some validation in creating the questionnaires In order to ensure data is captured in a consistent way and can be used programmatically once collected.

**Questionnaires** are built as a series of **Questions,** each having associated **Question Responses**

### Questionnaire Types

The "use case in charting" field within the template will determine which Command it is associated with. We also recommend naming your tabs using the use case as prefixes to keep track of the different templates.

| **Command** | **Use Case** | **Use Cases & What is Different** |
| --- | --- | --- |
| Questionnaire | QUES | Questionnaires can be used for many things including intake forms, social history questionnaires, screening questionnaires, and general charting templates. |
| Review of Systems (ROS) | ROS | A toggle to the left of each system will allow you to skip system and hide them from your documentation |
| Physical Exam (PE) | EXAM | A toggle to the left of each system will allow you to skip system and hide them from your documentation |
| Structured Assessment | SA | Adding ICD-10 and CPT backed responses can replace the need to use the Diagnose, Assess, or Perform Commands. Selecting these responses will add the appropriate codes to the visit. |

### Questionnaire, Question, & Question Response Codings

All questionnaires, questions, and question responses must be code backed. We allow you to use the following standard code systems: **CPT, LOINC, SNOMED, or ICD-10**. or you can leverage an custom code system by indicating that it is **INTERNAL. CANVAS** is used by our team for specific Canvas concepts. These are case sensitive. When loading a questionnaire, the following must be true:
