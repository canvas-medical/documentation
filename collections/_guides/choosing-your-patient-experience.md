---
title: "Choosing Your Patient Experience"
guide_for:
- /sdk/patient-portal/
- /sdk/handlers-applications/
- /api/
---

The first decision when building a patient-facing experience on Canvas isn't technical — it's about **how much of that experience you want to own**. Canvas gives you a spectrum: turn on our built-in patient portal as-is, extend it with plugins, or build your own patient app entirely and use Canvas as the clinical backend. This guide helps you pick the path that fits your product, team, and timeline — and points you to the how-to docs once you've decided.

{% include alert.html type="info" content="There's no wrong door, and you're not locked in. Most teams start with the built-in portal and add custom pieces over time — the paths below are complementary, not one-way." %}

## The three paths

| | **Use the built-in portal** | **Extend the built-in portal** | **Build your own** |
|---|---|---|---|
| **Who builds the UI** | Canvas | Canvas + your plugins | You |
| **Effort** | Lowest | Medium | Highest |
| **Control over look & flow** | Configuration | Configure, plus inject widgets, applications, and logic | Total |
| **Patient data** | Handled for you | Handled for built-in pages; you supply data to your own widgets & applications (Canvas data module, Custom Data, or external sources) | You read & write it via Canvas APIs |
| **Best when** | You want a working, compliant portal fast | The built-in portal is close, but you need extra pages, branding, or custom rules | You have (or want) your own branded app and use Canvas as the source of truth |

## How to choose

<div style="text-align: center; margin: 1.5rem 0;">
<svg viewBox="0 0 760 520" role="img" aria-labelledby="pe-flow-title pe-flow-desc" style="width: 100%; max-width: 720px; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <title id="pe-flow-title">Choosing a patient experience</title>
  <desc id="pe-flow-desc">If you want complete control of the experience with Canvas never exposed to patients, build your own (Path 3). Otherwise, if the built-in portal is enough as-is, use it (Path 1); if it needs a few custom touches, extend it with plugins (Path 2).</desc>
  <defs>
    <marker id="pe-arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#475569"/>
    </marker>
  </defs>
  <g stroke="#475569" stroke-width="1.5" fill="none">
    <line x1="380" y1="74" x2="380" y2="102" marker-end="url(#pe-arrow)"/>
    <line x1="470" y1="152" x2="536" y2="152" marker-end="url(#pe-arrow)"/>
    <line x1="380" y1="200" x2="380" y2="258" marker-end="url(#pe-arrow)"/>
    <line x1="470" y1="308" x2="536" y2="308" marker-end="url(#pe-arrow)"/>
    <line x1="380" y1="356" x2="380" y2="420" marker-end="url(#pe-arrow)"/>
  </g>
  <g font-size="12" fill="#475569">
    <text x="512" y="145" text-anchor="middle">Yes</text>
    <text x="392" y="232">No</text>
    <text x="512" y="301" text-anchor="middle">Yes</text>
    <text x="392" y="396">No</text>
  </g>
  <rect x="250" y="30" width="260" height="44" rx="22" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="380" y="57" text-anchor="middle" font-size="13" fill="#0f172a">Designing your patient experience</text>
  <polygon points="380,104 470,152 380,200 290,152" fill="#fef3c7" stroke="#fcd34d"/>
  <text x="380" y="148" text-anchor="middle" font-size="12.5" fill="#92400e">Complete control,</text>
  <text x="380" y="164" text-anchor="middle" font-size="12.5" fill="#92400e">Canvas not exposed?</text>
  <rect x="540" y="116" width="216" height="74" rx="8" fill="#ede9fe" stroke="#c4b5fd"/>
  <text x="648" y="140" text-anchor="middle" font-size="13" fill="#5b21b6" font-weight="600">Build your own app · Path 3</text>
  <text x="648" y="158" text-anchor="middle" font-size="11" fill="#6d28d9">highest effort · full build</text>
  <text x="648" y="174" text-anchor="middle" font-size="11" fill="#6d28d9">you have or will build an app</text>
  <polygon points="380,260 470,308 380,356 290,308" fill="#fef3c7" stroke="#fcd34d"/>
  <text x="380" y="304" text-anchor="middle" font-size="12.5" fill="#92400e">Built-in portal</text>
  <text x="380" y="320" text-anchor="middle" font-size="12.5" fill="#92400e">enough as-is?</text>
  <rect x="540" y="271" width="216" height="74" rx="8" fill="#dcfce7" stroke="#86efac"/>
  <text x="648" y="295" text-anchor="middle" font-size="13" fill="#166534" font-weight="600">Use the built-in portal · Path 1</text>
  <text x="648" y="313" text-anchor="middle" font-size="11" fill="#15803d">lowest effort</text>
  <text x="648" y="329" text-anchor="middle" font-size="11" fill="#15803d">fastest to launch</text>
  <rect x="272" y="424" width="216" height="74" rx="8" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="380" y="448" text-anchor="middle" font-size="13" fill="#1e40af" font-weight="600">Extend with plugins · Path 2</text>
  <text x="380" y="466" text-anchor="middle" font-size="11" fill="#1d4ed8">medium effort</text>
  <text x="380" y="482" text-anchor="middle" font-size="11" fill="#1d4ed8">portal's close — add a few things</text>
</svg>
</div>

---

## Path 1 — What's already built into Canvas

When you sign with Canvas, you already have a full patient portal — no build, no plugins, nothing to stand up. Patients can log in (with their email, phone number, or username, plus a password) and use it from day one, and Canvas hosts it and handles the login, data, and compliance for you.

Out of the box it includes **messaging, payments, labs, and a contact page**. Other pages — **scheduling, My Health, health records, consents, and self-registration** — are built in too and ready to switch on whenever you want them.

Everything in this path is **configuration only — no plugins or code**. You decide which built-in pages appear and set basic branding; that's the whole effort.

### Built-in pages you can turn on or off

Each page is toggled with a **Constance** setting, managed by Canvas Support — so [contact Support](https://canvas-medical.help.usepylon.com/) to change them. For a full walkthrough, see [Managing the Patient Portal](https://canvas-medical.help.usepylon.com/articles/7348270931-managing-the-patient-portal).

| Setting | Page | What patients can do | Default |
|---|---|---|---|
| `PATIENT_APP_MESSAGING` | Messaging | Securely message their care team | `True` |
| `PATIENT_APP_PAYMENTS` | Payment | View and pay outstanding balances | `True` |
| `PATIENT_APP_LABS` | Lab | View their lab results | `True` |
| `PATIENT_APP_CONTACT` | Contact | See the practice's contact information | `True` |
| `PATIENT_APP_MY_HEALTH` | My Health | Review conditions, medications, allergies, and related clinical info | `False` |
| `PATIENT_APP_RECORDS` | Health Records | Access and download their health records | `False` |
| `PATIENT_APP_APPOINTMENTS` | Scheduling flow | Book and view appointments | `False` |
| `PATIENT_APP_CONSENTS` | Consents | Review and complete consents | `False` |
| `PATIENT_APP_REGISTER` | Register | Self-register from the login page | `False` |

**Other portal settings:**

| Setting | Controls | Default |
|---|---|---|
| `ENABLE_PATIENT_PORTAL` | Whole portal on/off | `True` |
| `ALLOW_PATIENT_DOCUMENT_UPLOADS` | Patient document uploads on "My Health" | `False` |
| `PATIENT_APP_USERS_EMAIL_ONLY` | Email-only login (access mode, not a page) | `False` |
| `PATIENT_APP_BANNER` | Banner text on the portal login page | `""` |

{% include alert.html type="warning" content="Defaults are mixed, not all-off. Messaging, Payments, Labs, and Contact are on out of the box; My Health, Health Records, Appointments, Consents, and Register are off. So you typically turn off the stock pages you don't want and turn on the ones you do — rather than enabling everything from scratch." %}

### Branding

You can put your organization's identity on the portal without building anything:

- **Logo** — your organization's logo is shown on the login page and throughout the portal. It's configured on your Canvas organization; until you provide one, the default Canvas logo appears. Work with Canvas to set it.
- **Banner message** — `PATIENT_APP_BANNER` sets a short greeting above the login card.
- **Email sender for patient messages** — message and notification emails to patients are sent with **your organization's name** as the sender, from the address in your organization's `defaultEmail` setting (default `do-not-reply@canvasmedical.com`). You can change that address; using your own domain may require sender authentication set up with Canvas.

What stays **Canvas-driven** and isn't branded per organization:

- **The portal URL** — patients sign in at `https://<your-instance>.canvasmedical.com/app`.
- **The login flow** — the sign-in and verification screens are Canvas's.
- **Sign-in & verification emails** — these are sent from a fixed `no-reply@canvasmedical.com` (a separate path from the patient-message sender above), so they can't be rebranded.

{% include alert.html type="info" content="Want your own domain and login flow end to end? That's Path 3 — build your own app and use Canvas as the backend." %}

---

## Path 2 — Extend the built-in portal with plugins

The built-in portal is a strong starting point — but it's rarely *exactly* what you want. Path 2 is where you make it feel like **yours**: add the cards, pages, and rules your patients and workflows actually need, while Canvas keeps hosting the portal and handling login, data, and compliance. You never stand up your own app.

Under the hood, every extension is a plugin that **reacts to a portal event and returns an effect**. As patients move through the portal, your handler can add a widget, render a page, filter appointment slots, and so on.

New to plugins? Start with [Your First Plugin](/guides/your-first-plugin-with-claude-code/), then keep the [Patient Portal config hub](/sdk/patient-portal/) and the [portal events](/sdk/events/) handy. And for inspiration, the community-run [Medical Software Foundation library](https://github.com/medical-software-foundation/canvas) has production-ready portal extensions you can install or learn from — several are linked below.

Here's what you can do — mix and match as many as you like.

### Personalize the landing page with widgets

The portal home is the first thing patients see after logging in, and it's the easiest place to add value. **Widgets** are cards you render there: a "your next appointment" summary, an outstanding-balance nudge, a care-gap reminder ("you're due for a flu shot"), links to your own resources — anything you can compute for that patient.

You control what each card shows, pulling from the Canvas data module, your plugin's Custom Data, or an external service.

See [Portal Landing Page Widgets](/sdk/patient-portal/#portal-landing-page-widgets) and the [Custom Landing Page guide](/guides/custom-landing-page/) for the exact documentation on how to build them. And you don't have to start from a blank file — there's a ready-made [patient_portal_plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_plugin) in our open-source examples repo you can install as-is or use as a reference and starting point.

### Shape self-scheduling

Self-scheduling is powerful, but you'll usually want guardrails. Filter or reorder the slots a patient can book *before they see them* — keep new patients on longer visit types, hide same-day slots, steer certain reasons to specific providers, or enforce your booking policies.

See [Shape Self-Scheduling](/sdk/patient-portal/#shape-self-scheduling) · SDK example: [patient_portal_search_appointments_slots_plugin](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_portal_search_appointments_slots_plugin).

Real-world example (MSF):

- [urgent-care-self-scheduler](https://github.com/medical-software-foundation/canvas/tree/main/extensions/urgent-care-self-scheduler) — adds a "Need to be seen today?" portal card and a full self-booking flow that offers only credentialed providers, blocks duplicate bookings, and pre-populates the visit note. A good end-to-end model.

### Tailor appointment cards

Fine-tune the actions on each appointment. Hide **Cancel** or **Reschedule** when your policy says so (for example, no reschedule within 24 hours of the visit), or add a **telehealth join link** to virtual appointments — decided per appointment.

See [Customize Appointment Cards](/sdk/patient-portal/#customize-appointment-cards).

Real-world example (MSF):

- [portal_disable_cancel_appts](https://github.com/medical-software-foundation/canvas/tree/main/extensions/portal_disable_cancel_appts) — answers the "can this appointment be canceled?" check with *no*, removing the self-service Cancel action so cancellations route through staff.

### Surface forms and react to responses

Meet patients with the right questionnaire at the right moment — an intake packet before a first visit, a PHQ-9 for a behavioral-health appointment, a post-visit survey — and act on what they submit. Forms are surfaced to the patient when they log in to the portal: you choose which ones appear, then react to responses to store the answers or trigger follow-up. Responses are saved as Interviews, and you can even generate a Questionnaire command in the patient's note.

See the [Patient Portal effects → Forms](/sdk/patient-portal/#forms) for the technical reference.

### Automate login and activation

Getting patients into the portal doesn't have to be manual. Automatically **invite** patients to activate their account when they're ready — for example, once you've confirmed a good email or phone — instead of having staff send invitations one at a time. You can also keep a patient's portal **login in sync** when their email or phone changes, and **verify** a contact point before you rely on it to invite them or send messages.

See [User Login](/sdk/patient-portal/#user-login) for automating invitations and keeping the login in sync, and [Send Contact Verification](/sdk/effect-send-contact-verification/) for confirming a contact point first.

### Control the navigation layout

Decide which items appear in the portal navigation and in what order — and do it **conditionally per patient**. Surface a page only to patients in a certain program, reorder the menu so what matters most comes first, or hide built-in items you don't use. The navigation isn't fixed; you compute it for each patient every time the portal loads.

See [Configure Portal Menu Items](/sdk/patient-portal/#configure-portal-menu-items).

### Add your own pages

Need more than a card? Add entire patient-facing **pages** with an Application scoped to the patient portal — a program dashboard, an intake wizard, a financial-assistance flow, an education library. The page lives inside the portal (same URL, same login, same navigation), but its UI and logic are entirely yours.

This is also how you **replace a built-in page you don't love**. Don't like how the stock My Health page presents conditions, medications, and allergies? Build your own version exactly the way you want it, then turn off the built-in page with its Path 1 toggle (`PATIENT_APP_MY_HEALTH`) so patients only ever see yours. The same works for any built-in section — keep the stock pages that suit you and swap out the ones that don't, one at a time.

See the [Applications handler](/sdk/handlers-applications/) and [Configure Portal Menu Items](/sdk/patient-portal/#configure-portal-menu-items) for surfacing your page in the portal navigation · SDK examples: [example_patient_portal_page](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_patient_portal_page), [patient_app_schedule](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/patient_app_schedule).

Real-world examples (MSF):

- [patient-portal-profile](https://github.com/medical-software-foundation/canvas/tree/main/extensions/patient-portal-profile) — adds a read-only **My Profile** page (demographics, care team, preferred pharmacy).
- [portal-content](https://github.com/medical-software-foundation/canvas/tree/main/extensions/portal-content) — builds richer **My Records** and **My Profile** pages (visit notes, labs, imaging, letters, insurance) with optional review-gating. A great model for replacing the stock pages with your own.
- [patient-portal-forms](https://github.com/medical-software-foundation/canvas/tree/main/extensions/patient-portal-forms) — ships a whole forms experience as its own portal page: staff assign questionnaires (PHQ-9, GAD-7, ROS…) that patients complete in the portal, with responses posting back to the chart.

### Missing something? Ask before you rebuild

Customizing the portal puts you in the best position to see what's missing. If you hit something plugins can't do in the portal yet, requesting a **new SDK capability** is often a better move than jumping to building your own (Path 3) — it can unlock what you need *inside* the built-in portal, so you keep everything Canvas handles for you (login, data, compliance) instead of rebuilding it. Many of today's patient-portal capabilities exist because customers asked for them.

{% include alert.html type="info" content="Hitting the edge of what plugins can do in the portal? Tell your Canvas contact or Support what you're trying to build. A new SDK capability may unlock it inside the portal — and your request helps shape what we build next for everyone." %}

---

## Path 3 — Build your own patient app on Canvas data

If you want a fully branded app — your own UI, your own login — build it as an external application and use Canvas as the clinical source of truth. You move data between your app and Canvas in three **complementary** ways; most portals use a combination, because each fits a different job and has its own authentication model.

- **[FHIR API](/api/)** and **[SimpleAPI](/sdk/handlers-simple-api-http/)** are calls *from your app into Canvas* — **Canvas authenticates you**.
- **[Events → webhooks](/sdk/events/)** are calls *from Canvas out to your app* — **you authenticate Canvas**.

<div style="text-align: center; margin: 1.5rem 0;">
<svg viewBox="0 0 760 440" role="img" aria-labelledby="pe-arch-title pe-arch-desc" style="width: 100%; max-width: 720px; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <title id="pe-arch-title">How a customer-owned portal talks to Canvas</title>
  <desc id="pe-arch-desc">Your app calls into Canvas via the FHIR API (OAuth2) and SimpleAPI (API key) to read and write data; Canvas calls out to your app via event-driven webhooks, which your app authenticates with a shared secret.</desc>
  <defs>
    <marker id="pe-a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#475569"/>
    </marker>
  </defs>
  <!-- boxes -->
  <rect x="40" y="110" width="190" height="240" rx="10" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="135" y="222" text-anchor="middle" font-size="14" font-weight="600" fill="#1e40af">Your patient portal</text>
  <text x="135" y="242" text-anchor="middle" font-size="11.5" fill="#1e40af">your UI + your login</text>
  <rect x="530" y="110" width="190" height="240" rx="10" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="625" y="222" text-anchor="middle" font-size="14" font-weight="600" fill="#0f172a">Canvas</text>
  <text x="625" y="242" text-anchor="middle" font-size="11.5" fill="#475569">clinical source of truth</text>
  <!-- FHIR (into Canvas) -->
  <text x="380" y="145" text-anchor="middle" font-size="13" font-weight="600" fill="#0f172a">FHIR API</text>
  <text x="380" y="160" text-anchor="middle" font-size="11.5" fill="#475569">OAuth2 · standard resources (read/write)</text>
  <line x1="230" y1="172" x2="526" y2="172" stroke="#475569" stroke-width="1.5" marker-end="url(#pe-a)"/>
  <!-- SimpleAPI (into Canvas) -->
  <text x="380" y="213" text-anchor="middle" font-size="13" font-weight="600" fill="#0f172a">SimpleAPI</text>
  <text x="380" y="228" text-anchor="middle" font-size="11.5" fill="#475569">API key · custom endpoints (read/write)</text>
  <line x1="230" y1="240" x2="526" y2="240" stroke="#475569" stroke-width="1.5" marker-end="url(#pe-a)"/>
  <!-- Webhooks (out to your app) -->
  <text x="380" y="281" text-anchor="middle" font-size="13" font-weight="600" fill="#0f172a">Events → webhook</text>
  <text x="380" y="296" text-anchor="middle" font-size="11.5" fill="#475569">shared secret · Canvas pushes changes</text>
  <line x1="530" y1="308" x2="234" y2="308" stroke="#475569" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#pe-a)"/>
  <!-- legend -->
  <text x="380" y="392" text-anchor="middle" font-size="11.5" fill="#475569">→ into Canvas: Canvas authenticates you &#160;·&#160; ← out to you: your app verifies Canvas's secret</text>
</svg>
</div>

A typical combination:

- **FHIR API** for the bulk of standard reads and writes (patients, appointments, conditions, coverage…).
- **SimpleAPI** where you need something FHIR doesn't expose, a tailored/bundled response, or custom data — your app hits one plugin endpoint instead of stitching several calls.
- **Events → webhooks** to keep your app in sync as things change in Canvas, instead of polling.

### FHIR API — read & write standard Canvas data directly

**Best for:** standard resources (Patient, Appointment, Condition, Coverage, etc.) read or written straight from your app.

**Auth (your app → Canvas):** Canvas issues OAuth2 tokens with SMART on FHIR scopes. For a portal where a patient logs in and must only see their **own** record, use a [patient-scoped token](/api/customer-authentication/#patient-scoped-tokens) — it's locked to a single patient and Canvas enforces it server-side, so any read or write touching another patient is rejected. See [Customer Authentication](/api/customer-authentication/) for the full flow, scopes, and the `user/` and `system/` contexts.

See the [FHIR API reference](/api/) and [Auth best practices](/api/authentication-best-practices/).

Examples:

- [canvas_fhir_client](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/canvas_fhir_client) (SDK) — a Python client that authenticates and reads/writes Canvas FHIR resources.
- [cms-access-fhir-client](https://github.com/medical-software-foundation/canvas/tree/main/extensions/cms-access-fhir-client) (MSF) — FHIR-client mechanics in action (OAuth plus a full request/response exchange), here integrating with the external CMS ACCESS FHIR APIs.

### SimpleAPI — build the exact endpoints your app wishes Canvas had

Where FHIR gives you standard resources, **SimpleAPI lets you define your own** — you own the URL, the request, and the JSON response shape, all running inside a Canvas plugin. Instead of bending your app to fit a generic API, you build the endpoint your app actually wants and call it directly.

_New to the idea? Read the announcement: [Introducing Custom API Endpoints with the Canvas SDK](https://www.canvasmedical.com/articles/introducing-custom-api-endpoints)._

This is where SimpleAPI shines:

- **Shape the payload to your UI.** Return exactly the fields a screen needs, already assembled — no over-fetching, no reshaping FHIR bundles on the client.
- **Collapse many calls into one.** Bundle related reads and writes into a single round-trip, so a screen that would take five FHIR calls takes one. Fewer requests, simpler client code, faster load.
- **Reach data FHIR doesn't expose.** Surface your plugin's own [Custom Data](/sdk/custom-data/), computed values, or anything else in the [data module](/sdk/data/).
- **Run your logic server-side, next to the data.** Validation, orchestration, and business rules live in the plugin — close to Canvas and behind your key — instead of scattered across your app.

Reads come from the [data module](/sdk/data/); writes go through [Effects](/sdk/effects/) and [Commands](/sdk/commands/) (the SDK data models are read-only).

**Auth (your app → Canvas):** an **API key** — declare a secret in the plugin and send it in the `Authorization` header (`APIKeyAuthMixin`). Simple, and the right choice for an external caller.

See [SimpleAPI HTTP handlers](/sdk/handlers-simple-api-http/).

SDK examples:

- [api_samples](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/api_samples) — start here; the core request/response patterns.
- [charting_api_examples](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/charting_api_examples) — endpoints that read and write chart data.
- [note_management_app](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/note_management_app) — a fuller app built on SimpleAPI endpoints.
- [custom_data_room_booking](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/custom_data_room_booking) — endpoints backed by Custom Data.

Real-world examples (MSF):

- [lab-result-api](https://github.com/medical-software-foundation/canvas/tree/main/extensions/lab-result-api) — one `GET /lab-result/<id>` returns a lab report with its patient, originating order, ordering provider, and nested result values assembled into a single response. A textbook "collapse many calls into one, shaped to your UI" endpoint.
- [cpt-billing-api](https://github.com/medical-software-foundation/canvas/tree/main/extensions/cpt-billing-api) — a write endpoint that adds CPT billing line items to a note from an external caller.
- [note-command-api](https://github.com/medical-software-foundation/canvas/tree/main/extensions/note-command-api) — read notes with enhanced command data, and create notes via `POST /create-note` with flexible identifier lookup.
- [custom-observation-management](https://github.com/medical-software-foundation/canvas/tree/main/extensions/custom-observation-management) — an API-key-authed read/write API over a clinical resource: `GET` a single observation, a filtered list, or the available filters, and `POST` to record a new one.

### Events → webhooks — Canvas pushes changes to your app the moment they happen

Instead of your app constantly polling Canvas asking "anything new?", **let Canvas tell you.** A plugin subscribes to the events you care about — an appointment booked, a task created, a patient updated — and POSTs to your endpoint the instant it happens.

Why reach for webhooks:

- **Real-time sync, no polling.** Keep an external system current — a billing platform, a CRM, a data warehouse, your own app's database — the moment data changes, instead of nightly jobs that are always a little stale. For example, a patient gives the front desk an updated address; a webhook pushes that change to your app so it's already reflected the next time they log in to your portal.
- **Trigger downstream workflows.** Fire an appointment reminder, page a care team, kick off a prior-auth, or open a ticket in your system as soon as the triggering event lands.
- **Fan out from one event.** A single Canvas change can notify several systems at once, each with the payload it needs.
- **Lower latency and load.** You react in seconds and skip the wasted requests — and the changes missed between polls — that polling brings.

**Auth (Canvas → your app — reversed):** **you** secure your receiving endpoint. The plugin sends a shared secret/signature (stored as a plugin secret) that your app verifies; no Canvas token is involved on the inbound call.

See the [SDK Events reference](/sdk/events/), the [HTTP Request effect](/sdk/effect-http-request/), and the [Creating Webhooks guide](/guides/creating-webhooks-with-the-canvas-sdk/).

SDK examples:

- [example_patient_sync](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/example_patient_sync) — push patient changes to an external system on create/update.
- [coverage_metadata_sync](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/coverage_metadata_sync) — sync coverage metadata when it changes.

Real-world examples (MSF):

- [appointment-sync-webhook](https://github.com/medical-software-foundation/canvas/tree/main/extensions/appointment-sync-webhook) — POSTs appointment lifecycle events (created, cancelled, no-show) to an external system as they happen.
- [task_webhook_notification](https://github.com/medical-software-foundation/canvas/tree/main/extensions/task_webhook_notification) — sends a customizable payload to your endpoint whenever a task is created or updated.
- [gcal_sync](https://github.com/medical-software-foundation/canvas/tree/main/extensions/gcal_sync) — near-real-time two-way sync between Canvas appointments and Google Calendar, with Canvas as the system of record.

---

## Still deciding?

- Want a portal live quickly with minimal effort → **Path 1**, and [contact Support](https://canvas-medical.help.usepylon.com/) to set the page toggles.
- Happy with the built-in portal but need a few custom touches → **Path 2**; skim the [Patient Portal config hub](/sdk/patient-portal/).
- Building your own branded experience → **Path 3**; start with the [FHIR API](/api/) and add SimpleAPI and webhooks as needed.

<br/>
<br/>
<br/>
