---
title: "Constance Config"
layout: documentation
---

Constance Config allows you to enable/disable and customize certain features within Canvas. The values can either be set by checking or unchecking the box (checked = true) or setting the values as desired. It is broken down into the following sections. 

## Billing

|Setting|Default |Description|
| ----------- | ----------- | ----------- |
|AUTOMATED_INVOICING |False|Invoiced will automatically be generated after a balance falls to patient responsibility.|
|INVOICE_INTERVAL |15|Number of days between automatic invoicing for unpaid patient balances |
|ADJUSTMENT_BEHAVIOR_DESCRIPTION|False|Makes descriptions required when an adjustment deviates from its default behavior. |
|ALLOW_LOB_FOR_INVOICING |False|Canvas has partnered with LOB for patient invoicing. LOB provides direct mail services. LOB is a pass through variable cost based on usage|
|ALLOW_EMAIL_FOR_INVOICING |False |Enables e-mail as preferred method when sending invoices |
|<img width=300/>|<img width=50/>|<img width=300/>|


## Business Lines

|Setting|Default |Description|
| ----------- | ----------- | ----------- |
|ENABLE_BUSINESS_LINES|False |Description|


## Claim.MD Configuration

|Setting|Default |Description|
| ----------- | ----------- | ----------- |
|CLAIM_MD_CLEARINGHOUSE_USER_ID |Blank | Username for the customer Claim.MD account. This is typically added during implementation|
|CLAIM_MD_CLEARINGHOUSE_ACCOUNT_KEY  |Blank |Account key for the customer Claim.MD account. This is typically added during implementation|
|<img width=300/>|<img width=50/>|<img width=300/>|


## Clinical Signature Restrictions
NAME
DEFAULT
VALUE
IS MODIFIED
RESTRICT_MEDICATION_ORDERS_TO_PRESCRIBER 
Support: Only the Prescriber listed in a medication order command (such as Prescribe, Refill, or Adjust Medication) can commit the order.
Any user can initiate the command, however.
False


Reset to default	False
RESTRICT_NOTE_SIGNING_TO_PROVIDER 
Support: Only the provider can Sign/Amend a note
False


Reset to default	False
RESTRICT_SIGNING_NOTE_WITH_UNCOMMITTED_COMMANDS 
Support: Commands must be committed before Signing note
False


Reset to default	False

## Communication
NAME
DEFAULT
VALUE
IS MODIFIED
ENABLE_EXTERNAL_MESSAGE 
Support: Enable this to send messages through protocols. Depends on customer
False


Reset to default	False
ENABLE_PATIENT_COMMUNICATION 
Support: Disable this to prevent phone/email verifications being sent from Canvas UI.
Disabling this communication setting does not impact the patient appointment reminder settings.
Communication sent for appointment reminders requires configuration within the organization settings.
True


Reset to default	False
TELEHEALTH_INSTRUCTIONS_SMS_MESSAGE_BODY 
Support: Configure sms message body for telehealth appointment instructions.

Use {practice_name} in the message to display the practice location's name
Use {formatted_phone} in the message to display the practice location's phone number
Use {patient_first_name} in the message to display the patient's first name
Use {telehealth_link} in the message to display the telehealth link for the appointment
Use {start_time_only} in the message to display the start time of the appointment
It's almost time for your {practice_name} telehealth appointment. Please download the Zoom app if you haven't yet: https://zoom.us/download

Please join your appointment 5 minutes before your scheduled start time of {start_time_only}: {telehealth_link}

It's almost time for your {practice_name} telehealth appointment. Please download the Zoom app if you haven't yet: https://zoom.us/download

Please join your appointment 5 minutes before your scheduled start time of {start_time_only}: {telehealth_link}

Reset to default	False
TELEHEALTH_INSTRUCTIONS_HTML_MESSAGE_BODY 
Support: Configure html message body for telehealth appointment instructions.

Use {practice_name} in the message to display the practice location's name
Use {formatted_phone} in the message to display the practice location's phone number
Use {patient_first_name} in the message to display the patient's first name
Use {telehealth_link} in the message to display the telehealth link for the appointment
Use {start_time_only} in the message to display the start time of the appointment
<p>Hi {patient_first_name},</p><p>It's almost time for your {practice_name} telehealth appointment.</p><p><strong>Get ready!</strong></p><p>Please download Zoom if you haven't already:</p><ul><li><a href="https://zoom.us/client/latest/ZoomInstaller.exe">Windows</a></li><li><a href="https://zoom.us/client/latest/Zoom.pkg">Mac</a></li><li><a href="https://play.google.com/store/apps/details?id=us.zoom.videomeetings">Android</a></li><li><a href="https://itunes.apple.com/us/app/id546505307">iPhone</a></li></ul><p><strong>Go!</strong></p><p>Please join your appointment 5 minutes before your scheduled appointment time of {start_time_only}.</p><p><a href="{telehealth_link}">Click this link to start your appointment.</a></p><p>Your Care Team at {practice_name}</p>

<p>Hi {patient_first_name},</p><p>It's almost time for your {practice_name} telehealth appointment.</p><p><strong>Get ready!</strong></p><p>Please download Zoom if you haven't already:</p><ul><li><a href="https://zoom.us/client/latest/ZoomInstaller.exe">Windows</a></li><li><a href="https://zoom.us/client/latest/Zoom.pkg">Mac</a></li><li><a href="https://play.google.com/store/apps/details?id=us.zoom.videomeetings">Android</a></li><li><a href="https://itunes.apple.com/us/app/id546505307">iPhone</a></li></ul><p><strong>Go!</strong></p><p>Please join your appointment 5 minutes before your scheduled appointment time of {start_time_only}.</p><p><a href="{telehealth_link}">Click this link to start your appointment.</a></p><p>Your Care Team at {practice_name}</p>

Reset to default	False
FAX_COVER_SHEET 
Support: Adds a custom cover sheet to faxes.
False


Reset to default	False

## Dialing Service
NAME
DEFAULT
VALUE
IS MODIFIED
DIALING_LABEL 
Support: The name of the phone number software e.g. Acme Software

Reset to default	False
DIALING_URL_TEMPLATE 
Support: The url used to dial the phon number. Use {number} in the url to indicate the phone number placement in the url. e.g. https://phone.canvasmedical.com/call?number={phone_number}

Reset to default	False

## Drug and Allergy Warning Level
NAME
DEFAULT
VALUE
IS MODIFIED
DRUG_INTERACTION_WARNING_LEVEL 
Drug/Drug Interaction Warning Level
Show-All


Show All Drug/Drug Interaction Warnings

Reset to default	False
ALLERGY_WARNING_LEVEL 
Allergy Warning Level
Show-All


Show All Allergy Warnings

Reset to default	False
PREVENT_PRESCRIBING_AT_ALLERGY_LEVEL 
Prevent Prescribing at Allergy Level
severe


Severe

Reset to default	False

## Feature Configuration
NAME
DEFAULT
VALUE
IS MODIFIED
STRUCTURED_REASON_FOR_VISIT_ENABLED 
Support: Enable/disable using structured reason for visit
False


Reset to default	False
USE_LAST_REASON_FOR_VISIT_FOR_NOTE_HEADER 
Support: Enable/disable using the latest reason for visit command as the note header. (Default setting is the first reason for visit command as the note header)
False


Reset to default	False
HIDE_LOGIN_BUTTON_IN_VERIFICATION_WORKFLOW 
Support: Hides login button during the email/text verification workflow
False


Reset to default	False
ALLOW_DOUBLE_BOOKING 
Support: Enable/disable ability to book more than one patient for a specific provider within the same time frame.
True


Reset to default	False
PREFERRED_NAME 
Support: Enable/disable use of preferred name instead of first name in patient communications.
False


Reset to default	False
DEFAULT_APPOINTMENT_DURATION 
Support: Set duration to be selected by default when creating appointments
20

20

Reset to default	False
DEFAULT_SCHEDULE_EVENT_TYPE 
Support: Schedule event type to be selected by default on the UI
None


---

Reset to default	False
APPOINTMENT_STATUS_ONCE_CHECKED_IN 
This configuration will mark the appointment.status field to the value selected when the check-in button on the Note is clicked.
The calendar/schedule view will have that appointment block turn the corresponding color of that appointment.status field value.
None


---

Reset to default	False
HIDE_TELEHEALTH_BUTTON_IN_NOTE_HEADER 
Support: Canvas note for telehealth appointment automatically include a zoom button on the top right when the visit is checked in. By enabling this configuration, the button will be hidden on the header.
False


Reset to default	False
REQUEST_RECORDS_TASK 
Support: When enabled, protocol cards will have a request records button that when selected will create a task to obtain medical records.
True


Reset to default	False
DEFAULT_NUMBER_OF_APPOINTMENTS_TO_FETCH 
Support: By default fetch this number of appointments for the schedule view (Max: 350)
300

300

Reset to default	False

## Multi-Factor Authentication
NAME
DEFAULT
VALUE
IS MODIFIED
MFA_REQUIRED 
Support: Force all users to set up multi-factor authentication
False


Reset to default	False
MFA_ALLOW_EMAIL 
Support: Allow MFA via email
True


Reset to default	False
MFA_ALLOW_ALTERNATE_EMAIL 
Support: Allow custom email addresses when specifying an email for MFA
True


Reset to default	False
MFA_ALLOW_SMS 
Support: Allow MFA via text message
True


Reset to default	False
MFA_ALLOW_ALTERNATE_SMS 
Support: Allow custom phone numbers when specifying an SMS number for MFA
True


Reset to default	False
MFA_ALLOW_AUTHENTICATOR_APP 
Support: Allow MFA via authenticator app (like Google Authenticator)
True


Reset to default	False
MFA_REMEMBER_DAYS 
Support: Number of days to remember MFA for
30

30

Reset to default	False

## Network Settings
NAME
DEFAULT
VALUE
IS MODIFIED
NETWORK_STATUS_DIMMER_ENABLED 
Support: Enable network status dimmer over notes
False


Reset to default	False

## Patient App
NAME
DEFAULT
VALUE
IS MODIFIED
PATIENT_APP_MESSAGING 
Support: Enable the Messaging page in the patient app
True


Reset to default	False
PATIENT_APP_PAYMENTS 
Support: Enable the Payment page in the patient app
True


Reset to default	False
PATIENT_APP_LABS 
Support: Enable the Lab page in the patient app
True


Reset to default	False
PATIENT_APP_CONTACT 
Support: Enable the Contact page in the patient app
True


Reset to default	False
PATIENT_APP_RECORDS 
Support: Enable the Health Records page in the patient app.
False


Reset to default	False

## Registration
NAME
DEFAULT
VALUE
IS MODIFIED
ENABLE_TIMEZONE 
Support: Enable preferred timezone for patients
False


Reset to default	False
ENABLE_PATIENTS_CONSENTS 
Support: Enable patient consents
True


Reset to default	False
ENABLE_PATIENT_METADATA 
Support: When enabled, users will have access to a metadata section on the patient registration page, below coverages.
False


Reset to default	False
ENABLE_HOMELESS_LOCATION 
Support: Provider can enter a free text Last Known Location for unhoused individuals without a permanent address
False


Reset to default	False
COVERAGE_CREATE_WITH_QR 
Support: Create coverages with QR code
True


Reset to default	False

## Reporting
NAME
DEFAULT
VALUE
IS MODIFIED
REPORT_EMAIL 
Support: A comma-separated list of email addresses where staff reports should be sent. Usually different for every customer.

Reset to default	False

## SSO Configuration
NAME
DEFAULT
VALUE
IS MODIFIED
SERVICE_PROVIDER_CONFIG 
Engineering: Dictionary with custom service provider configuration
{}

{}

Reset to default	False
SSO_PRIVATE_KEY 
Engineering: Private key base64 encoded

Reset to default	False
SSO_PUBLIC_CERT 
Engineering: Public cert base64 encoded

Reset to default	False
IDP_METADATA_XML 
Engineering: IdP metadata xml file base64 encoded

Reset to default	False
SSO_LOGIN_ENABLED 
Engineering: Enable SSO login link in the login page
False


Reset to default	False
SSO_IDP_INFO 
Engineering: Identity provider information
{}

{}

Reset to default	False

## Sfax Configuration
NAME
DEFAULT
VALUE
IS MODIFIED
SFAX_USERNAME 
Support: Sfax username. Usually different for every customer.

Reset to default	False
SFAX_APIKEY 
Support: Sfax API key. Usually different for every customer.

Reset to default	False
SFAX_ENCRYPTIONKEY 
Support: Sfax encryption key. Usually different for every customer.

Reset to default	False
SFAX_VECTOR 
Support: Sfax initialization vector. Usually different for every customer.

Reset to default	False

## Stripe Configuration
NAME
DEFAULT
VALUE
IS MODIFIED
STRIPE_API_KEY 
Support: The API key for authenticating to Stripe. Usually different for every customer.

Reset to default	False
STRIPE_PUBLIC_KEY 
Support: The public key for authenticating to Stripe. Usually different for every customer.

Reset to default	False
STRIPE_CONNECTED_ACCOUNT_ID 
Support: The ID of the customer Stripe account. Usually different for every customer.

Reset to default	False
