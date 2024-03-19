---
title: Fixed Duplicative Patient Conditions based on Claim CREATE via API
layout: productupdates
tags: ui api bugfix
date: 2024-03-19
---
We have resolved an issue that resulted in duplicative conditions on a patient’s summary when a claim was created with an associated ICD-10 code via API. Now, we will only include the ICD-10 code in the patient’s condition list if the code is not already listed within the condition list as “active”.
