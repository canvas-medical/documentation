---
title: "Plugin Capabilities Overview"
---

Canvas plugins let you tailor your EHR to the way your organization practices medicine. Rather than working around a rigid system, plugins allow you to automate clinical workflows, customize the user interface, integrate with external systems, and optimize revenue cycle processes — all without modifying the core platform.

This page is a comprehensive map of what plugins can do, organized by the business problems they solve. For each capability, you'll find a link to the relevant technical documentation if you'd like to share it with your engineering team.

---

## Clinical Workflow Automation

Plugins can embed clinical intelligence directly into provider workflows, reducing manual steps and ensuring nothing falls through the cracks.

### Clinical Decision Support

Surface actionable recommendations at the point of care. Plugins can evaluate patient data in real time and present clinicians with relevant alerts, reminders, and suggested actions — directly within the chart.

- Display protocol cards with condition-specific recommendations, screening reminders, or care gap alerts
- Trigger recommendations based on patient demographics, diagnoses, lab results, medications, or any combination of clinical data
- Link recommendations to one-click actions so providers can act immediately

📄 *Technical reference: [Protocol Cards](/sdk/effect-protocol-cards/), [Events](/sdk/events/)*

### Charting Automation

Reduce documentation burden by auto-populating note content and streamlining common charting tasks.

- Auto-populate note sections (HPI, assessment, plan) from intake forms, previous visits, or external data
- Carry forward content from prior encounters for follow-up visits
- Create custom commands that insert structured content into notes with a single click
- Validate note content before signing to catch missing documentation

📄 *Technical reference: [Note Effects](/sdk/effect-notes/), [Commands](/sdk/commands/custom_command/), [Command Validation](/sdk/effect-command-validation/)*

### Quality Measures and Compliance

Automate quality measure tracking and surface compliance gaps proactively.

- Build screening protocols that remind providers when patients are due for assessments (e.g., tobacco screening, depression screening, fall risk)
- Track measure completion and surface outstanding items as protocol cards
- Automate documentation of quality measure interventions

📄 *Technical reference: [Protocol Cards](/sdk/effect-protocol-cards/), [Events](/sdk/events/)*

### Questionnaires and Assessments

Create structured data collection workflows with automated scoring and follow-up.

- Define questionnaires with conditional logic and branching
- Auto-score validated instruments (PHQ-9, GAD-7, STOP-BANG, etc.)
- Trigger follow-up actions based on assessment results
- Surface questionnaires within the patient portal for pre-visit completion

📄 *Technical reference: [Questionnaires](/sdk/questionnaires/), [Questionnaire Effects](/sdk/effect-questionnaires/), [Patient Portal Forms guide](/guides/patient-portal-forms/)*

---

## Revenue Cycle and Billing

Plugins can automate coding, streamline claim management, and reduce revenue leakage.

### Automated Coding

Reduce under-coding and coding errors by automatically suggesting or applying diagnosis and procedure codes.

- Auto-assign ICD-10 codes based on clinical data (e.g., BMI-based Z-codes)
- Surface HCC coding gaps from external data sources as actionable recommendations
- Annotate diagnoses with risk adjustment categories to support value-based care

📄 *Technical reference: [Billing Line Items](/sdk/effect-billing-line-items/), [Improve HCC Coding Accuracy guide](/guides/improve-hcc-coding-accuracy/)*

### Claim Management

Organize and streamline the claims workflow with automation.

- Apply labels to claims for categorization and queue management
- Automate claim status transitions and follow-up actions
- Post payments and reconcile billing data programmatically

📄 *Technical reference: [Claim Effects](/sdk/effect-claim/), [Claim Labels](/sdk/effect-appointment-labels/)*

### Billing Line Item Automation

Ensure accurate and complete billing by automating charge capture.

- Automatically add billing line items to notes based on services rendered
- Modify or remove line items based on business rules
- Assign CPT codes for time-based services (e.g., chronic care management)

📄 *Technical reference: [Billing Line Items](/sdk/effect-billing-line-items/)*

---

## Patient Engagement

Plugins can customize the patient-facing portal to improve engagement, streamline intake, and support self-service.

### Patient Portal Customization

Tailor the portal experience to your patient population and organizational workflows.

- Build custom landing pages with appointment scheduling, messaging, and health data widgets
- Add custom menu items and navigation to the portal
- Create fully custom portal applications for specialized workflows

📄 *Technical reference: [Patient Portal Effects](/sdk/effect-patient-portal/), [Custom Landing Page guide](/guides/custom-landing-page/)*

### Portal Forms and Questionnaires

Collect structured data from patients before, during, or after visits.

- Surface intake forms and questionnaires within the patient portal
- Enforce form completion before appointments
- Route form responses into the clinical record automatically

📄 *Technical reference: [Patient Portal Forms guide](/guides/patient-portal-forms/), [Questionnaires](/sdk/questionnaires/)*

### Messaging Enhancements

Extend patient-provider communication with automated messaging workflows.

- Send automated messages based on clinical events (appointment reminders, lab result notifications, follow-up instructions)
- Route incoming messages to appropriate staff or queues
- Integrate with external messaging platforms (SMS, email)

📄 *Technical reference: [Message Effects](/sdk/effect-message/), [Clients](/sdk/clients/)*

---

## User Interface Customization

Plugins can reshape the clinician and staff experience within Canvas to match your workflows.

### Chart Layout Configuration

Control what clinicians see and how information is organized within the patient chart.

- Show, hide, or reorder sections within the patient chart
- Group related items together for faster scanning
- Tailor chart layouts based on patient characteristics (e.g., pediatric vs. adult, behavioral health vs. primary care)

📄 *Technical reference: [Layout Effects](/sdk/effect-layout/), [Chart Group Effects](/sdk/effect-patient-chart-group/), [Tailoring the Chart guide](/guides/tailoring-the-chart-to-the-patient/)*

### Custom Applications

Embed rich, interactive applications directly within Canvas for specialized workflows.

- Build chart-level apps that display alongside the patient record
- Create note-level apps that support documentation workflows
- Add dashboard-level apps for population health views or operational dashboards

📄 *Technical reference: [Applications](/sdk/handlers-applications/), [Your First Application guide](/guides/your-first-application/)*

### Action Buttons and Modals

Add one-click actions for common workflows and surface contextual forms when needed.

- Add action buttons to the chart panel for quick operations
- Display modal dialogs for data entry or confirmation workflows
- Customize panel buttons across the application

📄 *Technical reference: [Action Buttons](/sdk/handlers-action-buttons/), [Customize Panel Buttons guide](/guides/customize-panel-buttons/)*

### Banner Alerts

Display important notifications directly within the patient chart with configurable severity levels.

- Show informational, warning, or critical alerts at the top of the chart
- Trigger alerts based on patient data (e.g., overdue screenings, drug interactions, care gaps)
- Include actionable links within alert banners

📄 *Technical reference: [Banner Alerts](/sdk/effect-banner-alerts/)*

### Data Visualization

Present clinical data in visual formats that support faster clinical decision-making.

- Display vitals trends and growth charts within the patient chart
- Build custom visualizations for any clinical data

📄 *Technical reference: [Visualizing Data guide](/guides/growth-charts/)*

---

## Integrations and Data Exchange

Plugins can connect Canvas to external systems, enabling bidirectional data flow and workflow automation.

### Custom HTTP APIs

Expose secure API endpoints from within Canvas for external systems to call.

- Build RESTful endpoints that external applications can call to read or write data
- Support authentication and authorization for secure integrations
- Enable real-time data exchange with third-party systems

📄 *Technical reference: [Simple API](/sdk/handlers-simple-api/)*

### Webhooks and Event-Driven Automation

React to events within Canvas and trigger actions in external systems.

- Listen for clinical events (new notes, lab results, appointment changes) and call external APIs
- Push data to external systems in real time as events occur
- Build complex multi-step workflows that span Canvas and external tools

📄 *Technical reference: [Events](/sdk/events/), [Creating Webhooks guide](/guides/creating-webhooks-with-the-canvas-sdk/)*

### Third-Party Service Integrations

Connect to popular platforms and services directly from plugin code.

- Send SMS messages via Twilio
- Send emails via SendGrid
- Store and retrieve files from AWS S3
- Call AI/LLM APIs for clinical decision support or documentation assistance
- Integrate with any HTTP-based external service

📄 *Technical reference: [Clients](/sdk/clients/)*

### FHIR API

Exchange clinical data using the healthcare industry-standard FHIR protocol.

- Read and write patient records, encounters, observations, and other clinical resources
- Integrate with health information exchanges and payer systems
- Support standard healthcare interoperability workflows

📄 *Technical reference: [FHIR API documentation](/api/)*

### External Event Ingestion

Receive and process events from external systems within Canvas.

- Ingest ADT (Admit/Discharge/Transfer) feeds from hospitals and facilities
- Process external lab results and clinical documents
- React to events from connected health devices or remote monitoring platforms

📄 *Technical reference: [External Events](/sdk/effect-external-events/)*

---

## Task and Workflow Management

Plugins can automate task creation, assignment, and lifecycle management to keep care teams organized.

### Automated Task Creation and Assignment

Create tasks automatically based on clinical events or business rules.

- Generate follow-up tasks when specific conditions are met (e.g., abnormal lab results, missed appointments)
- Assign tasks to specific team members or roles based on configurable rules
- Include relevant context and due dates with auto-created tasks

📄 *Technical reference: [Task Effects](/sdk/effect-tasks/), [Staying on Top of Tasks guide](/guides/staying-on-top-of-tasks/)*

### Task Lifecycle Management

Track and manage tasks through their complete lifecycle.

- Update task status, priority, and assignments programmatically
- Trigger actions when tasks are completed or overdue
- Build custom task workflows that match your operational processes

📄 *Technical reference: [Task Effects](/sdk/effect-tasks/), [Task Metadata](/sdk/effect-task-metadata/)*

---

## Scheduling and Appointments

Plugins can extend appointment workflows with custom data and integrations.

### Appointment Customization

Add custom fields, labels, and metadata to appointments.

- Attach custom data fields to appointment scheduling forms
- Apply labels for categorization and filtering
- Store and retrieve appointment-level metadata for reporting or integrations

📄 *Technical reference: [Appointment Labels](/sdk/effect-appointment-labels/), [Appointment Metadata](/sdk/effect-appointment-metadata/), [Appointment Scheduling Fields guide](/guides/appointments-additional_fields/)*

### Calendar Integration

Synchronize scheduling data with external calendar systems.

- Push appointment data to external calendars
- React to scheduling events to trigger preparation workflows

📄 *Technical reference: [Calendar Effects](/sdk/effect-calendar/)*

---

## What Plugins Cannot Do

Understanding the boundaries is just as important as knowing the capabilities.

| Boundary | Details |
|----------|---------|
| **Core UI framework** | Plugins cannot replace the Canvas application shell, navigation, or core UI components. Customization happens within designated extension points. |
| **Security and access controls** | Plugins operate within the platform's security model. They cannot bypass authentication, authorization, or audit logging. |
| **HIPAA compliance** | All plugin activity is subject to the same HIPAA compliance requirements as the core platform. Plugins cannot circumvent data protection policies. |
| **Database schema** | Plugins cannot modify the underlying database schema. They interact with data through well-defined APIs and data models. |
| **Other plugins** | Plugins are isolated from each other. One plugin cannot directly call or modify another plugin's behavior. |
| **Performance limits** | Plugin execution is sandboxed with resource limits to protect platform stability. Long-running or resource-intensive operations should be offloaded to external systems. |

---

## Next Steps

- **See real-world examples:** [Real-World Plugin Use Cases](/guides/plugin-use-cases/) shows how organizations use these capabilities to solve specific business problems.
- **Share with your engineering team:** Each section above links to the technical documentation they'll need to build the solution.
- **Explore the SDK:** The [Plugin SDK documentation](/sdk/) provides the complete technical reference.


<br/>
<br/>
<br/>