---
title: "Surescripts staging test patients"
layout: documentation
---

Canvas can configure a dev instance to send and receive prescriptions against Surescripts' **staging** environment rather than production. This lets your team validate e-prescribing workflows (NewRx, RxRenewalRequest, MedicationHistory) end-to-end without affecting real patients or pharmacies.

This is a beta offering. **Reach out to your Canvas account team or [Canvas support](https://portal.usepylon.com/canvas-medical/forms/standard){:target="_blank"} to have your dev instance configured for Surescripts staging**; the infrastructure side of the setup (service endpoint overrides, signing keys, prescriber-customer mapping at the pharmacy gateway) is managed by Canvas Medical.

Once your instance is wired up, the rest is on the customer side. The Surescripts staging environment only returns mocked responses for a fixed set of canonical test patients, pharmacies, and prescribers; arbitrary fresh patients you create on your dev instance will not get medication history or refill responses. The sections below cover the canonical staging fixtures Canvas uses.

## The canonical staging prescriber

Canvas configures every staging-enabled dev instance with the same canonical prescriber so that outgoing NewRx messages route correctly through Surescripts staging back to your instance:

- **Name:** Wayne Best DO
- **NPI:** `3688523885`
- **SPI:** `5630156655001`
- **Date of birth:** 1966-09-09
- **Sex at birth:** male
- **Role:** Physician (DO)
- **License:** California Medical Board, license A60695, valid 2020-06-16 through 2035-06-16
- **Address:** 150 Monument Road, Suite 500, Philadelphia, PA 19019
- **Contact:** phone / fax 914-960-3674; email `pharmacy-staging-<instance-name>@canvasmedical.com`

When you sign a NewRx in staging, **sign as Wayne Best**, not as your own user. The SPI on the outgoing message has to match the prescriber Canvas has mapped at the pharmacy gateway, or the inbound RxRenewalRequest will not route back to your instance.

## Canonical test patient

Surescripts staging will only return medication history and refill responses for canonical test patients whose demographics it recognizes; arbitrary fresh patients you create on your dev instance will not return responses. The canonical test patient Canvas uses for staging is:

| Field   | Value                                                |
| ------- | ---------------------------------------------------- |
| Name    | Zachary Delaplaine                                   |
| DOB     | 12/01/2010                                           |
| Gender  | Male                                                 |
| Address | 901 Sauvblanc Blvd, Petaluma, CA 94952               |
| Weight  | 62 lb                                                |
| Height  | 51 in                                                |

Create this patient on your dev instance with the demographics **exactly as listed** &mdash; address mismatches (especially ZIP code) are the most common cause of failed routing on the return refill request.

## Canonical test pharmacy

Set the patient's preferred pharmacy to the canonical pharmacy paired with this patient rather than picking from Canvas's general pharmacy directory:

- **Name:** Shollenberger Pharmacy
- **NCPDP:** `1655458`
- **Address:** 2002 S. McDowell Blvd Ext, Petaluma, CA 94954

Using a pharmacy outside the canonical pairing will produce a NewRx that looks accepted but never closes the refill loop.

## Surescripts staging service hours

Surescripts staging is only available **Monday through Friday, 8:00 AM to 6:00 PM Eastern Time**. NewRx messages sent outside those hours will not return a response. There is no Sev 1 escalation available for staging; Sev 2 cases receive an initial response in 2-4 business hours.

## What to expect

A few behaviors are normal in Surescripts staging but do not reproduce in production. Treat these as staging artifacts, not Canvas defects:

- **The medication on the inbound refill request may not match what you prescribed.** Surescripts staging response templates carry their own bundled medication payloads, so the drug on the inbound RxRenewalRequest comes from the template, not your outgoing NewRx. To get a clean match, pick a NewRx medication that aligns with the template you'll use to respond (for `INT-RENEWALREQ-1a`, that is Augmented Betamethasone 0.05% Topical Ointment, 14.555 grams, 3 refills).
- **The provider name shown on the inbound refill card may differ from the prescriber who signed.** Surescripts staging's pharmacy admin UI does not enforce provider-name consistency. Canvas routes by SPI, not by displayed name, so the refill still associates correctly when it lands.

## When things don't work

If you have configured the patient, the pharmacy, and the prescriber as above and a NewRx still does not produce an inbound refill response, the most likely causes are:

- The patient's demographics do not exactly match the canonical test patient above (re-check ZIP, street suffix, exact name spelling)
- The preferred pharmacy is not the canonical pharmacy paired with this patient
- You signed the NewRx as your own user rather than as Wayne Best
- The message was sent outside Surescripts staging service hours (M-F 8am-6pm ET)

Once those are confirmed, contact [Canvas support](https://portal.usepylon.com/canvas-medical/forms/standard){:target="_blank"} and we can check the prescriber-customer mapping at the pharmacy gateway, inbound logs, and directory state on Canvas's side. If Canvas's side looks clean and Surescripts staging never delivered, the next step is a Sev 2 case with Surescripts via their Self Service Portal (Support &rarr; Report a Problem &rarr; Certified Technology Vendors); phone fallback is 1-866-797-3239, Opt 1 Opt 1.
