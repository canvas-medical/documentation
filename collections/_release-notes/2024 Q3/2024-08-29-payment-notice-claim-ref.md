---
title: Collect Payment Prior to Services Being Rendered 
date: 2024-08-29
layout: productupdates
tags: api

---
We have added an extension to the FHIR PaymentNotice endpoint that references the claim to which the payment is or should be applied. When using this reference in the create interaction, you can now bring a balance below zero, supporting prepayment workflows such as copays and coinsurance. Without a reference to a specific claim, the paymentnotice amount cannot exceed the patient’s account balance. [Read more](/api/paymentnotice/#create). 