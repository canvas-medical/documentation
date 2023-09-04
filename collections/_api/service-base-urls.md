---
title: "Service Base URLs"
layout: apipage
---

{% include alert.html type="warning" content="These URLs represent the updated API. If you are using it for the first time,  you will need to reach out to have it enabled for your instances." %}

## Sandbox URLs

Spin up a sandbox environment at [https://dashboard.canvasmedical.com](https://dashboard.canvasmedical.com) to get started. There, you will choose an instance name. This will determine the base URL for your FHIR endpoint.

| URL Type              | URL                                         |
|-----------------------|---------------------------------------------|
| EMR User Interface    | `https://{instance-name}.preview.canvasmedical.com` |
| FHIR API              | `https://fumage-{instance-name}.preview.canvasmedical.com` |

**Example:**
If you choose to name your instance "galorndon-core," your EMR user interface would be reachable at [https://galorndon-core.preview.canvasmedical.com](https://galorndon-core.preview.canvasmedical.com), and your FHIR API would be reachable at [https://fhir-galorndon-core.preview.canvasmedical.com](https://fumage-galorndon-core.preview.canvasmedical.com).

## Production FHIR URLs

| Organization Name     | URL                                         |
|-----------------------|---------------------------------------------|
| modernfamilypractice  | `https://fumage-modernfamilypractice.canvasmedical.com` |
