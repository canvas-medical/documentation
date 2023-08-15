---
title: "Protocols"
slug: "protocols"
hidden: true
createdAt: "2021-10-08T13:44:40.503Z"
updatedAt: "2021-10-08T13:44:40.503Z"
---
### Abstract Classes

To declare a parent Protocol class that does not implement recommendation logic, add a Meta class with the attribute `abstract = True`. This code will need to be uploaded alongside the implementation of the protocol.
[block:code]
{
  "codes": [
    {
      "code": "class ParentQualityMeasure(ClinicalQualityMeasure):\n\n    class Meta:\n        abstract = True",
      "language": "python"
    }
  ]
}
[/block]