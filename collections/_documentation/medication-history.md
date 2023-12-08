---
title: Surescripts Medication History
layout: documentation
---

Surescripts Medication History provides data on medication fill received directly from pharmacies and pharmacy benefit managers. This data is critical for care teams to understand medication adherence, to remove barriers to care and close the loop on important therapies. Canvas offers an out of the box integration that enables you to get this history. You can surface it to front end users and also make it available for reporting.

{% include alert.html type="info" content="This is a new feature in beta. Please reach out to Canvas to activate." %}
<!--
### Enabling the Feature
Currently these steps are taken by Canvas.
1. **Manual Activation**: Go to `Admin > Patients` and click “Medication history” next to a patient’s name. This requires `MEDICATION_HISTORY_SUPPORT` configuration to be active.
2. **Automatic Daily Requests**: Enable the `MEDICATION_HISTORY_DAILY_REQUESTS` config. This will trigger daily automatic medication history requests.-->

## How to request and view Medication History

There are two ways to request medical history:
- **Manual Requests**: Through the patient’s profile in the Admin section. Navigate to `Admin > Patients` and click “Medication history” next to a patient’s name.
- **Automatic Requests**: A scheduled task runs every 10 minutes to check for patients needing a daily medication history request. Requests are sent if not already made that calendar day.

Making requests causes the following series of events to occur:
- **Request Sent**: A `MedicationHistoryRequest` is sent to Surescripts for a patient.
- **Response Received**: Surescripts returns a `MedicationHistoryResponse` which contains medication fill data or a denial notice.

Every time a request is made, it comes from a specific provider. When making a request in the UI, the active user is the requester. When making nightly automatic requests, theres is some logic to be aware of. First the systme looks for the staff member with the care team role defined in the config `MEDICATION_HISTORY_DAILY_REQUESTS_STAFF_ROLE` for each patient. If there is no staff member with that care team role, then it falls back to the staff defined in `MEDICATION_HISTORY_DAILY_REQUESTS_DEFAULT_STAFF_USERNAME`. If neither of these is filled out there is no provider to request under and so no requests will go out.

After a response has been received, Medication History can be consumed in two ways:
- **User interface**: First, it can be viewed in the user interface in the admin section as mentioned above (`Admin > Patients` and click “Medication history” next to a patient’s name).
- **Database**: Data that is received is saved in your read-only replica, so that you can use it for reporting or taking automated actions.

## Understanding the data

### Source of the data

Surescripts is the network through which the data is received. The sources of the data are:
- Pharmacies - up to 90% of pharmacies support this feature.
- Pharmacy Benefit Managers (PBMs)

### Filled vs. sold

Both Pharmacies and PBMs will include medication data when a fill event occurs. Often this happens when the prescription is received by the pharmacy. Note that a fill event can occur before the medication is sold (i.e. before the patient actually acquires the medication). If a medication is filled and a patient does pick up or receive the medication, then the claim will be reversed and the medication will no longer appear in the Medication History response from Surescripts. One value that can be useful in this regard is `SoldDate` - this is sometimes sent by the pharmacy and is only included if the medication was actually sold to the patient.

### Additional guidance

- **Surescripts deduplication**: Currently, deduplication is not enabled, meaning duplicate entries from PBMs and pharmacies may appear.
- **Matching algorithm**: Patient demographics from pharmacies and PBMs are used for matching, which might not always be consistent across both sources.
- **Reasons for errors**: There are some known reasons that Surescripts will return an error. These include:
	- Patient has special characters in name
	- Patient has no address
	- Requesting provider has no address
	- Requesting provider does not have a valid NPI

## Structure of the data

For technical users who need more information about the database tables, here is a summary of the relevant tables:
- **MedicationHistoryResponse**: This table records each response received from Surescripts. Each row in this table represents a unique response from Surescripts for a specific patient. For instance, if two requests are made on different dates and Surescripts sends responses for each, there will be two separate rows in this table, one for each response date.
- **MedicationHistoryMedication**: This table stores specific medication data from the Surescripts responses. Each row is an instance of a fill event for a given patient. However please note that this table is pruned with every Surescripts response. Specifically, every time a new response is received, all rows in this table for the given patient and date range and overwritten. Therefore this table will always include the most up to date medication history information for all patients. As an example, if a fill was reversed and medication history is requested again, that fill would no longer appear in this table.
- **MedicationHistoryMedicationCoding**: this table contains coding information for each medication in the above table. This is amost always NDC code.

Important notes regarding the tables:
- **No Unique IDs for Fills**: Surescripts does not provide unique IDs for fill events, so it is not possible to map fill events uniquely from request to request.
- **No Direct Mapping**: There is currently no direct mapping between the MedicationHistoryResponse and MedicationHistoryMedication tables.




