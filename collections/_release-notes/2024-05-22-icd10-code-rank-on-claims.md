---
title: ICD-10 Codes Rank on Claims
date: 2024-05-22
tags: bugfix
layout: productupdates
---
Resolves bug that incorrectly ranked ICD-10 codes on claims. ICD-10 codes are now ranked on claim based on time of insertion within a note or claim, newer codes will be ranked below previously placed codes to reflect the correct order for accurate billing.