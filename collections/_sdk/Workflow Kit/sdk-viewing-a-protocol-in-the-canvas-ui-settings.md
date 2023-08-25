---
title: "Viewing a Protocol in the Canvas UI Settings"
slug: "sdk-viewing-a-protocol-in-the-canvas-ui-settings"
hidden: false
createdAt: "2022-02-14T18:06:44.854Z"
updatedAt: "2022-02-18T20:32:50.391Z"
---
## Viewing a Protocol in Settings

In the previous article on how to [Create a Protocol](doc:sdk-create-a-protocol), it was shown how to upload your Protocol code using the `canvas-cli upload` command. In this section, we will explore how to find and view your uploaded Protocol in the Settings section of the Canvas UI.

### Navigating to Settings

To access the Settings section in the Canvas UI, click the hamburger menu in the top portion of the main screen, and then select _Settings_ in the expanded menu:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/db5cc8d-e074881-readme-quickstart-02-hamburger_button.png",
        "e074881-readme-quickstart-02-hamburger_button.png",
        520,
        166,
        "#bec4be"
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
        "https://files.readme.io/ed48d7c-1de1f56-readme-quickstart-03-settings.png",
        "1de1f56-readme-quickstart-03-settings.png",
        282,
        501,
        "#e9e5e6"
      ]
    }
  ]
}
[/block]
After clicking on _Settings_, scroll down to the _Practice_ section, and then select _Protocol Uploads_: 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c572353-49844bc-readme-quickstart-05-protocol_uploads.png",
        "49844bc-readme-quickstart-05-protocol_uploads.png",
        688,
        373,
        "#d4d9de"
      ]
    }
  ]
}
[/block]
You should see your uploaded Protocol in the list like so:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ef43d5f-94069ac-readme-quickstart-06-protocol_uploads_screen.png",
        "94069ac-readme-quickstart-06-protocol_uploads_screen.png",
        1004,
        466,
        "#d6d7da"
      ]
    }
  ]
}
[/block]
Click on the link of your Protocol and you will be taken to the following page:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/aecf2ac-e04fd23-readme-quickstart-07-edit_protocol.png",
        "e04fd23-readme-quickstart-07-edit_protocol.png",
        764,
        607,
        "#ebe1e3"
      ]
    }
  ]
}
[/block]
Within this detailed page, the following options are available:

1. __Test the Protocol against a Patient__ This is the same functionality that is available when using the `canvas-cli test-fixture` command that was shown in [Create A Protocol](https://docs.canvasmedical.com/docs/create-a-protocol-se-81-unpublished#testing-your-protocol-against-patient-data) article. To execute a test, paste a patient key into the box, and click the _Test against patient id/key_ button. You will receive output similar to the terminal output of the`test-fixture` command. 
2. __View the change history of the Protocol__ This will show the changes made to the Protocol entry after upload. Please note that this will only show changes made through the UI.
3. __Toggle Active Status__ This will activate or deactivate the Protocol.
4. __Change the Active Version__ This will change the version of the Protocol that is currently active. When uploading using the `canvas-cli upload` command, the version that is uploaded is automatically set as the active version.
5. __Is Abstract__ Toggle the abstract state of the Protocol.
6. __Error__ View any error details that are generated from the Protocol's execution.
7. __Delete__ Delete the Protocol.
8. __Save Functionality__ Save any changes made to the Protocol via the Settings page.