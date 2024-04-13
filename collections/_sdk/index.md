---
slug: /
title: "SDK Overview"
layout: sdklandingpage
---


## Care Modeling in Action
To help customers implement and iterate on their care model in Canvas, we created the Canvas SDK. Through the Canvas SDK, customers are able to customize and extend the capabilities of Canvas by control over the design of care delivery workflows and how they manifest within Canvas inclusive of how Canvas interacts with other systems through the Canvas FHIR API.

## Legacy SDK: The Canvas Workflow Kit

The Canvas Workflow Kit is a Software Development Kit (SDK) that makes it possible to extend the functionality of a Canvas instance. By providing a built-in command-line interface, skeleton code and test commands, developers can use the SDK to customize Protocols. The Canvas Workflow Kit's original purpose was to support clinical quality measures. Through  Protocols, customers are able to drive recommendations or changes to workflow based on various patient changes. Due to the original purpose of the Canvas Workflow Kit, recommending changes in workflow or creating additional interventions based on triggers or events beyond patient data is not possible. 

Documentation on the Canvas Workflow Kit can be found [here](/sdk/sdk-quickstart/).

## New: The Canvas SDK

The Canvas SDK allows for the development of plugins that listen for events
and respond with one or more effects on the system. Use plugins to make
recommendations, generate tasks, re-order or enrich search results, or even
create a co-pilot for charting.

A guide for developing your first plugin can be found [here](/guides/your-first-plugin).
