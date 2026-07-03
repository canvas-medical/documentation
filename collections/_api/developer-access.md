---
title: "Third-Party Developer Access"
layout: apipage
---

Canvas Medical is certified to ONC's [§170.315(g)(10)](/product-updates/rwt/) *Standardized API for Patient and Population Services*. This page describes how a third-party developer requests access to the FHIR API, the verification we perform, and the timelines we commit to under [45 CFR 170.404](https://www.ecfr.gov/current/title-45/section-170.404).

## Two kinds of access

The API supports two distinct access models. The authorization gate is different for each, and it is important to know which one your application needs.

### Patient-directed access

An individual patient authorizes your application to access **their own** health information. The patient authenticates and grants consent through the [SMART on FHIR](/api/customer-authentication/#smart-on-fhir-scopes) authorization-code flow, and the resulting token is scoped to that patient (`patient/` context). The patient's authorization is the only approval required — access does not depend on separate sign-off from the patient's practice.

### Population and bulk access

A practice or organization using Canvas as its EHR authorizes access to data across its patient population, typically through the client-credentials flow (`system/` context) and bulk export. This access is authorized by the practice or organization that holds the data.

## Requesting access

Third-party developers do not need to be an existing Canvas customer to request access. To begin:

1. Contact us at [developer-access@canvasmedical.com](mailto:developer-access@canvasmedical.com) with your organization name, a description of your application, the access model you need (patient-directed or population/bulk), and a technical point of contact.
2. We complete an authenticity-verification review. This process is objective and applied uniformly to all API users, and we complete it within **ten business days** of receiving your request.
3. Once verification is complete, we register and enable your application for production use within **five business days**.

We do not condition access on fees or royalties for the rights the API Condition of Certification protects, non-compete or exclusive-dealing terms, unrelated licenses, transfer of your intellectual property, Canvas-specific testing or certification, or reciprocal access to your application's data.

## What we verify

Verification confirms the authenticity of your organization and your application. It is limited to identity and does not evaluate the merits of your product. We apply the same criteria to every API user. You provide:

- **Organization identity** — your registered legal business name and a verifiable business identifier, such as control of your organization's domain, a state business registration, or a D-U-N-S number.
- **A domain-verified contact** — a named representative reachable at an email address on your organization's domain who can act on the organization's behalf.
- **Application details** — the application name, a description of its intended use, the access model (patient-directed or population/bulk), and the redirect URIs or registered endpoints it will use.
- **Attestations** — that the application has a published privacy policy and terms, that it will access data only as authorized by the patient (patient-directed access) or the organization (population/bulk access), and that you will comply with applicable law.
- **Agreement to our [Terms of Use](/api/terms-of-use/).**

## Sandbox access

We provision a sandbox so your team can build and test before production enablement. Request sandbox credentials as part of step 1 above. Sandbox base URLs follow the pattern `https://fumage-<sandbox-name>.canvasmedical.com`; see the [Quickstart](/api/quickstart/) for making your first request.

## Registering your application

Once you have access to an instance (sandbox or production), register your application and obtain OAuth credentials by following [Customer Authentication](/api/customer-authentication/). That page documents the client-credentials and authorization-code flows and the available SMART scopes.

## Fees

There is no fee to register, verify, or enable a third-party application for access to the API.

## Service base URLs

Canvas publishes service base URLs for its customers. See [Service Base URLs](/api/service-base-urls/).

## Terms of Use

Use of the API is governed by our [Terms of Use](/api/terms-of-use/).
