---
slug: /
title: "SDK Overview"
layout: sdklandingpage
---


## Care Modeling in Action
To help customers implement and iterate on their care model in Canvas, we created the Canvas SDK. Through the Canvas SDK, customers are able to customize and extend the capabilities of Canvas by control over the design of care delivery workflows and how they manifest within Canvas inclusive of how Canvas interacts with other systems through the Canvas FHIR API.

## Current State: The Canvas Workflow Kit

The Canvas Workflow Kit is a Software Development Kit (SDK) that makes it possible to extend the functionality of a Canvas instance. By providing a built-in command-line interface, skeleton code and test commands, developers can use the SDK to customize Protocols. The Canvas Workflow Kit's original purpose was to support clinical quality measures. Through  Protocols, customers are able to drive recommendations or changes to workflow based on various patient changes. Due to the original purpose of the Canvas Workflow Kit, recommending changes in workflow or creating additional interventions based on triggers or events beyond patient data is not possible. 

Documentation on the Canvas Workflow Kit can be found [here](/sdk/sdk-quickstart/).

## Future State: The Canvas SDK

We are in the process of building a more complete and fully functional SDK. The new Canvas SDK will give customers the ability to control most aspects of workflow within Canvas and simplify the method of deploying these changes to their individual Canvas environment. There are many advantages to the new architecture, including but not limited to:
- The Canvas SDK will leverage full python packages, instead of the single sandboxed python files used today, supporting a better developer experience
- Plugins will expand coverage of the application, extending beyond patient events. Customers will be able to create workflow changes in response to user based events, application events, cron-based events, etc.
- The Commands Module will improve performance and allow for the customization of commands
Check out our documentation for the new Canvas SDK [here](https://canvas-medical.github.io/canvas-core/quickstart/plugins.html). We are working on integrating it into this site.

{% include alert.html type="info" content="Plugins are currently in beta. If you are interested in participating, please reach out to product@canvasmedical.com." %}



## Which should I use?

We are actively working on migrating existing functionality of the Canvas Workflow Kit into the new Canvas SDK. As we do this, it may be easier for you to customize Canvas using the Canvas Workflow Kit vs the new Canvas SDK and vice versa. If you are looking to create a clinical recommendation based on patient data, you should continue to utilize the Canvas Workflow Kit and Protocols. If you have a workflow you would like to support that doesn’t fit into the category just mentioned, we would love to hear about it and determine if plugins are the right choice. 

When we fully roll out the new Canvas SDK, we will partner with you to migrate existing Protocols to the new structure. More to come when ready.
