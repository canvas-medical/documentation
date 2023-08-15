---
title: "Fetching and Viewing Patient Data"
slug: "sdk-fetching-and-viewing-patient-data"
excerpt: "Using the Canvas Workflow Kit SDK to Fetch Patient Data"
hidden: false
createdAt: "2022-02-08T17:52:39.949Z"
updatedAt: "2023-02-08T14:45:59.649Z"
---
## Fetching Patient Data

When using the Canvas Workflow Kit, it helps to have patient data to develop and test against. The SDK allows for patient data to be fetched from a Canvas instance and populated in your project's workspace in _.json_ format.

Create a directory named `patients` within your project directory (the one that we named `canvas_protocols` in the [Initial Setup section](doc:sdk-quickstart#initial-setup) in the Quickstart):

```sh
(env) $ pwd
/Users/{username}/Projects/canvas_protocols
(env) $ mkdir patients
```

In order to retrieve patient data for your project, you will need to find the key for each patient record that will be fetched. For the purposes of this tutorial, we recommend starting with 2 patient records (you can always retrieve more later). To find a patient's key:

1. Using a browser, log in to your Canvas instance.
2. Use the Patient Search box to find an existing patient record, or create a new patient with with the _New Patient_ button:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b856037-patient_search_sdkdocs_image.png",
        "patient_search_sdkdocs_image.png",
        1210,
        376,
        "#c9e0e1"
      ]
    }
  ]
}
[/block]
3. The key we are looking for is contained in the URL of the patient's chart page:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c95862a-be81a58-readme-quickstart-01-patient-uuid.png",
        "be81a58-readme-quickstart-01-patient-uuid.png",
        1716,
        532,
        "#c4c6cb"
      ]
    }
  ]
}
[/block]
Now that your `patients/` directory has been created and you have found a patient's key, navigate into the `patients` directory:

```
(env) $ cd patients
```

Run the following `canvas-cli fixture-from-patient` command (replace `<patient_key>` with the key from above):

```
(env) $ canvas-cli fixture-from-patient <patient_key>
```

You should get a success message and a directory containing the patient's data:

```sh
(env) $ canvas-cli fixture-from-patient 265b00201239436485d1f2fa423a6056
Successfully wrote patient fixture to /Users/{username}/Projects/canvas_protocols/patients/Daphne Smith 1969 (F)
```

The directory that is created is a series of JSON files built from the patient record keys *(billing_line_items.json, conditions.json, imaging_reports.json, etc.)*:

```sh
(env) $ cd Daphne\ Blake\ 1969\ \(F\)/
(env) $ ls
billing_line_items.json
conditions.json
imaging_reports.json
immunizations.json
inpatient_stay.json
instructions.json
interviews.json
lab_reports.json
medications.json
messages.json
patient.json
protocol_overrides.json
protocols.json
reason_for_visits.json
referral_reports.json
referrals.json
suspect_hccs.json
upcoming_appointment_notes.json
upcoming_appointments.json
vital_signs.json
```

Repeat the above steps to retrieve 1 or more patients.

We will see how these patient data files can be used for development and testing in the next section.

## Viewing Patient Data Directly In a Browser

Another option for viewing patient data is directly in a browser. The following URL in your Canvas instance will show patient data in a _json_ structure (replace _{patient_key}_ with a valid patient key and _{your_canvas_instance}_ with the name of your instance):

`https://{your_canvas_instance}.canvasmedical.com/api/PatientProtocolInput/{patient_key}/`

The data shown in this URL will match the data fetched using the `fixture-from-patient` command. The only difference between the json files and the URL data are that each json key in the URL is represented as a separate file in the local data that was fetched from the instance.

Now let's move on to creating our first [Protocol](doc:sdk-create-a-protocol).