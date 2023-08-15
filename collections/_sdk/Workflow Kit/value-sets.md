---
title: "Value Sets"
slug: "value-sets"
excerpt: "Value sets contain lists of codes (RXNORM, SNOMED, ICD...) that represent concepts."
hidden: false
createdAt: "2021-09-22T22:18:36.624Z"
updatedAt: "2022-02-21T22:41:16.354Z"
---
# v2021

Value sets are bundled lists of codes (RXNORM, SNOMED, ICD...) that represent abstract concepts. These concepts can represent anything such as conditions, immunizations, patient attributes, and procedures.
Rather than working in multiple code systems with unwieldy lists of identifiers, value sets
make code readable and vastly reduces development time. 

The list is maintained by the [Agency for Healthcare Research and Quality](https://www.hcup-us.ahrq.gov/)
(or AHRQ) and is updated throughout the year to return the most up-to-date results.

**Example**

```python
from canvas_workflow_sdk.value_set.v2021 import Hba1CLaboratoryTest

last_test = patient.lab_reports.find(Hba1CLaboratoryTest).last()

```

While value sets are categorized into subsets, all can be imported using `from canvas_workflow_sdk.value_set.v2021 import <ValueSetClassName>`