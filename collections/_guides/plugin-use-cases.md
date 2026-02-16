---
title: "Real-World Plugin Use Cases"
---

This page showcases how organizations use Canvas plugins to solve real business problems. Each use case describes a common challenge, how plugins address it, and the business impact you can expect. Use these examples as inspiration when scoping new projects or evaluating whether Canvas can meet a specific need.

For a complete map of plugin capabilities, see the [Plugin Capabilities Overview](/guides/plugin-capabilities-overview/).

---

## Chronic Care Management

### Automated CCM Activity Tracking and Billing

**The problem:** Chronic care management (CCM) programs require meticulous time tracking for billable activities. Manual tracking is error-prone, leads to missed billing opportunities, and creates administrative burden for care teams.

**How plugins solve it:**
- A timer-based plugin tracks time spent on CCM activities automatically as staff interact with patient records
- When monthly time thresholds are reached, the plugin assigns the appropriate CPT codes (99490, 99491, etc.) and adds billing line items to the patient's record
- Monthly CCM notes are generated automatically, summarizing activities performed and time spent

**Business impact:** Reduced revenue leakage from missed billing, lower administrative overhead, and more accurate documentation for audit compliance.

📄 *Technical reference: [Billing Line Items](/sdk/effect-billing-line-items/), [Cron Tasks](/sdk/handlers-crontask/)*

---

## Clinical Screening and Risk Assessment

### Tobacco Use Screening Protocol

**The problem:** Quality measure compliance (e.g., CMS138v14) requires systematic screening of all eligible patients, but it's easy for screenings to fall through the cracks during busy visits.

**How plugins solve it:**
- A protocol evaluates each patient's record to determine screening eligibility and status
- When a patient is due for screening, a recommendation card appears at the top of their chart
- Clinicians can act on the recommendation with one click, documenting the screening and any interventions
- The protocol automatically resolves once screening is completed

**Business impact:** Higher quality measure scores, reduced compliance risk, and less manual tracking by quality teams.

📄 *Technical reference: [Protocol Cards](/sdk/effect-protocol-cards/), [Events](/sdk/events/)*

### Sleep Apnea Risk Scoring (STOP-BANG)

**The problem:** Sleep apnea is significantly underdiagnosed. Providers may not consistently apply validated screening tools during routine visits.

**How plugins solve it:**
- A questionnaire plugin administers the STOP-BANG assessment within the patient portal or during the visit
- Responses are automatically scored and the risk level is documented in the patient record
- High-risk results trigger a protocol card recommending next steps (sleep study referral, follow-up appointment)

**Business impact:** Earlier identification of at-risk patients, improved care quality, and potential revenue from follow-up diagnostic services.

📄 *Technical reference: [Questionnaires](/sdk/questionnaires/), [Protocol Cards](/sdk/effect-protocol-cards/)*

### Mental Health Screening Automation

**The problem:** Depression (PHQ-9) and anxiety (GAD-7) screenings need to be administered at specific intervals, scored accurately, and followed up on — all of which are easy to miss in high-volume practices.

**How plugins solve it:**
- Questionnaires are surfaced in the patient portal before visits or presented during check-in
- Scores are calculated automatically and documented as structured observations
- Score trends are visible in the chart, helping providers track progress over time
- Critical scores trigger immediate alerts and recommended interventions

**Business impact:** Better outcomes tracking, improved compliance with behavioral health quality measures, and earlier intervention for patients in crisis.

📄 *Technical reference: [Questionnaires](/sdk/questionnaires/), [Banner Alerts](/sdk/effect-banner-alerts/), [Patient Portal Forms guide](/guides/patient-portal-forms/)*

---

## Revenue Optimization

### Automated BMI Coding with Z-Codes

**The problem:** BMI-related Z-codes (Z68.x) are frequently missed during documentation, resulting in under-coding and lost revenue — especially in value-based care models.

**How plugins solve it:**
- When a BMI observation is recorded, a plugin automatically calculates the appropriate Z-code based on the BMI value and patient age
- The Z-code is added to the encounter's billing line items without any additional provider action
- Existing diagnoses are cross-referenced to avoid duplicate coding

**Business impact:** Increased per-encounter revenue capture, more accurate risk adjustment scores, and zero additional documentation burden on providers.

📄 *Technical reference: [Billing Line Items](/sdk/effect-billing-line-items/), [Events](/sdk/events/)*

### AI-Powered Claim Coding Assistance

**The problem:** Manual coding review is time-consuming and subject to human error. Under-coding leaves revenue on the table; over-coding creates compliance risk.

**How plugins solve it:**
- A plugin analyzes note content using an AI service and suggests appropriate diagnosis and procedure codes
- Suggestions are presented as protocol cards that coders can accept, modify, or dismiss
- Coding patterns are tracked over time to identify systematic gaps

**Business impact:** Faster coding turnaround, reduced denial rates, and improved coding accuracy across the organization.

📄 *Technical reference: [Protocol Cards](/sdk/effect-protocol-cards/), [Clients](/sdk/clients/), [Simple API](/sdk/handlers-simple-api/)*

### HCC Coding Gap Closure

**The problem:** In Medicare Advantage and other risk-adjusted payment models, unaddressed coding gaps directly reduce reimbursement. Gaps often come from external sources (health plan data, prior claims) and need to be validated and addressed by clinicians.

**How plugins solve it:**
- Coding gaps from external sources are ingested via the FHIR API and stored as detected issues
- A protocol surfaces unreviewed gaps as cards in the patient chart for clinical validation
- Once validated, gaps are presented to providers with one-click commands to add the diagnosis and close the gap
- Resolved gaps are tracked for reporting and audit purposes

**Business impact:** Maximized risk adjustment revenue, streamlined CDI workflows, and comprehensive audit trails.

📄 *Technical reference: [Improve HCC Coding Accuracy guide](/guides/improve-hcc-coding-accuracy/)*

---

## Telehealth and Virtual Care

### Auto-Populated HPI from Intake Forms

**The problem:** Telehealth visits often start with providers re-asking questions that patients already answered on intake forms, wasting valuable visit time and frustrating patients.

**How plugins solve it:**
- Patients complete a structured intake questionnaire in the portal before their visit
- When the provider opens the note, relevant intake responses are automatically populated into the HPI section
- Providers can review and edit the pre-populated content rather than starting from scratch

**Business impact:** Shorter visit times, higher patient satisfaction, and more visits per provider per day.

📄 *Technical reference: [Note Effects](/sdk/effect-notes/), [Questionnaires](/sdk/questionnaires/), [Patient Portal Forms guide](/guides/patient-portal-forms/)*

### Carry-Forward Notes for Follow-Up Visits

**The problem:** Follow-up visits for chronic conditions often require reviewing and updating the same information. Providers waste time re-documenting stable findings.

**How plugins solve it:**
- A custom command copies relevant sections from the most recent prior note into the current encounter
- Carried-forward content is clearly marked so providers know what to review and update
- Only clinically relevant sections are carried forward based on visit type and diagnoses

**Business impact:** Reduced documentation time per visit, more consistent longitudinal records, and less provider burnout.

📄 *Technical reference: [Commands](/sdk/commands/custom_command/), [Note Effects](/sdk/effect-notes/)*

---

## Patient Portal Enhancement

### Custom Landing Page with Self-Service Widgets

**The problem:** The default portal experience may not highlight the actions most important to your patient population, leading to low engagement and increased call volume for routine tasks.

**How plugins solve it:**
- A custom landing page displays the most relevant widgets for your patients: upcoming appointments, unread messages, recent lab results, and outstanding forms
- The layout and content adapt based on patient characteristics (e.g., new patient vs. established, chronic condition panels)
- Direct action buttons let patients schedule, message, or complete forms without navigating through menus

**Business impact:** Higher portal adoption rates, reduced call volume, and better patient preparation for visits.

📄 *Technical reference: [Patient Portal Effects](/sdk/effect-patient-portal/), [Custom Landing Page guide](/guides/custom-landing-page/)*

### Intake Form Enforcement Before Visits

**The problem:** Incomplete intake data leads to longer visits, missing information for billing, and gaps in the clinical record.

**How plugins solve it:**
- Required questionnaires are assigned to patients when appointments are scheduled
- The portal prominently displays outstanding forms and sends reminders
- Form completion status is visible to staff in the scheduling view, enabling proactive outreach for incomplete forms

**Business impact:** More complete data at the start of each visit, shorter check-in times, and fewer billing issues from missing information.

📄 *Technical reference: [Patient Portal Forms guide](/guides/patient-portal-forms/), [Questionnaires](/sdk/questionnaires/)*

---

## External System Integration

### Single Sign-On with Auto-Patient Creation

**The problem:** Organizations using external identity providers need seamless access to Canvas without manual account provisioning, and patient records should be created automatically when new patients authenticate.

**How plugins solve it:**
- A plugin exposes an API endpoint that receives SAML assertions from the identity provider
- On successful authentication, the plugin checks for an existing patient record and creates one if needed
- The patient is redirected to their portal with a valid session, with no manual registration required

**Business impact:** Frictionless patient onboarding, reduced IT support burden, and seamless integration with existing identity infrastructure.

📄 *Technical reference: [Simple API](/sdk/handlers-simple-api/), [Patient Effects](/sdk/effect-patient/)*

### Calendar Sync with External Scheduling Systems

**The problem:** Organizations using external scheduling tools (cal.com, third-party schedulers) need appointment data synchronized with Canvas in real time.

**How plugins solve it:**
- Webhooks from the external scheduling system call a plugin API endpoint when appointments are booked, modified, or canceled
- The plugin creates or updates the corresponding Canvas appointment, including patient matching and provider assignment
- Confirmation data is sent back to the external system to close the loop

**Business impact:** Single source of truth for scheduling, no double-booking, and reduced manual data entry.

📄 *Technical reference: [Simple API](/sdk/handlers-simple-api/), [Calendar Effects](/sdk/effect-calendar/)*

### Webhook-Based Data Synchronization

**The problem:** Data lives in multiple systems (CRM, care management platforms, analytics tools) and keeping it in sync requires manual exports or fragile batch processes.

**How plugins solve it:**
- Plugins listen for relevant Canvas events (new patients, note completions, lab results) and push data to external systems via API calls
- Incoming webhooks from external systems trigger plugins that update Canvas records
- Bidirectional sync keeps all systems current without manual intervention

**Business impact:** Eliminated data silos, real-time data availability across systems, and reduced manual reconciliation effort.

📄 *Technical reference: [Creating Webhooks guide](/guides/creating-webhooks-with-the-canvas-sdk/), [Events](/sdk/events/), [Clients](/sdk/clients/)*

---

## Lab and Diagnostic Workflows

### Automated Task Creation for Fasting Labs

**The problem:** When a provider orders fasting labs, someone needs to ensure the patient is contacted with instructions and that the lab is completed within the appropriate window. This follow-up is often manual and inconsistent.

**How plugins solve it:**
- When a fasting lab is ordered, a plugin automatically creates a task assigned to the appropriate staff member
- The task includes patient contact information, lab instructions, and a due date
- If the task isn't completed within the specified window, an escalation task is created

**Business impact:** Fewer missed labs, better patient compliance with ordered tests, and less manual coordination by nursing staff.

📄 *Technical reference: [Task Effects](/sdk/effect-tasks/), [Events](/sdk/events/), [Staying on Top of Tasks guide](/guides/staying-on-top-of-tasks/)*

### Abnormal Lab Result Notifications

**The problem:** Critical or abnormal lab results require timely provider review, but results can sit unnoticed in a busy inbox.

**How plugins solve it:**
- A plugin monitors incoming lab results and evaluates them against configurable thresholds
- Abnormal results trigger immediate banner alerts in the patient's chart and create urgent tasks for the ordering provider
- Critical values can also trigger automated outreach to the patient

**Business impact:** Faster response to critical results, reduced liability risk, and better patient safety.

📄 *Technical reference: [Banner Alerts](/sdk/effect-banner-alerts/), [Task Effects](/sdk/effect-tasks/), [Events](/sdk/events/)*

---

## Provider Efficiency

### One-Click Note Templates from Previous Visits

**The problem:** Providers seeing patients for recurring issues spend significant time recreating similar notes from scratch each visit.

**How plugins solve it:**
- A custom command is available within the note editor that pulls structured content from the most recent relevant visit
- The template pre-fills common sections while highlighting areas that need updating
- Different templates can be configured for different visit types or specialties

**Business impact:** Reduced documentation time, more consistent notes, and more time for patient interaction.

📄 *Technical reference: [Commands](/sdk/commands/custom_command/), [Note Effects](/sdk/effect-notes/)*

### Vitals Trend Visualization

**The problem:** Reviewing vitals trends over time requires clicking through multiple encounters. Providers need a quick visual summary to spot trends and make decisions.

**How plugins solve it:**
- A chart-level application displays vitals data as interactive trend lines directly within the patient chart
- Providers can quickly see blood pressure trends, weight changes, or growth patterns without leaving the chart
- Abnormal trends are highlighted visually for quick identification

**Business impact:** Faster clinical decision-making, better chronic condition monitoring, and improved patient conversations about health trends.

📄 *Technical reference: [Visualizing Data guide](/guides/growth-charts/), [Applications](/sdk/handlers-applications/)*

### Custom Action Buttons for Common Workflows

**The problem:** Frequent tasks like ordering a standard lab panel, sending a patient education packet, or creating a referral require multiple clicks through menus and forms.

**How plugins solve it:**
- Action buttons are added to the chart panel for the most common workflows
- A single click triggers a multi-step process: creating orders, sending messages, updating records, or calling external services
- Buttons can be shown or hidden based on patient context (e.g., only show diabetes-related actions for diabetic patients)

**Business impact:** Fewer clicks per common task, more standardized workflows, and less time spent navigating the application.

📄 *Technical reference: [Action Buttons](/sdk/handlers-action-buttons/), [Customize Panel Buttons guide](/guides/customize-panel-buttons/)*

---

## From Idea to Plugin

Turning a business need into a working plugin follows a straightforward path:

| Step | Who | What happens |
|------|-----|-------------|
| **1. Define the need** | Product / Operations | Describe the workflow problem and desired outcome. Use this page and the [Capabilities Overview](/guides/plugin-capabilities-overview/) to identify which capabilities apply. |
| **2. Spec the solution** | Product + Engineering | Map the business requirements to specific plugin capabilities. Identify which events to listen for, what data to display, and what actions to automate. |
| **3. Build and test** | Engineering | Develop the plugin using the [Canvas SDK](/sdk/), test locally, and validate against acceptance criteria. |
| **4. Deploy** | Engineering | Install the plugin on your Canvas instance using the [Canvas CLI](/sdk/canvas_cli/). Plugins can be deployed to staging first for validation. |
| **5. Monitor and iterate** | Product + Engineering | Review [plugin logs](/sdk/plugin-logs/) to monitor behavior, gather user feedback, and iterate on the solution. |

For a hands-on walkthrough of building your first plugin, share the [Your First Plugin guide](/guides/your-first-plugin/) with your engineering team.


<br/>
<br/>
<br/>