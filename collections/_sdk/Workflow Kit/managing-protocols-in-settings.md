---
title: "Managing Protocols in Settings"
hidden: false
createdAt: "2022-02-14T18:06:44.854Z"
updatedAt: "2022-02-18T20:32:50.391Z"
---
## Viewing a Protocol in Settings

The quickstart explains how to [upload](/sdk/sdk-quickstart/#creating-a-protocol) your protocol code using the `canvas-cli upload` command. In this section, we will explore how to find and view your uploaded Protocol in the Settings section of the Canvas UI.

### Navigating to Settings

To access the Settings section in the Canvas UI, click the hamburger menu in the top portion of the main screen, and then select _Settings_ in the expanded menu:
<!-- Image 1 -->
<div>
    <img src="https://files.readme.io/db5cc8d-e074881-readme-quickstart-02-hamburger_button.png" alt="Hamburger Button" width="520" height="166" style="background-color: #bec4be;">
</div>
<p>After clicking on <em>Settings</em>, scroll down to the <em>Practice</em> section, and then select <em>Protocol Uploads:</em></p>

<!-- Image 2 -->
<div>
    <img src="https://files.readme.io/ed48d7c-1de1f56-readme-quickstart-03-settings.png" alt="Settings" width="282" height="501" style="background-color: #e9e5e6;">
</div>
<p>You should see your uploaded Protocol in the list like so:</p>

<!-- Image 3 -->
<div>
    <img src="https://files.readme.io/c572353-49844bc-readme-quickstart-05-protocol_uploads.png" alt="Protocol Uploads" width="688" height="373" style="background-color: #d4d9de;">
</div>
<p>Click on the link of your Protocol and you will be taken to the following page:</p>

<!-- Image 4 -->
<div>
    <img src="https://files.readme.io/ef43d5f-94069ac-readme-quickstart-06-protocol_uploads_screen.png" alt="Protocol Uploads Screen" width="1004" height="466" style="background-color: #d6d7da;">
</div>
<p>This is the page for editing your Protocol:</p>

<!-- Image 5 -->
<div>
    <img src="https://files.readme.io/aecf2ac-e04fd23-readme-quickstart-07-edit_protocol.png" alt="Edit Protocol" width="764" height="607" style="background-color: #ebe1e3;">
</div>

Within this detailed page, the following options are available:

1. __Test the Protocol against a Patient__ This is the same functionality that is available when using the `canvas-cli test-fixture` command that was shown in [Create A Protocol](https://docs.canvasmedical.com/docs/create-a-protocol-se-81-unpublished#testing-your-protocol-against-patient-data) article. To execute a test, paste a patient key into the box, and click the _Test against patient id/key_ button. You will receive output similar to the terminal output of the`test-fixture` command. 
2. __View the change history of the Protocol__ This will show the changes made to the Protocol entry after upload. Please note that this will only show changes made through the UI.
3. __Toggle Active Status__ This will activate or deactivate the Protocol.
4. __Change the Active Version__ This will change the version of the Protocol that is currently active. When uploading using the `canvas-cli upload` command, the version that is uploaded is automatically set as the active version.
5. __Is Abstract__ Toggle the abstract state of the Protocol.
6. __Error__ View any error details that are generated from the Protocol's execution.
7. __Delete__ Delete the Protocol.
8. __Save Functionality__ Save any changes made to the Protocol via the Settings page.