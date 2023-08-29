---
title: "Annotating PDFs"
---

Annotations allow users to mark up and comment on PDFs without altering the original authors content. Through our Apryse integration Canvas supports the following editing capabilities:

- Comments
- Text markup (highlight, squiggly, underline, strikeout)
- Add shapes (line, arrow, polyline, rectangle, ellipse, polygon, cloud)
- Cloud annotations
- Apply freehand ink annotations
- Signatures
- FreeText, Callout
- Stamps (checks, approvals/denials, dates)
- Redaction

### Using the PDF Editor
The option to annotate PDFs is available in Data Integration and when reviewing documents in your Action Center. It is currently not available when viewing documents from the patient's record. When enabled, you will see a grey button: "Annotate". You have the option to enable a warning for users, alerting them to the cost associated with this action. 

After clicking, the PDF viewer will refresh to show the additional tools. 

### Creating Annotations

The available annotation tools can be found in the lower toolbar (in gray). You can click on a tool to switch to it. Use the dropdown in the top menu to switch between tool types (currently set to "Annotate" in the image below).

{:refdef: style="text-align: center;"}
![Annotation UI](/assets/images/annotations.png){:width="80%"}
{: refdef}

Another way to switch tools is to right-click on the document which will bring up a context menu. From this menu you can select from a subset of annotation tools.

{:refdef: style="text-align: center;"}
![Annotation UI](/assets/images/context-menu.png){:width="50%"}
{: refdef}

Once you have switched to an annotation tool, then you'll be able to click or click + drag (depending on the annotation type) to create the annotation.

You can access Apryse's documentation [here](https://docs.apryse.com/documentation/web/guides/annotation/) to learn more about all of the various tools. Here are a couple that we find most useful in your clinical workflows. 

To add dates:
Fill and Sign > Calendar 

To add signatures:
Fill and Sign > Signature
Insert > Signature
Annotate > Freehand
Insert > Image


Stamp Annotations
Stamp annotations allow users to place an image annotation onto any page on the document. It is the most versatile annotation since you can draw anything as its content.

Rubber stamps are also stamp annotations and the PDF specification defines a standard set of rubber stamps. WebViewer also provides the ability to create custom stamps by setting the text of the stamp annotation.

Along with free hand signature annotations, stamp annotations can also be used to sign a signature field.








Customers also have the ability to view annotated documents through our FHIR API, within the associated patient chart, or through Admin settings. These annotated changes also include details of the users who made changes to the document and when the annotations were made for audit purposes.

The PDF annotation feature can be enabled for customers starting on Thursday, June 29th, via a passthrough cost. For those customer interested in enabling within their instance, please be sure to request a demo with product@canvasmedical.com or connect with your customer support team member

To enhance a user’s experience in Canvas, integration of functionalities aims to provide a seamless experience across the application. With PDF annotations, users are able to interact directly with any uploaded document within Canvas.  Previously, users needed to download a document, make annotations, and reupload to associate to a patient’s chart. Some example use cases include:

Highlighting or underlining critical information within a document for users to easily spot before the document is added to a patient’s chart.
Including important comments or symbols on a specific type of document for future reference by all members of the organization. 
Allowing providers to directly sign a lab report, imaging report, specialty consult report, or uncategorized clinical document within Canvas prior to delegating the review to another team member or attaching to the patient chart. 
Removing unnecessary pages from an uploaded packet, rotating pages for easy review, and redacting information with solid boxes when such changes are needed by document
Enabling PDF Annotations

In order to enable the PDF annotation functionality, Administrators must contact Canvas support in order to configure this feature within any instances. Given that there is a passthrough cost associated with the utilization of the PDF annotation functionality, it is important for all customers to understand the cost and full capabilities of this feature. 

There are guardrails in place to ensure that when the functionality is enabled, users understand the cost implications of utilizing within any given document as the cost is calculated per utilization. 




As a user selects the Annotate button, prior to accessing the functionalities, there is a confirmation popup asking if the user is sure about utilizing. If a user cancels, they are brought back to the previous view but if a user confirms a new version of the document is displayed with all functionalities. 







Annotating in Data Integration

Once a document is available within Data Integration, and PDF annotation is enabled in an instance, a user will see an annotation button above the patient name field. This button will be included per each document faxed or uploaded. 




Users have the ability to determine whether they want to annotate a document or not. Users can either annotate a document before or after linking to a patient and choosing the document type value. This allows customers to determine the most appropriate workflow for their teams. 

When users want to annotate a document, they are able to click the Annotate document and after confirming the associated cost popup, a new version of the document with annotation capabilities will appear. 







Users are able to take the following actions within the annotations feature:

Insert annotations such as underline text, highlight text, insert boxes, type in text (with preferred font style and size), and strikeout text
Insert comment bubbles in any part of the document
Insert shapes that are free drawn or part of a set list of options
Insert stamps, signatures, images, or callouts in any part of the document
Insert cross, ticked, or dotted checkboxes when appropriate with the ability 
Review pages side by side and rotate specific pages when necessary
Search for a specific word or phrase across the entire document for easy review or search needs

Many of the actions allow for flexibility of color used and can be undone if needed. 

Once a document has been annotated and is ready to be saved, users simply click the save button on the top right corner of the menu bar. Once the document is saved, a user is able to associate it with the corresponding patient. 




If users make annotations to a document and in the process of associating to a patient, forget to save their annotations, prior to the document being associated there will be a popup confirming the action a user was intending to take. 

Selecting Cancel submission, the user is taken back to the annotation view to take any action they want
Selecting Save annotations & Submit, the annotations will be saved and included in the version of the document associated with a patient
Selecting Submit without saving, none of the annotations will be saved to the version of the document associated with a patient

Once an annotated document has been saved to a patient, a user is able to find it on the patient chart in the corresponding section of the document type. (Ex. Consents will be found on the consent link of a patient’s profile or within the documents section of the patient chart). Any annotated documents that have a review document type association can also be found within the review workflow. These document types include:

Imaging Report
Lab Report
Specialist Consult Report
Uncategorized Clinical Document (which is it’s own document type AND the below document type dropdown options appear within the uncategorized clinical documents when reviewing on schedule view)
Care Management
Emergency Department Report
External Medical Records
Home Care Report
Hospital Discharge Summary
Hospital History & Physical
In-Office Testing
Nursing Home
Operative Report
Patient Intake Form
Physical Exams
Prescription Refill Request
Rehabilitation Report
Annotating in Clinical Review Workflow

When selecting New Labs, New Imaging, New consult reports, or New uncategorized reports from the action center, users are able to annotate any document within these workflows.




When a user selects to annotate any of these clinical review documents, the same functionalities and user experiences from Data Integration are available:

Popup confirmation of cost association
Annotation functionalities once they service is confirmed for utilization
Submission confirmation if an annotate document is not saved
Annotation to the patient chart with annotations included
Annotation Functionalities

This feature has an extensive list of possible actions that can be taken on a document. Below is a quick summary of possibilities within this workflow.

Top bar navigation menu allows for:
Downloading, printing, and document settings
Page setup settings
Zooming capabilities
Dragging and cropping
Document comments review
Searching of words or phrases
Saving
Dropdown of further actions: view, annotate, shapes, insert, edit, fill & sign, and forms (each will be explained in more detail below)




View: Allows for viewing of the full documents with no inserting actions needed
Annotate: Allows for inserting the necessary annotations within the document

This includes underlining, highlighting, insertion of squares, text input, freehand highlighting, free hand underlining, insertion of notes, and strikethrough
Users can also erase any annotations added 
Shapes: Allows for inserting free hand shapes or those already provided by the feature

Insert: Allows for inserting stamps, signatures, images, and callouts

Within signatures, users can free hand a signature, allow for signatures to be created based on typed words or upload a signature that a user may prefer. We recommend that signatures are saved so that they can quickly be uploaded if that is the preferred need. 

Edit: Allows for cropping the document into a new version of the document. Note that if a document is cropped, the cropped selection becomes the new version of the document and the original version will not be saved.  
Fill & Sign: Allows for inserting rubber stamps, text, signatures, checkboxes, and dates.
Forms: Allows for creating interactive form fields on a document that can be filled in by users after they have been saved to a patient’s profile. Form capabilities include: signature, checkbox, radio buttons, and list selections.







Important to call out that once form value have been filled in, the document must be downloaded from Canvas with changes made option in order to keep the form changes. We recommend the new version of the document be uploaded and added back to the patient chart if required.
History of Annotated Documents

For use cases in which Administrators need to review what team members made annotations to a document, what the annotations were, and when, this information is located within the Settings section of each instance. Under the Practice header, Administrators will see a Document Annotations page which will list all annotated documents, within each document the following is visible: