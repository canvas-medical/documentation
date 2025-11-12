---
title: "Lesson 1: Overview"
slug: "overview"
layout: education
hidden: true
---

Welcome to Canvas! The Canvas platform is a fully-featured, ONC certified Electronic Medical Record (EMR) that provides robust tools for customization and extension. For developers looking to integrate with or build custom logic within the EMR, the platform offers two main pathways: the **FHIR API** and the **Canvas SDK**.

While the FHIR API offers a standards-based **REST API** with 37 resources (21 of which are writable) for interoperability, the Canvas SDK enables developers to write custom **Python programs (plugins)** that execute synchronously within the EMR server container.

If your goal is to deeply customize the EMR’s behavior, implement clinical decision support, enforce business rules, or automate charting, the SDK is your primary tool.

In this overview, we will explore the three core concepts developers need to master to build effective plugins: **Events**, **Data**, and **Effects**, and we'll look at the specific **Handler** types used to implement your logic.

## The Plugin Runner: Your Custom Code in the EMR

The core of the SDK is the **plugin runner**, an open-source gRPC server that executes your Python code. Your logic is structured as a set of one or more **handlers**: classes that listen for declared **events** and perform a single responsibility via one or more **effects**.

Developing a plugin requires a mental model centered around three key concepts: **Events**, **Data**, and **Effects**.

## Events: The Entry Point for Execution

All plugin execution is **event-driven**, starting with an event emitted from the EMR. These events trigger your custom logic, allowing you to respond to nearly any action or state change within the system.

### Event Examples

- A patient was created.
- A user is about to view options in a form's select box.
- Dr. Smith started writing a prescription for Patient123.
- A specific button was clicked or a custom application was launched.
- A scheduled time was reached (e.g., "It is 7:05 pm").
- An external HTTP POST was received by a custom defined endpoint.

Events provide a direct link back to access their parent object, along with event specific context. In the case of a prescribe command, for example, the event target object tells you the specific command ID, and the context contains relevant fields (medication, indications, days supply, etc.), note ID, and patient ID. All of these can be used to filter to only the events you care about.

By responding to these events, developers can tailor the EMR's behavior to specific operational or clinical workflows.

## Data: Read-Only Access via Django ORM

Within your plugin, you need access to the EMR data. The SDK provides this access through a set of **read-only database views** using the **Django ORM**.

The use of the Django ORM is a significant developer advantage because **Django ORM objects offer a robust opportunity to filter and parse a given data model and any of its defined relationships.** This allows developers to write powerful and concise queries to fetch exactly the patient records, appointments, or clinical data they need for their custom logic.

### Why Read-Only Database Views?

This design choice is intentional to provide a **stable developer interface**. Canvas's internal database schemas may change over time, and the SDK view definitions can adapt accordingly. This shields your plugin code from breaking changes that would occur if you accessed tables directly.

If developers need access to data types that are not currently exposed, we encourage you to request them.

## Effects: Persisting Changes and Controlling the UI

While you have direct read access to the EMR's transactional database, writes are handled separately in the form of **Effects**.

Effects are typed payloads that essentially act as an **instruction set** for the EMR on how to persist data or modify the user's experience.

### Effect Examples and Corresponding Events

| **Triggering Event** | **Corresponding Effect(s)** |
| --- | --- |
| **A patient was created** | Create a task for staff to send a welcome packet. |
| **User views a select box** | Present filtered, reordered, and annotated options instead of the default. |
| **Dr. Smith started a prescription** | Pre-fill the prescription details based on a structured form or patient data. |
| **A custom application was launched** | Launch a specific modal or pre-fill chart notes based on a template. |
| **It is 7:05 pm (Cron)** | Rebalance task assignment for overdue tasks. |
| **Received an HTTP POST to `<path>`** | Return a custom JSON response with a specific payload and status code. |

The platform aims to give plugins the same capabilities as end-users, with the key exception being regulatory limitations. For example, a plugin can automate the filling out of a prescription, but a prescriber must still manually sign off on it—the final click of approval must come from a human.

## Implementing Your Logic: Types of Handlers

Your plugin is built around **handlers**, which are the specific units of code you provide. They may listen for events by declaring them directly or by inheriting from a specific handler subclass.

Key Handler Types to Know:

- **`BaseHandler`**: The most fundamental type. You declare the events it listens for in the `RESPONDS_TO` constant and implement the `compute` method to return a list of effects.
- **`CronTask`**: Designed for scheduled automation. You set the cron string in the `SCHEDULE` constant and implement the `execute` method.
- **`ActionButton`**: Allows you to customize the EMR user interface. You set the button label and location and implement the `handle` method. An optional `visible` method can be implemented to make the button appear only under certain conditions.
- **`SimpleAPI`**: For custom HTTP interactions. You implement an `authenticate` method and a method for each request path, annotated with the path and verb (e.g., GET, POST), resulting in a custom endpoint IN YOUR CANVAS INSTANCE…!
- **`Application`**: Used to embed custom user interfaces or launch modals within the EMR. You provide an icon and title, and implement the `on_open` method.

For example, an ActionButton in the patient charting menu, when launched, makes a GET call to a SimpleAPI endpoint that renders some custom HTML content in a sidebar. The [Vitals Visualizer Plugin](https://docs.canvasmedical.com/sdk/example-vitals_visualizer_plugin/) showcases a composition of handlers that allow you to display custom UIs in response to a user initiated event.

A single plugin can contain multiple handlers, and group handlers of similar functionality together. For example, [Patient Summary Chart Groups](https://docs.canvasmedical.com/sdk/example-patient_summary_chart_groups/) iterates on and organizes patient conditions and also medications.

These handlers allow you to build everything from small quality-of-life agentic automations (like [AI note titles](/sdk/example-ai_note_titles/)) to more complex integrations ([Syncing patients between systems](/sdk/example-patient_creation_platform_sync/)), or even full web applications ([Example Chart Application](/sdk/example-example_chart_app/)).

## Summary

In this overview, you learned about:

- The two primary ways to interact with the Canvas EMR programmatically: The **FHIR API** for general interoperability and the **Canvas SD**K** for deep system customization.
- The SDK's **plugin runner**, an open-source gRPC server that executes your custom logic.
- The three foundational concepts for building plugins: **Events** (the trigger), **Data** (read-only access via Django ORM views), and **Effects** (typed payloads used to persist changes and control the UI).
- The specific **Handler** classes you can use to implement different kinds of logic, including `BaseHandler`, `CronTask`, and `SimpleAPI`.

---

## Next Steps
[Next: let's set up your developer environment](/learn/setup)!


