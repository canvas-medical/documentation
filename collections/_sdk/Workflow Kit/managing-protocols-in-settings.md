---
title: "Managing Protocols in Settings"
hidden: false
createdAt: "2022-02-14T18:06:44.854Z"
updatedAt: "2022-02-18T20:32:50.391Z"
---
## Viewing a Protocol in Settings

The quickstart explains how to [upload](/sdk/workflow-sdk-quickstart/#creating-a-protocol) your protocol code using the `canvas-cli upload` command. In this section, we will explore how to find and view your uploaded Protocol in the Settings section of the Canvas UI.

### Navigating to Settings

To access the Settings section in the Canvas UI, click the hamburger menu in the top portion of the main screen, and then select _Settings_ in the expanded menu:

After clicking on **Settings**, scroll down to the **Practice**section, and you will see multiple **Protocol**related models.

#### Protocol Upload

The **Protocol Upload** page displays the list of all the different protocols on your instance. 

In the table view you will see the following columns:

- **Name:** The name of the protocol (the class name in the code)
- **Active Version Link:** This will link out the active protocol upload version record where the code of the protocol lives.
- **Is active:** Boolean value representing if the protocol is actively able to be triggered on the instance.
- **Is abstract:** Boolean value representing if this is protocol is an abstract class. This means that the code isn’t a stand along protocol and other protocols inherit from this class and utilized shared functions. Currently only the DiabetesQualityMeasure is abstract since there are multiple builtin protocols that use this code.
- **Has error:** Boolean value representing if the protocols uploaded has an error in it.
- **Show in chart:** Boolean value representing if this protocol will appear in the Patient’s chart.
- **Show in population:** Boolean value representing if this protocol will appear in the Populations Page.
- **Can be snoozed:** Boolean value representing if this protocol is able to be snoozed in the Protocol Snooze command or in the protocol card on the right hand Protocols panel of a patient's chart.
- **Patients currently due:** Link that will show the protocol current values of the patients that are due for this protocol right now
- **Links:** There are two links in this column
    - The logs for this protocol to view. Logs show the most recent times this protocol has run. 
    - A link to the Protocol Upload Versions list of all the versions of this protocol that have historically been uploaded

With this table you can search and filter the list down: 

- **Text Searching** will look at the:
    - Name of the protocol
    - The Active Versions Title or Version
- **Filtering** on the right hand side by:
    - active
    - show in population
    - show in chart
    - can be snoozed
    - change type - filter by protocols that respond to a certain model (patient, appointment, encounter, etc)

There are also many **Actions** you can perform in the actions drop down menu that allow for bulk updating of records:

- **Activate / Deactivate** - Switches the boolean of whether this protocol should actively get kicked off right now
- **Mark patients due with selected protocols as not applicable** - While deactivating a protocol won’t automatically mark current due ones as not due anymore since we want these as separate actions in case they want to freeze those protocols in time. This action will take all the patients that are due for the protocol and mark them as not applicable
- **Kick off a recompute of selected protocols for all active patients -** This will kick off a background job to run the protocol for all active patients to get updated status if needed
- **Allow show in chart / Remove from show in chart -** These actions will flip the show in chart boolean value
- **Allow show in population / Remove from show in population -** These actions will flip the show in population boolean value
- **Allow snoozing / Do not allow snoozing -** These actions will flip the can be snoozed boolean value


If you click on the Name of the protocol, it will take you into the detailed page where there are two things you can exclusively do from this page:


1. **Test the Protocol against a Patient** This is the same functionality that is available when using the `canvas-cli test-fixture` command that was shown in [Create A Protocol](/sdk/workflow-sdk-quickstart/#testing-your-protocol-against-patient-data) article. To execute a test, paste a patient key into the box, and click the _Test against patient id/key_ button. You will receive output similar to the terminal output of the `test-fixture` command. 
2. **Change the Active Version** This will change the version of the Protocol that is currently active. When uploading using the `canvas-cli upload` command, the version that is uploaded is automatically set as the active version. But coming in here allows you to go back to an older version if needed.


#### Protocol Upload Version

The **Protocol Upload Version** page displays the list of all the different protocols code version on your instance. 

In the table view you will see the following columns:
- **Title:** The title of the protocol
- **Version:** The version number/string of this protocol
- **Protocol Upload:** The link to the protocol uploaded this version is associated with
- **Is active version:** Boolean value representing if this is the current active version the protocol is using
- **Can be snoozed:** Boolean representing if this version of the protocol is allowed to be snoozed using the Protocol Snooze command in the chart
- **Show in Chart:** Boolean representing if this protocol when due should appear in the Patient’s chart
- **Show in Population:** Boolean representing if this protocol should appear in the Populations View in the UI

With this table you can search and filter the list down: 

- **Text Searching** will look at the:
    - Title 
    - Version
    - The Protocol Upload class name
- **Filtering** on the right hand side by:
    - active version - only show the versions that are actively being used and hide all older versions not in use anymore
    - show in population
    - show in chart
    - can be snoozed
    - change type - filter by protocols that respond to a certain model (patient, appointment, encounter, etc)
    - protocol upload

If you click on the title of the protocol upload version, it will take you into the detailed page where you can edit information specifically about this upload version and view the code. If the version you are editing is the Protocol's active version, if you update the show in chart, show in population, can be snoozed values, it will be reflected in the Protocol Upload table as well once saved. 
