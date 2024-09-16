---
title: Letters	
layout: documentation
---


Creating a letter to provide to a patient, use as an order, or forward to another care provider is an essential part of healthcare. The ability to [print](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7EDRAVQWE5451CVGJBYXQ) or [directly fax](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7EKX6EF5GJD89FNA3EPMX) this letter is core functionality within Canvas. Please see our [letter templates](https://canvas-medical.zendesk.com/hc/en-us/articles/1500003414602) article to learn how to create templates that can be used in the letter note type. Users also have the ability to add attachments to letters that can be previewed, printed, and faxed as packages. Please see our [letter attachment](https://canvas-medical.zendesk.com/hc/en-us/articles/10914874591123) article for more details.

## Step by Step

### **Letter Note**

Letter Notes are available as one of the default note types in Canvas and can be disabled in the [Note Types](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083) setting.  The top of the letter note has drop down menus that allow users to select a sending provider, custom template (optional), and sending location. If no template is selected the user is free to type out the content of the letter as needed.

**NOTE:** *When letter content is complete, the letter can be [previewed,](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7E5Q326KPPAXSX9WVPV32) [printed](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7EDRAVQWE5451CVGJBYXQ) or [faxed](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7EKX6EF5GJD89FNA3EPMX). See below for details.*

{:refdef: style="text-align: center;"} 
![create-letters](/assets/images/create-letters.gif){:width="100%"}
{: refdef}

### **Attachments to Letters**

Users have the ability to add attachments to letters that can be previewed, printed, and faxed as packages. Please see our attachments to letters article for more details. Patient associated resources that can be included as attachments:

- Patient chart notes
- After visit summary
- Labs
- Imagining Consult reports
- Uncategorized documents
- Chart documents
- Administrative documents
- Consents

### **Missing Letter Template Placeholders**

When using a templated letter with missing placeholders the placeholder is displayed in red bolded font in the note body. This red bolded text does not show up when letters are printed or faxed. Instead a blank space will take the place of the missing placeholder. A warning is also displayed if the patient is missing any of the expected placeholders. To resolve the warning, add the missing details. Once the placeholder details have been added you will have to reload the template by refreshing and re-selecting the desired template again.

https://canvas-medical.zendesk.com/hc/article_attachments/10925620979091

### **Restrict Enduser editing**

You can restrict whether an endusers can make changes within the letter template from the patient's chart by selecting the Restrict editing setting. This will prevent endusers from editing the content of the letter within the letter note. Endusers that attempt to edit the letter will see the message below.

!https://canvas-medical.zendesk.com/hc/article_attachments/9186733214867/desktop.gif

### **Preview, Print, and Fax Letters**

Letter templates can be previewed, printed, and faxed utilizing the functionality buttons located in the footer of the letter note.

To preview a letter, select the Preview button to open a PDF preview in a new tab. Chrome native actions are available in the top menu of this PDF preview. Once previewed, users can navigate back to the patient chart to continue to edit, print, or fax the letter.To print a letter, select the Print button to collapse the letter and view a print preview. Ensure print preview looks correct and make changes as needed to the print settings. Users can then choose to print from the print module or navigate back to the letter note to make edits. Once printed, the letter note collapses and can no longer be edited. The following message will also display at the top of the letter note: *"Printed ____ ago on ____"*

To fax a letter, select the Fax button to open the fax module. In this module you will need to provide the recipient name and the fax number with no spaces or special characters. If your organization has the fax cover sheet setting enabled please see the related article for more details. Once the appropriate fields have been filled out select Send fax button. After faxing, the letter collapses and can no longer able to be edited. The top of the letter note will display the message below along with the status of the fax. See below for actions and statuses of Letter notes. *"Faxed ____ ago on ____"*

### **Actions and Statuses of Letter Notes**

Letters have several actions that are able to be taken after a letter is completed or a status that is displayed.

- **Collapsed note** - denotes a completed letter that has been printed or faxed. Clicking the collapsed header expands the letter and allows the user to repeat a preview, print or fax action

!https://canvas-medical.zendesk.com/hc/article_attachments/6809720545683/mceclip3.gif

- **Action log** - in the note header, actions such as drafting, printing or faxing are captured with the date the action was completed
- **Fax status** - within the action log in the note header fax status is displayed
    - Fax sending via Sfax - Sending fax is in process through third party vendor SfaxFax delivered - Sfax has returned a status of a successfully delivered faxFax failed to deliver - receives a status directly from Sfax such as "Blocked Number" or "Number Busy"Failed to connect to Sfax - Sfax failed to connectSfax is not configured - Sfax has not been configured in the instance

!https://canvas-medical.zendesk.com/hc/article_attachments/6809908412947/mceclip4.png

- **Missing template placeholders** - When using a templated letter with placeholders a warning will be displayed if the patient is missing any of the expected placeholders.

!https://canvas-medical.zendesk.com/hc/article_attachments/6809094909971/mceclip1.gif

## FAQs:

**Q: How many times does Sfax try to send a fax before it is determined to be failed?**

A: Each fax is tried 3 times.

**Q: Will I receive a notification for fax status?**

A:[Fax status](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634-Letters#01G4Z7EW5TPCA09R6DJ680R0NH) is only captured in the note header.   Sfax provides the ability for users to receive email notifications for successful and failed faxes.

## Creating Letter Templates

## Introduction:

Users can create letter templates to communicate with patients through a [letter](https://canvas-medical.zendesk.com/hc/en-us/articles/360057339634), a [patient portal](https://canvas-medical.zendesk.com/hc/en-us/articles/1500003538882) message, or through a [population](https://canvas-medical.zendesk.com/hc/en-us/articles/4405414136595)/[campaign](https://canvas-medical.zendesk.com/hc/en-us/articles/6636965206547) intervention outreach. Multiple variations of the same letter can be created in different languages, for different locations, or with different titles. Front-end editing of templates can be restricted and templates can be inactivated as needed.

## Step by Step

### **Create and Update a Letter Template**

Letter templates can be configured in `Settings` under the `Letter Templates` section (in Practice header). On the main letter templates page, the list of letter templates can be seen with a table displaying template types, locations associated per template, languages per template, which are active, and which are restricted for editing by front-end users

💡 **Pro Tip:** *Use Control+F (Windows) or Command + F (Mac) to easily search all text on the page.*

Here you can select Add letter template from the letter templates module and follow the instructions at the top of the module to begin creating your letter. See below for a guide on what templates fields are available. As a general rule, any required field will be bolded. You can update letter templates from the

```
Letter Templates
```

settings view by selecting the name of the letter template and making changes as needed. Once desired changes have been made ensure you select the Save button. Configurators have the ability to preview letters by selecting Save and continue editing button to remain in the editing module and then selecting the Preview template here hyperlink.

!https://canvas-medical.zendesk.com/hc/article_attachments/9179313465619/lettemp1.gif

You can restrict an endusers ability to make changes within the letter template by selecting the Restrict editing setting. You can also mark a letter template as inactive by unselecting the Active checkbox. Both of these settings are located under the Name field.

### **Template Fields Available**

As a general rule, any required field will be bolded.

- **Name** - Name displayed when selecting a template to use in the patient chart
    - Within this field you can restrict whether an enduser can make changes to the template on the front end by selecting the Restrict editing check box.Within this field you can inactivate the template if it is no longer used by your organization by unselecting the Active checkbox.
- **Template Type** - How templates will be used. Letter templates can be used for one or multiple message types.
    - Intervention - generated within population management campaigns and is shown across all locations when template is marked as active (location restrictions do not apply)Letter - generated in the patient chart using **letter** note typeMessage - generated in the patient chart using the **message** note type. The patient receives notification by phone or email, depending on the communication channel verified on patient demographics, and then a unique link provides access to [patient app](https://canvas-medical.zendesk.com/hc/en-us/articles/360057949533).
- **Location** - Location(s) where template should be made available
    - If no location is specified it will be available in all locations.
- Header - Customize information displayed in the header of templates
    - If no content is included the current default header will be utilized.As a reminder headers and footers are not displayed in messages and interventions that are sent via the patient app.
- **Content** - Create the content of the template.
    - *Placeholders are available for personalization at letter creation. See section below.*
- Footer - Customize information displayed in the footer of templates
    - Footer content has a 5 line limit.If no content is included the current default footer will be utilized.
- **Language** - Select a language from the drop down menu to denote which language is used in the template
    - e.g English (en) and Spanish (es)

### **Customize the Header and Content fields**

Further customization of header and content fields is available through our embedded HTML editor. With this editor you are able to do the following:

- Customize text features such as style, font, typographical emphasis, size, and alignment
- Create numbered and bulleted lists
- Add images
- Create tables and edit table properties
- Add placeholders
- Upload images
    - *If a 404 error is encountered when trying to access the images folders, please contact support to ensure you have the right permissions.*
- Add special characters or horizontal lines

*With this additional HTML formatting messages are now saved in the database in HTML format. Customers using the [Communication Search](https://docs.canvasmedical.com/reference/communication-search) endpoint for their own patient applications will need to take this into account either by embedding the html directly or extracting the text. Messages sent before release (10/26/2022 @ 17:00 PST) will remain in plain text format*

As a reminder headers and footers are not displayed in messages and interventions that are sent via the patient app. Content can be previewed by selecting Save and continue editing to remain in the editing module and then selecting the Preview template here hyperlink. If the templates are not restricted, end users will have similar ability to customize the letter content on the front end with the exception of adding images.

***💡 Pro Tip:** Right click the header or content field boxes to leverage the   `<> Source code` option to make edits to your template's html code.*

https://canvas-medical.zendesk.com/hc/article_attachments/10711821139219

### **Organization Images**

Images used for letter templates must be JPEGs or PNGs under 5 MB. You have two options of uploading images for letter template customization. You can upload straight from the letter template using the image uploader icon or adding images to the

```
Organization Images
```

setting. Images added from letter templates will be automatically uploaded to the uncategorized folder.

***💡 Pro Tip:** Ensure your image has the correct name prior to uploading. This makes it easier to locate if the image will be reused. If a 404 error is encountered when trying to access the images folders, within letter templates, please contact support to ensure you have the right permissions.*

https://canvas-medical.zendesk.com/hc/article_attachments/10711898937107

Uploading images from the `Organization Images` setting gives users the option to create new folders, reload different versions of existing photos, and inactivate any existing photo.

https://canvas-medical.zendesk.com/hc/article_attachments/10738256743827

Images can be selected from the image insert icon. This icon houses the individual images within in their respective folders. To resize an image simply click and drag from one of the image corners or right click on the image and select Image to edit the width and height.

https://canvas-medical.zendesk.com/hc/article_attachments/10739280782227

### **Placeholders available**

Be sure to include the double curly brackets for any placeholder used, as displayed below. Alternatively you can also utilize the placeholder stamp to insert any of the placeholders below.

**Global**

- **{{PRACTICE_NAME}}**: practice name
- **{{PRACTICE_ADDRESS}}**: practice address on multiple lines
- **{{PRACTICE_ADDRESS_SINGLE}}**: practice address on a single line **(Coming soon - 11/2/22)**
- **{{PRACTICE_PHONE}}**: practice phone
- **{{PRACTICE_FAX}}**: practice fax
- **{{ORGANIZATION_NAME}}**: organization name
- **{{CURRENT_DATE_VERBOSE}}**: current date verbose
- **{{CURRENT_DATE_CARDINAL}}**: current date cardinal **(Coming soon - 11/2/22)**
- **{{CURRENT_DATE_COMPACT}}**: current date compact
- **{{CURRENT_DATE_TIMEZONE}}**: current date with time and timezone
- **{{CURRENT_DATE_TIME(FORMAT)}}**: current date time using [Arrow Format](https://canvas-medical.zendesk.com/hc/en-us/articles/10509707503123) **(Coming soon - 11/2/22)**

**Patient**

- **{{PATIENT_FULL_NAME}}**: patient full name
- **{{PATIENT_PREFERRED_NAME}}**: patient preferred name
- **{{PATIENT_FIRST_NAME}}**: patient first name
- **{{PATIENT_MIDDLE_NAME}}**: patient middle name
- **{{PATIENT_LAST_NAME}}**: patient last name
- **{{PATIENT_DATE_OF_BIRTH}}**: patient date of birth
- **{{PATIENT_PREFERRED_PHONE}}**: patient preferred phone
- **{{PATIENT_ADDRESS}}**: patient address on multiple lines
- **{{PATIENT_ADDRESS_SINGLE}}**: patient address on a single line **(Coming soon - 11/2/22)**
- **{{PATIENT_SSN}}**: patient SSN
- **{{PATIENT_COVERAGES}}**: active patient coverages

**Provider**

- **{{PROVIDER_CREDENTIALED_NAME}}**: provider credentialed name
- **{{PROVIDER_LICENSES}}**: provider licenses, excluding DEA
- **{{PROVIDER_SIGNATURE}}**: provider signature (if available - only shows in letters, not messages or campaign interventions)
    - *Canvas will use the [signature image](https://canvas-medical.zendesk.com/hc/en-us/articles/360061863154) that has been uploaded to Canvas for that provider. If the provider does not have a signature uploaded, Canvas will simply print the provider's name.*
- **{{PROVIDER_NPI_NUMBER}}**: provider NPI number
- **{{PROVIDER_DEA_LICENSE}}**: provider DEA license

**Staff**

- **{{STAFF_CREDENTIALED_NAME}}**: staff credentialed name

## Tips & Tricks

- If either Header or Footer fields is left blank, the default header or footer will be used.
- Headers and footers are not associated with messages
- Templates will be shown across all locations if chosen locations column is left blank
- Campaign interventions, if selected as a template type, will be shown across all locations when template is marked as active (location restrictions do not apply)
- Provider signature, if available, only shows in letters and not messages or intervention templates
- On the main letter templates page, the list of letter templates can be seen with a table displaying template types, locations associated per template, languages per template, which are active, and which are restricted for editing by front-end users

## FAQs

**Q: How can I make several selections in the template or location fields?**

A: Hold command or ctrl to multi-select in a menu.

**Q: How can I move the location selected from the available locations to the chosen locations column?**

A: Select a location by clicking the location name or multiple locations. Click on the to move between *Available location* and *Chosen locations* double dot **location column. If no location is moved to the *Chose Locations* column, the template will automatically be applied to all locations.

**Q: How can I preview my template from the settings view?**

A: Configurators have the ability to preview all content of customizable letters within the letter template settings by selecting Save and continue editing to remain in the editing module and then selecting the preview template here hyperlink