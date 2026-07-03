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

1. Contact us at {{CONFIRM: developer-access intake address}} with your organization name, a description of your application, the access model you need (patient-directed or population/bulk), and a technical point of contact.
2. We complete an authenticity-verification review. This process is objective and applied uniformly to all API users, and we complete it within **ten business days** of receiving your request.
3. Once verification is complete, we register and enable your application for production use within **five business days**.

We do not condition access on fees or royalties for the rights the API Condition of Certification protects, non-compete or exclusive-dealing terms, unrelated licenses, transfer of your intellectual property, Canvas-specific testing or certification, or reciprocal access to your application's data.

## Sandbox access

We provision a sandbox so your team can build and test before production enablement. Request sandbox credentials as part of step 1 above. Sandbox base URLs follow the pattern `https://fumage-<sandbox-name>.canvasmedical.com`; see the [Quickstart](/api/quickstart/) for making your first request.

## Registering your application

Once you have access to an instance (sandbox or production), register your application and obtain OAuth credentials by following [Customer Authentication](/api/customer-authentication/). That page documents the client-credentials and authorization-code flows and the available SMART scopes.

## Fees

{{CONFIRM: fee schedule and link}} Any permitted fees are limited to the recovery of costs reasonably incurred to develop, deploy, and host the certified API technology, consistent with 45 CFR 170.404(a). Fees, if any, are published in full so you can evaluate them before requesting access.

## Service base URLs

Canvas publishes service base URLs for its customers. See [Service Base URLs](/api/service-base-urls/).

## Terms of Use

Use of the API is governed by our [Terms of Use](/api/terms-of-use/).
