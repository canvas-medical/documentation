---
title: "Workflow SDK Quickstart"
slug: "workflow-sdk-quickstart"
excerpt: "Canvas Workflow Kit SDK Installation Quickstart"
hidden: false
createdAt: "2022-02-08T17:38:02.138Z"
updatedAt: "2022-02-16T22:42:57.253Z"
---
## Introduction

The <b>Canvas Workflow Kit</b> is a Software Development Kit (SDK) that makes it
possible to extend the functionality of a Canvas instance. By providing a
built-in command-line interface, skeleton code and test commands, developers
can use the SDK to customize Protocols. The Canvas Workflow Kit’s original
purpose was to support clinical quality measures. Through Protocols, customers
are able to drive recommendations or changes to workflow based on various
patient changes. Due to the original purpose of the Canvas Workflow Kit,
recommending changes in workflow or creating additional interventions based on
triggers or events beyond patient data is not possible.

## Installation

The SDK can either be [downloaded directly from PyPI](https://pypi.org/project/canvas-workflow-kit/) or can be installed using the Python Package Manager `pip`. Python 3.8 or above is required.

If you are new to Python, it is recommended to install packages used for development into a Python Virtual Environment rather than your system-wide installation. Instructions for setting up and activating a Virtual Environment can be [found here](https://docs.python.org/3/tutorial/venv.html).

Once your virtual environment is set up and activated, open a terminal and type the following command to install the SDK:

```
(env) $ pip install canvas-workflow-kit
```

Once the installation is complete, the `canvas-cli` command will automatically be available in the terminal. You can test this by using the `which` command:

```
(env) $ which canvas-cli
```

You should see the output location like so (the directory structure will differ based on your Python installation):

```
(env) $ which canvas-cli
/Users/{username}/Environments/env/bin/canvas-cli
```
<br>
## Initial Setup

Now it's time to set up your local environment to be able to interact with your Canvas development instance. Run the following command in the terminal:

```sh
(env) $ canvas-cli create-default-settings
```

This will create a `.canvas` folder in your home directory that contains a file named `config.ini`.

Open and edit the `~/.canvas/config.ini` file in your editor of choice, and add the *url* of your canvas instance, as well as your Canvas API key.

If you are working on a Canvas preview instance, your Canvas API key is the Bearer Token on your dashboard page. If you are on a Canvas-created dev, staging or production instance, you will need to request your API token from your Canvas Implementation Manager.

After adding your *url* and *api-key* data, your `config.ini` file should look something like this:

```
[canvas_cli]
url=https://yourcanvasinstance.canvasmedical.com/
api-key=abcdef123ccaef41d4381afdd86562de8accc999
```

Finally, create a directory in the location of your choice to store your project. For the purposes of this guide, we have created a directory called `canvas_protocols` to store our code:

```sh
(env) $ mkdir canvas_protocols
(env) $ cd canvas_protocols
(env) $ pwd
/Users/{username}/Projects/canvas_protocols
```
<br>

## Fetching Patient Data

When using the Canvas Workflow Kit, it helps to have patient data to develop and test against. The SDK allows for patient data to be fetched from a Canvas instance and populated in your project's workspace in _.json_ format.

Create a directory named `patients` within your project directory (the one that we named `canvas_protocols` [above]({{site.baseurl}}/sdk/workflow-sdk-quickstart/#initial-setup):

```sh
(env) $ pwd
/Users/{username}/Projects/canvas_protocols
(env) $ mkdir patients
```

In order to retrieve patient data for your project, you will need to find the key for each patient record that will be fetched. For the purposes of this tutorial, we recommend starting with 2 patient records (you can always retrieve more later). To find a patient's key:

1. Using a browser, log in to your Canvas instance.<br>
2. Use the Patient Search box to find an existing patient record, or create a new patient with with the _New Patient_ button: <br><br>
![Patient Search](https://files.readme.io/b856037-patient_search_sdkdocs_image.png){:width="60%"}

3. The key we are looking for is contained in the URL of the patient's chart page:<br><br>
![Image](https://files.readme.io/c95862a-be81a58-readme-quickstart-01-patient-uuid.png){:width="60%"}

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
<br><br>
## Viewing Patient Data Directly In a Browser

Another option for viewing patient data is directly in a browser. The following URL in your Canvas instance will show patient data in a _json_ structure (replace _{patient_key}_ with a valid patient key and _{your_canvas_instance}_ with the name of your instance):

`https://{your_canvas_instance}.canvasmedical.com/api/PatientProtocolInput/{patient_key}/`

The data shown in this URL will match the data fetched using the `fixture-from-patient` command. The only difference between the json files and the URL data are that each json key in the URL is represented as a separate file in the local data that was fetched from the instance.
<br><br>
## Protocols Within Canvas

The SDK allows developers to create customized Protocols that will be utilized within a Canvas instance. Protocols are recommendations of care, screenings or actions for patients that fit certain criteria, such as age, medical history or a combination of factors.

More information about Protocols can be found [in the Canvas Knowledge Center](https://canvas-medical.help.usepylon.com/articles/4408606761-care-protocols).

There are two places within the Canvas UI that Protocols can be found:

<b>In a patient's chart:</b> <br>
Protocols that are recommended for a patient are shown after clicking the icon that the arrow is pointing to below. The number in the red box shows that this patient has 5 active Protocols:
![Image](https://files.readme.io/4a0036e-protocol_button.png){:width="60%"} <br>
Once the icon is clicked, the Protocols are displayed on the right-hand side of the chart. The ability to filter according to the Protocol status is available in the dropdown menu at the top. By default, a provider will see a patient's _Active_ Protocols:
![Image](https://files.readme.io/bb32062-protocol_sidebar.png){:width="60%"}

<b>In the Populations section of the UI:</b> 
The Populations section shows all active Protocols, a listing of patients that are recommended for that Protocol, as well as the ability to create a Campaign. For more information on Populations and Campaigns, see [this article in the Canvas Knowledge Center](https://canvas-medical.help.usepylon.com/articles/3316466244-population-module).
![Image](https://files.readme.io/df1c096-canvas_hamburger_menu.png){:width="60%"}

![Image](https://files.readme.io/eae99f2-canvas_protocols_page.png){:width="60%"}

![Image](https://files.readme.io/59f60db-protocol_population_tab.png){:width="60%"}
<br><br>
## Creating a Protocol

### File Setup

So far, you should have created a project directory (in our case, `canvas_protocols`), as well as a `patients` directory. The structure of your project should currently look like this:

```
canvas_protocols/
  patients/
    PATIENT NAME YYYY (F)/
    PATIENT NAME YYYY (M)/
```

Next, create a folder called `src` within the `canvas_protocols` directory. If you are currently still in the `patients` directory, you may need to move up one level:

```
(env) $ cd ..
(env) $ mkdir src
```

Your project structure should now look like this:

```
canvas_protocols/
  patients/
    PATIENT NAME YYYY (F)/
    PATIENT NAME YYYY (M)/
  src/
```

Navigate into your newly-created `src` directory, then create a file with a _.py_ extension that you will be working in to create your first Protocol. We'll call ours `test_measure.py`.

```
(env) $ cd src
(env) $ touch test_measure.py
```
<br>

### Setting Up Initial Code

Let's begin by creating an example of a Protocol class in our Python file. Don't worry if you don't know what the following code means - it will be explained as we move through this tutorial.

Add the following code to `test_measure.py`:

```python
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_DUE,
    STATUS_SATISFIED
)

from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import Recommendation


class MyFirstProtocol(ClinicalQualityMeasure):

    class Meta:

        title = 'My First Protocol'

        description = 'My First Canvas Protocol'

        version = '2022-02-01v1'

        information = 'https://docs.canvasmedical.com'

        identifiers = ['CMS12345v1']

        types = ['CQM']

        compute_on_change_types = [
            CHANGE_TYPE.CONDITION
        ]

        references = [
            'Protocol Reference https://canvas-medical.help.usepylon.com/articles/4408606761-care-protocols'
        ]


    def in_denominator(self):
        """
        Patients in the initial population.
        """
        return True

    def in_numerator(self):
        """
        Patients that have already been notified.
        """
        return False

    def compute_results(self):
        result = ProtocolResult()

        if self.in_denominator():
            if self.in_numerator():
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    f'{self.patient.first_name} has been interviewed'
                )
            else:
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_narrative(
                    f'{self.patient.first_name} is due for an interview'
                )

                result.add_recommendation(
                    Recommendation(
                        key='CMS12345v1_CHOICE_INTERVIEW',
                        title='Interview Patient About Choices'
                    )
                )
        return result
```

Let's step through the example above:

<ol>
  <li>The <code>MyProtocol</code> class is an example of how a custom Protocol can be developed using the SDK. When developing your own classes, they should always inherit from SDK's <code>ClinicalQualityMeasure</code> class as shown above. Your own Protocols, for example, may be named something like <code>HypertensionScreeningProtocol</code> or <code>DepressionAssessmentProtocol</code> depending on what type of Protocol is being developed.</li>
  <li>The <code>ClinicalQualityMeasure</code> Meta class contains the following attributes:
    <br>
    <br>
    <table>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Required</th>
        <th>Description</th>
      </tr>
      <tr>
        <td><code>title</code></td>
        <td><em>string</em></td>
        <td><strong>true</strong></td>
        <td>The main Protocol title that will be shown on Patient charts and the Populations tab of the Canvas UI.</td>
      </tr>
      <tr>
        <td><code>description</code></td>
        <td><em>string</em></td>
        <td><strong>false</strong></td>
        <td>A more detailed description of the Protocol. This is displayed as the subheader on the Populations section of the Canvas UI.</td>
      </tr>
      <tr>
        <td><code>version</code></td>
        <td><em>string</em></td>
        <td><strong>true</strong></td>
        <td>A version number of your choice. This is to keep track of subsequent updates to your code for a specific Protocol. Every time a version is updated to your Canvas instance, it must have a unique version number. You may want to use a date (as shown in the example) or choose a versioning method of your own.</td>
      </tr>
      <tr>
        <td><code>information</code></td>
        <td><em>string</em></td>
        <td><strong>false</strong></td>
        <td>This is for the URL that populates in the <em>More Info</em> link for each Protocol listed on the Populations section of the UI. You may choose to populate this with the link to the page of an <a href="https://ecqi.healthit.gov/ep-ec">eCQI</a> Protocol or to another resource of your choice.</td>
      </tr>
      <tr>
        <td><code>identifiers</code></td>
        <td><em>list[string]</em></td>
        <td><strong>false</strong></td>
        <td>This is a list of identifiers associated with the Protocol. These are sometimes populated with eCQI codes (e.g., <em>CMS125v6</em>), but can also be populated with strings of your choice to identify your custom Protocols. In the Canvas UI, these are populated underneath the Protocol title in a patient's chart.</td>
      </tr>
      <tr>
        <td><code>types</code></td>
        <td><em>list[string]</em></td>
        <td><strong>true</strong></td>
        <td>This is a list of shorthand, abbreviated types identified with the Protocol. Some industry standard examples of these are <em>CCP</em>, <em>CQM</em>, and <em>HCC</em>. These are populated in parentheses next to <em>identifiers</em> in the Protocols section of a patient's chart.</td>
      </tr>
      <tr>
        <td><code>compute_on_change_types</code></td>
        <td><em>list[CHANGE_TYPE]</em></td>
        <td><strong>false</strong></td>
        <td>The change types listed here signal the Canvas backend to know when the Protocol criteria should be rerun against patients. For example, if a patient begins a new medication, they may be eligible for a Protocol whereas they may not have been before. In this case, <code>CHANGE_TYPE.MEDICATION</code> would be included in this list. A full list of CHANGE_TYPE choices are available <a href="doc:change-types">here</a>.</td>
      </tr>
      <tr>
        <td><code>references</code></td>
        <td><em>list[string]</em></td>
        <td><strong>false</strong></td>
        <td>A list of references identified with the Protocol. These are listed when the information icon is clicked on the Protocol listing in a patient's chart. URLs that are included in each string are automatically detected and crafted as href links with the display text.</td>
      </tr>
    </table>
  </li>
  <li>The <code>in_numerator</code> and <code>in_denominator</code> methods, though not filled out in the example above, are methods that can be used to compile patients into different groups. Each group can then be used in conditional logic within <code>compute_results</code>.  We will look more at how these methods can be used a little later in the tutorial.</li>
  <li>The <code>compute_results</code> method is the main method that is called by the Canvas backend to determine the Protocol status and recommendations for a patient.  You should always return an instance of <code>ProtocolResult</code> in this method. The <code>ProtocolResult</code> class has the following attributes that can be set:
    <br>
    <br>
    <table>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Required</th>
        <th>Description</th>
      </tr>
      <tr>
        <td><code>status</code></td>
        <td>_choice_</td>
        <td><strong>false</strong></td>
        <td>This represents the status of the Protocol for a patient. The choices can be imported from <code>canvas_workflow_kit.protocol</code> as follows:<br> <br><code>STATUS_DUE</code><br><code>STATUS_PENDING</code><br><code>STATUS_NOT_APPLICABLE</code><br><code>STATUS_SATISFIED</code><br><code>STATUS_UNCHANGED</code><br><br>In a patient's chart in the Canvas UI, Protocols with a <code>status</code> of <code>STATUS_DUE</code> will show under the <em>Active</em> status, while <code>STATUS_PENDING</code> will show under <em>Pending</em>. Protocols with a status of <code>STATUS_SATISFIED</code>, meaning the patient has fulfilled all of the requirements, will show under the <em>Inactive</em> status. Protocols with a <code>status</code> of <code>STATUS_NOT_APPLICABLE</code> will not show in a patient's chart. Protocols with a <code>status</code> of <code>STATUS_UNCHANGED</code> will ignore the current protocol run, maintaining whatever the result of the previous protocol run was. This can be useful in cases where the changed fields are not relevant.</td>
      </tr>
      <tr>
        <td><code>due_in</code></td>
        <td><em>integer</em></td>
        <td><strong>false</strong></td>
        <td>An integer that represents the number of days for when the patient is due for the Protocol. For example, if patient John is due for a Protocol 2 weeks after becoming eligible, this field would be populated with <em>14</em>. Negative integers are also allowed, and a value of <em>-1</em> can be used for patients that are currently due.</td>
      </tr>
      <tr>
        <td><code>narratives</code></td>
        <td><em>list[str]</em></td>
        <td><strong>false</strong></td>
        <td>A list of text items that will be displayed on a patient's chart within each Protocol. Each item should be thought of as being within the context of a particular patient, which can be accessed through the <code>self.patient</code> attribute. Narrative text can be appended to the <code>narratives</code> list by calling the <code>add_narrative()</code> method as shown in the example above.</td>
      </tr>
    </table>
  </li>
  <li>Recommended actions that can be taken to resolve a Protocol for a patient are presented in the bottom portion of each Protocol listed on a patient's chart. Recommendations can be added to each instance of <code>ProtocolResult</code> by using the <code>add_recommendation()</code> method. There are <a href="/sdk/recommendation-types">many built-in types of Recommendations available</a>. Let's look at what makes up a standard <code>Recommendation</code> object:
    <br>
    <br>
    <table>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Required</th>
        <th>Description</th>
      </tr>
      <tr>
        <td><code>key</code></td>
        <td><em>string</em></td>
        <td><strong>true</strong></td>
        <td>A unique identifier for the recommendation.</td>
      </tr>
      <tr>
        <td><code>rank</code></td>
        <td><em>integer</em></td>
        <td><strong>false</strong></td>
        <td>A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top.</td>
      </tr>
      <tr>
        <td><code>title</code></td>
        <td><em>string</em></td>
        <td><strong>true</strong></td>
        <td>The text to show on a patient's chart to identify and describe the recommendation.</td>
      </tr>
    </table>
  </li>
</ol>

<br><br>
### Uploading Your Protocol

Canvas instances have a number of [built-in Protocols](https://canvas-medical.help.usepylon.com/articles/4408606761-care-protocols). The Protocols that are developed using the SDK, such as our example above, can be uploaded and run on the Canvas backend in the same manner that the built-in Protocols are.

At this point, you will have a completed Protocol with all of the `Meta` attributes populated, as well as a `compute_results` method that returns an instance of `ProtocolResult`. While this is a very basic example, it is enough to upload to your Canvas development instance in order to test with and to see what appears in the UI.

To upload your code to your Canvas instance, pass the file name of your measure to the `canvas_cli upload` command. Make sure you are in the same directory as your file and run the following command in your terminal:

`(env) $ canvas-cli upload test_measure.py`

On successful upload, you should see the following message:

```
(env) $ canvas-cli upload test_measure.py
Uploading test_measure.py...
Upload successful.  Version 2022-02-01v1 set to latest version.
```

Next, pull up the chart of any patient. You should see your Measure appear in the Protocols section of that patient's chart:

<img src="https://files.readme.io/b9a7cf0-my_first_protocol_in_chart.png" alt="My First Protocol in Chart" width="60%">

By default, a protocol will recompute for all patients after it is uploaded (unless it is a [notification protocol](/sdk/notification-protocol)). If you wish to upload a protocol without recomputing for all patients, you can use the `--no-compute` flag with the upload command, like so:

`(env) $ canvas-cli upload test_measure.py --no-compute`

This can be useful for times when you want to make an update to your protocol (like a docstring change), but don't find it necessary to recompute for all patients at that time. 
The `--no-compute` flag is only available in versions of the canvas-workflow-kit >= v0.6.10, so be sure to upgrade before you use it! 

<br>

### Testing Your Protocol Against Patient Data

So far in this tutorial, you have created a basic Protocol, uploaded it to your development Canvas instance, and seen how it appears in the UI. This was a very basic measure used for example purposes. However, much more complex logic can and will be used when developing actual Protocols. For this reason, the SDK includes a command named `test-fixture` in order to test your code against patient data locally.

In the previous section, it was explained how to [fetch patient data](/sdk/workflow-sdk-quickstart/#fetching-patient-data) that is stored locally in _*.json_ files. To test the Protocol that you just created in `test_measure.py`, the following command can be run from within the `src` directory:

```
(env) $ canvas-cli test-fixture test_measure.py ../patients
```

This command will run the Protocol against each patient in the `/patients/` directory. If there are Protocol recommendations for a patient, those details will be printed to the console. If there are no recommendations for a patient, that will also be printed under the patient's name. Once run, the output in the terminal should look something like this:

<img src="https://files.readme.io/4d63a6e-test_fixture_results_terminal.png" alt="Test Fixture Results Terminal" width="60%">

<br>

## Expanding a Protocol

Building on our [previous example](/sdk/workflow-sdk-quickstart/#creating-a-protocol), we will now explore how to create logic to tell if a patient has or has not satisfied the requirements for fulfilling a Protocol. This is important in order to only display Protocol alerts for those that have not been satisfied. Conversely, we also want to display information about the Protocol under the _Inactive_ status if it indeed has been satisfied.

To help visualize this, let's say that we want to develop a Protocol for all patients 65 and older to be interviewed in order to screen their risk of falling. Patients who are eligible for this Protocol should be interviewed once a year.

As an example, a new patient, _John Smith_, is over 65 and thus would be due for our Fall Screening Protocol. Here is how the Protocol is displayed in John's chart when he arrives for his first appointment:

<img src="https://files.readme.io/ca476a8-fall_screening_protocol_in_chart.png" alt="Fall Screening Protocol in Chart" width="60%">


As recommended, John's physician can then complete the Fall Questionnaire in his chart:

<img src="https://files.readme.io/e4d8fa2-fall_screening_questionnaire.png" alt="Fall Screening Questionnaire" width="60%">


{% include alert.html type="info" content="For more information on creating Questionnaires in Canvas, see [Creating a New Questionnaire](https://canvas-medical.help.usepylon.com/articles/7418371785-creating-a-new-questionnaire)." %}

Once the recommended Fall Screening Questionnaire has been completed, the Protocol is considered to have been satisfied. It is now moved to the _Inactive_ tab in John's chart:

<img src="https://files.readme.io/8c9f063-fall_screening_satisfied.png" alt="fall_screening_satisfied.png" width="60%">
<br><br>
### The `in_numerator` and `in_denominator` Methods

In the context of our custom Protocol code, we want to be able to tell whether a patient such as John has completed the requirements to satisfy a Protocol, such as the completion of the Fall Screening Questionnaire. This can be done by using the `in_numerator` and `in_denominator` methods. The results of these methods can then be used with logic within `compute_results`.

Using our example above, the `in_denominator` method can be used to see if John exists in the population of patients that should receive the screening. The Fall Screening applies to all patients 65 or older, so our code for this method should look like this:

```python
def in_denominator(self):
    return self.patient.age_at(self.now) >= 65
```

Now let's compute whether or not John has already satisfied this Protocol. Since we saw above that the Fall Screening Protocol is satisfied after completion of the Fall Screening Questionnaire, we can see if John has fulfilled this requirement within the `in_numerator` method. First, import the relevant screening object from the Canvas Workflow Kit (we'll go into more detail about these shortly):

```python
from canvas_workflow_kit.value_set.v2021 import FallsScreening
from canvas_workflow_kit.timeframe import Timeframe
```

```python
def in_numerator(self):
    last_screening_timeframe = Timeframe(self.now.shift(years=-1), self.now)
    falls_screening = self.patient.interviews.find(
        FallsScreening
    ).within(last_screening_timeframe)
    return bool(falls_screening)
```

The methods above will tell us two things about our patient John:

1. The `in_denominator` method will tell us if John is an applicable candidate for this Protocol. Since he is in the 65 or older age bracket, this will return `True`.
2. The `in_numerator` method will tell us if John has completed the Fall Screening Questionnaire within the last year. Since he has, this will also return True.

<br>

### Incorporating Logic into `compute_results`

We can now use the logic from both of these methods in `compute_results`:

```python
    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator(): # Patient is 65 or older
            if self.in_numerator(): # Has completed the Screening
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    f'{self.patient.first_name} has been screened for fall risk in the past year.'
                )
            else: # Has not completed the Screening
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_recommendation(
                    InterviewRecommendation(
                        key='CMS139v9_INTERVIEW_RECOMMENDATION',
                        rank=1,
                        button='Interview',
                        patient=self.patient,
                        questionnaires=[FallsScreening],
                        title=f'Complete the Fall Screening Questionnaire',
                    )
                )
        return result
```

As you can see above, we marked the Status as `STATUS_DUE` for when John had not completed the Questionnaire, as well as a recommendation to do so. After John had completed the Questionnaire, a status of `STATUS_SATISFIED` was set.
<br><br>
### A Complete Example

Here is the complete example of the Protocol for the example above:

```python
from canvas_workflow_kit.protocol import (
    ClinicalQualityMeasure,
    ProtocolResult,
    STATUS_DUE,
    STATUS_SATISFIED,
)
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.recommendation import InterviewRecommendation


from canvas_workflow_kit.value_set.v2021 import (
    FallsScreening
)
from canvas_workflow_kit.timeframe import Timeframe


class SeniorFallProtocol(ClinicalQualityMeasure):

    class Meta:

        title = 'Preventive Care and Screening: Fall Screening'

        description = 'Fall Screening for Patients 65 and older'

        version = '2022-02-01v7'

        information = 'https://ecqi.healthit.gov/ecqm/ep/2021/cms139v9'

        identifiers = ['CMS139v9']

        types = ['CQM']

        compute_on_change_types = [
            CHANGE_TYPE.CONDITION,
            CHANGE_TYPE.PATIENT,
        ]

        references = [
            'Falls: Screening for Future Fall Risk https://ecqi.healthit.gov/ecqm/ep/2021/cms139v9'
        ]

    def in_denominator(self):
        """
        Patients in the initial population.
        """
        return self.patient.age_at(self.now) >= 65

    def in_numerator(self):
        last_screening_timeframe = Timeframe(self.now.shift(years=-1), self.now)
        falls_screening = self.patient.interviews.find(
            FallsScreening
        ).within(last_screening_timeframe)
        return bool(falls_screening)

    def compute_results(self):
        result = ProtocolResult()
        if self.in_denominator(): # Patient is 65 or older
            if self.in_numerator(): # Has completed the Screening
                result.status = STATUS_SATISFIED
                result.add_narrative(
                    f'{self.patient.first_name} has been screened for fall risk in the past year.'
                )
            else: # Has not completed the Screening
                result.status = STATUS_DUE
                result.due_in = -1
                result.add_recommendation(
                    InterviewRecommendation(
                        key='CMS139v9_INTERVIEW_RECOMMENDATION',
                        rank=1,
                        button='Interview',
                        patient=self.patient,
                        questionnaires=[FallsScreening],
                        title=f'Complete the Fall Screening Questionnaire',
                    )
                )
        return result
```
<br>

### Recommendations and Next Steps

You may have noticed that instead of using a generic `Recommendation` in our `add_recommendation` method, we used an `InterviewRecommendation`. The SDK includes a number of recommendation classes, which you can explore in the [Canvas SDK Recommendation Types doc](/sdk/recommendation-types).

