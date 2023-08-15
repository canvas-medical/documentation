---
title: "Create a Protocol"
slug: "sdk-create-a-protocol"
excerpt: "Using the Canvas Workflow Kit SDK to Create a Protocol"
hidden: false
createdAt: "2022-02-08T18:35:49.135Z"
updatedAt: "2022-11-04T20:03:23.614Z"
---
## Protocols Within Canvas

The SDK allows developers to create customized Protocols that will be utilized within a Canvas instance. Protocols are recommendations of care, screenings or actions for patients that fit certain criteria, such as age, medical history or a combination of factors.

More information about Protocols can be found [in the Canvas Knowledge Center](https://canvas-medical.zendesk.com/hc/en-us/articles/360057232994-Care-Protocols).

There are two places within the Canvas UI that Protocols can be found:

1. __In a patient's chart__ Protocols that are recommended for a patient are shown after clicking the icon that the arrow is pointing to below. The number in the red box shows that this patient has 5 active Protocols:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4a0036e-protocol_button.png",
        "protocol_button.png",
        1054,
        162,
        "#f7f5f6"
      ]
    }
  ]
}
[/block]
Once the icon is clicked, the Protocols are displayed on the right hand side of the chart. The ability to filter according to the Protocol status is available in the dropdown menu at the top. By default, a provider will see a patient's _Active_ Protocols:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/bb32062-protocol_sidebar.png",
        "protocol_sidebar.png",
        720,
        696,
        "#deddda"
      ]
    }
  ]
}
[/block]
2. __In the Populations section of the UI__ The Populations section shows all active Protocols, a listing of patients that are recommended for that Protocol, as well as the ability to create a Campaign. For more information on Populations and Campaigns, see [this article in the Canvas Knowledge Center](https://canvas-medical.zendesk.com/hc/en-us/articles/4405414136595-Population-Module#h_01FDXMBTC6RECGN3MNP3KZAAXB).
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/df1c096-canvas_hamburger_menu.png",
        "canvas_hamburger_menu.png",
        576,
        90,
        "#f3f4f5"
      ]
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/eae99f2-canvas_protocols_page.png",
        "canvas_protocols_page.png",
        360,
        368,
        "#f9f9f8"
      ]
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/59f60db-protocol_population_tab.png",
        "protocol_population_tab.png",
        396,
        520,
        "#dee2e7"
      ]
    }
  ]
}
[/block]
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
            'Protocol Reference https://canvas-medical.zendesk.com/hc/en-us/articles/360057232994-Care-Protocols'
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

1. The `MyProtocol` class is an example of how a custom Protocol can be developed using the SDK. When developing your own classes, they should always inherit from SDK's `ClinicalQualityMeasure` class as shown above. Your own Protocols, for example, may be named something like `HypertensionScreeningProtocol` or `DepressionAssessmentProtocol` depending on what type of Protocol is being developed.

2. The `ClinicalQualityMeasure` Meta class contains the following attributes:

| Name             |Type  | Required     | Description    |
| -----------    | ----- | ----------- |  ------------- |
| `title`      | _string_ | `true`|The main Protocol title that will be shown on Patient charts and the Populations tab of the Canvas UI.|
| `description`  |_string_   | `false`| A more detailed description of the Protocol. This is displayed as the subheader on the Populations section of the Canvas UI. |
| `version`   | _string_     | `true`| A version number of your choice. This is to keep track of subsequent updates to your code for a specific Protocol. Every time a version is updated to your Canvas instance, it must have a unique version number. You may want to use a date (as shown in the example) or choose a versioning method of your own. |
| `information`   | _string_  | `false`| This is for the URL that populates in the _More Info_ link for each Protocol listed on the Populations section of the UI. You may choose to populate this with the link to the page of an [eCQI](https://ecqi.healthit.gov/ep-ec) Protocol or to another resource of your choice.      |
|  `identifiers` | _list[string]_ |  `false`| This is a list of identifiers associated with the Protocol. These are sometimes populated with eCQI codes (i.e. _CMS125v6_), but can also be populated with strings of your choice to identify your custom Protocols. In the Canvas UI, these are populated underneath the Protocol title in a patient's chart.     |
| `types`      | _list[string]_     |  `false` | This is a list of shorthand, abbreviated types identified with the Protocol. Some industry standard examples of these are _CCP_, _CQM_ and _HCC_. These are populated in parentheses next to _identifiers_ in the Protocols section of a patient's chart. |
| `compute_on_change_types` | _list[CHANGE_TYPE]_ | `false`|  The change types listed here signal the Canvas backend to know when the Protocol criteria should be rerun against patients. For example, if a patient begins a new medication, they may be eligible for a Protocol whereas they may not have been before. In this case, `CHANGE_TYPE.MEDICATION` would be included in this list. A full list of CHANGE_TYPE choices are available [here](doc:change-types).     |
| `references` | _list[string]_ | `false`| A list of references identified with the Protocol. These are listed when the information icon is clicked on the Protocol listing in a patient's chart. URLs that are included in each string are automatically detected and crafted as href links with the display text. |

The following images illustrate where the attributes in the `Meta` class are shown in the Canvas UI:

On the Populations page:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0630ca7-population_tab_meta_arrows_small.png",
        "population_tab_meta_arrows_small.png",
        864,
        517,
        "#e8eaed"
      ]
    }
  ]
}
[/block]
In the Patient's Chart:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e16b1f3-patient_chart_meta_arrows.png",
        "patient_chart_meta_arrows.png",
        360,
        227,
        "#eeedee"
      ]
    }
  ]
}
[/block]
This is the view when clicking the information icon:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/cbbead6-patient_chart_meta_references.png",
        "patient_chart_meta_references.png",
        576,
        391,
        "#f0f0f0"
      ]
    }
  ]
}
[/block]
3. The `in_numerator` and `in_denominator` methods, though not filled out in the example above, are methods that can be used to compile patients into different groups. Each group can then be used in conditional logic within `compute_results`.  We will look more at how these methods can be used a little later in the tutorial.

4. The `compute_results` method is the main method that is called by the Canvas backend to determine the Protocol status and recommendations for a patient.  You should always return an instance of `ProtocolResult` in this method. The `ProtocolResult` class has the following attributes that can be set:

| Name           | Type           | Required    | Description |
| -----------  | ----------- |----------- | -----------  |
| `status` | _choice_  | `false` | This represents the status of the Protocol for a patient. The choices can be imported from `canvas_workflow_kit.protocol` as follows:<br> <br>`STATUS_DUE`<br>`STATUS_PENDING`<br>`STATUS_NOT_APPLICABLE`<br>`STATUS_SATISFIED`<br><br>In a patient's chart in the Canvas UI, Protocols with a `status` of `STATUS_DUE` will show under the _Active_ status, while `STATUS_PENDING` will show under _Pending_. Protocols with a status of `STATUS_SATISFIED`, meaning the patient has fulfilled all of the requirements, will show under the _Inactive_ status. Protocols with a `status` of `STATUS_NOT_APPLICABLE` will not show in a patient's chart.  |
| `due_in` | _integer_ | `false` | An integer that represents the number of days for when the patient is due for the Protocol. For example, if patient John is due for a Protocol 2 weeks after becoming eligible, this field would be populated with _14_. Negative integers are also allowed, and a value of _-1_ can be used for patients that are currently due. |
| `narratives` | _list[str]_ | `false` | A list of text items that will be displayed on a patient's chart within each Protocol. Each item should be thought of as being within the context of a particular patient, which can be accessed through the `self.patient` attribute. Narrative text can be appended to the `narratives` list by calling the `add_narrative()` method as shown in the example above. |

The following image shows where the arguments passed to `ProtocolResult` show up in a Protocol listed on a patient's chart:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d2e288b-protocol_result_patient_chart.png",
        "protocol_result_patient_chart.png",
        432,
        332,
        "#f1f1f1"
      ]
    }
  ]
}
[/block]
5. Recommended actions that can be taken to resolve a Protocol for a patient are presented in the bottom portion of each Protocol listed on a patient's chart. Recommendations can be added to each instance of a `ProtocolResult` by using the `add_recommendation()` method. There are [many built-in types of Recommendations available](doc:recommendation-types). Let's look at what makes up a standard `Recommendation` object:

| Name             | Type           |Required          | Description     |
| -----------    | ----------- | ----------       | ------------    |
| `key`      | _string_ | `true` | A unique identifier for the recommendation. |
| `rank` | _integer_ | `false` | A value to control the sort order of recommendations within a Protocol. For each Protocol listed in the Canvas UI, recommendations with lower rank values will appear at the top. |
| `title` | _string_ | `true` | The text to show on a patient's chart to identify and describe the recommendation. |

### Uploading Your Protocol

Canvas instances have a number of [built-in Protocols](https://canvas-medical.zendesk.com/hc/en-us/sections/4404352708115-Population-Management-Protocols). The Protocols that are developed using the SDK, such as our example above, can be uploaded and run on the Canvas backend in the same manner that the built-in Protocols are.

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
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b9a7cf0-my_first_protocol_in_chart.png",
        "my_first_protocol_in_chart.png",
        504,
        248,
        "#f3f3f3"
      ]
    }
  ]
}
[/block]
### Testing Your Protocol Against Patient Data

So far in this tutorial, you have created a basic Protocol, uploaded it to your development Canvas instance, and seen how it appears in the UI. This was a very basic measure used for example purposes. However, much more complex logic can and will be used when developing actual Protocols. For this reason, the SDK includes a command named `test-fixture` in order to test your code against patient data locally.

In the previous section, it was explained how to [fetch patient data](doc:sdk-fetching-and-viewing-patient-data) that is stored locally in _*.json_ files. To test the Protocol that you just created in `test_measure.py`, the following command can be run from within the `src` directory:

```
(env) $ canvas-cli test-fixture test_measure.py ../patients
```

This command will run the Protocol against each patient in the `/patients/` directory. If there are Protocol recommendations for a patient, those details will be printed to the console. If there are no recommendations for a patient, that will also be printed under the patient's name. Once run, the output in the terminal should look something like this:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4d63a6e-test_fixture_results_terminal.png",
        "test_fixture_results_terminal.png",
        576,
        154,
        "#282a29"
      ]
    }
  ]
}
[/block]
Now that we have our basic Protocol up and running, let's move on to [expanding and adding more functionality](doc:sdk-adding-more-functionality-to-a-protocol) to our Protocol.