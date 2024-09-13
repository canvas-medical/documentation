---
slug: /
title: "The Canvas SDK"
layout: sdk
---
A guiding belief at Canvas is that much faster iteration on clinical protocols and surrounding workflow is a vital core competency to improving the effectiveness of care and increase access to it. Software should enable faster iteration of care models not impede it. Since day one, Canvas has sought to give every care delivery organization the tools to differentiate their care model to drive lower cost, better quality, or both.

The new Canvas SDK takes the validated capabilities of the existing Canvas Workflow Kit, simplifies and amplifies them. Moreover it significantly improves the developer experience and facilitates more effective collaboration between the individuals delivering care and those responsible for the software systems. Lastly, it enables developers to customize more of Canvas as they see fit using a wider variety of inputs to determine when to trigger those customizations and more areas of Canvas that can be customized through a wider area of effects and UI control points.

With the Canvas SDK, organizations will be able to not only implement and continuously improve clinical protocols, but also a wide variety of different use cases across operational and financial objectives.

{% include alert.html type="warning" content="The Canvas SDK is currently in closed Beta release." %}

Ready to get started right away? Check out this [guide](/guides/your-first-plugin/).


## What is the Canvas SDK?

The Canvas SDK is your toolkit for customizing workflows natively across the full Canvas platform: scheduling, charting, billing, and more. It is a [python package](https://pypi.org/project/canvas/) comprised of seven modules that help customers implement and iterate on their care model in Canvas. The Canvas SDK will replace the Canvas Workflow Kit when released for General Availability, and offers a far greater breadth of event triggers, contextual data, UI control points, and improved developer ergonomics.

## What purpose does the Canvas SDK serve?

The Canvas SDK, in conjunction with the Canvas FHIR API, is designed to let organizations rapidly build and continuously optimize custom EMRs that map to their care delivery model. Organizations are able to use a cloud-based EMR development platform to introduce programmatic logic to customize their Canvas instance through Python packages - Plugins. With the Canvas SDK, organizations can create Plugins that control workflows, the interaction design, and how various systems (internal and external to Canvas) interact with one another. Plugins enable organizations to respond to any event, trigger recommendations for any type of action, integrate easily with external tools, and automate any process, fast.

### What is a Plugin?

A Plugin is a Python package that a developer can write and upload to their Canvas instance to completely independently customize their Canvas instance. A Plugin can be a very small customization or a very complex workflow change. Plugins are unique to each organization and the logic contained within the Plugin can be modified to utilize any of the modules of the Canvas SDK. Plugins follow an event based architecture, which means that they can be thought of as working in the following way: whenever X event occurs, in Y situation, take Z action. Additional information about how to write a Plugin and load it to a Canvas instance can be found [here](/guides/your-first-plugin).

### What are the modules of the Canvas SDK that I can use in my Plugin?

Using these modules, a developer can utilize the Canvas SDK to build Plugins to simplify and package up the customizations to be deployed to a Canvas instance.

**The Seven Modules of the Canvas SDK**

| [Commands](/sdk/commands/) | The Commands module lets you define commands, which capture and display data and in some cases transmit orders or other external communications. Our built-in commands are included in this module and can be subclassed as a basis for custom commands, or the more primitive components of fields and handlers can be used to build a new command by subclassing the base command class, like all the built-in commands do. |
| [Data](/sdk/data)| The Data module provides you with data to compute on. It provides curated, secure access to both PHI (e.g. patient data) and non-PHI (e.g. staff and practice-level data), representing the current state of your target Canvas instance. The module's classes offer convenience methods and operators that make business logic and clinical logic easy to express with standard terminologies like ICD-10, SNOMED-CT, CPT, and the like. | 
| [Protocols](/sdk/protocols/)| The Protocols module lets you define workflows and workflow automations. Protocols may be clinical or operational in nature, and they may be very simple or very complex. They may encode well-established best practice guidelines, or they may be experimental. | 
| [Events](/sdk/events)| The Events module provides you with a set of event types to use as triggers for protocols. They are part of the "if" parameter in an "if this then that" expression (whereas the effects module is part of the "then" parameter). For now, defining custom events is discouraged and currently unsupported. | 
| [Effects](/sdk/effects/) | The Effects module allows you to cause effects on workflow that change user behavior or autonomously perform activities on behalf of users. Typically effects deliver either components or commands in some form. Effects are most often applied as the result of a protocol. They can also be applied other ways if necessary. Depending on the type of effect, applying it may represent a small workflow intervention, like annotating content or changing visual emphasis, or it may represent a significant consequence like ordering a test or fetching external data. | 
| [Views](/sdk/views/) | The Views module lets you specify data for display all around the Canvas application. The module provides classes representing all of the customizable UI components, which can be subclassed, customized, and applied using an effect. | 
| [Utils](/sdk/utils/) | The Utils Module provides access to common functions and capabilities to be used within other modules, and also some standalone tools that are useful to manage the plugin development lifecycle, namely testing and deployment. |

### What are some examples of Plugins?

Plugins can be utilized in many different ways. Here are some example use cases for Plugins.

- Modify the diagnose command such that conditions related to obstetric or pediatric diagnoses are filtered out
- Make an http request when a new patient record is created
- Insert new commands or questionnaires based upon the answers to one or more questions in a questionnaire
- Make a webhook call to request a patient’s contact and encounter information from a CRM application
- Annotate the diagnose command condition search results to add risk adjustment information
- Modify the refer command to populate providers from a different provider directory based upon the patient's geographic location and employer sponsored health benefits
- Change the default pharmacy based on patient insurance information for the prescribe command
- Move the immunizations section of the patient summary section of Canvas up when the patient is under the age of 13

### How do I get up and running with Plugins?

[This guide](/guides/your-first-plugin) will walk you through creating your first plugin.

### What is coming in future development of the Canvas SDK?

We are focused on continuing to unlock use cases for our customers. As we discover and understand new use cases, we will extend the functionality of the Canvas SDK. Currently under development is the expansion of the commands that can be utilized with the Canvas SDK, the event types available, the effects available, and building out the Data module. We will be keeping this documentation up to date with any changes in the capabilities of the Canvas SDK or you can find details in our [release notes](/product-updates/release-notes/) using the SDK tag. Feel free to send a request for new functionality or feedback on the Canvas SDK to product@canvasmedical.com.



