---
title: "Submit a Full Vital Panel through Canvas FHIR API"
guide_for:
- /api/observation/
---

Inside of the Canvas' [Vital Sign Command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs) there are many vital signs supported to document. 

TODO insert image

The Canvas [FHIR Observation Create](/api/observation/#create) endpoint supports writing some of the vital signs in the command. This guide will show you all the vitals that can be documented in the Create interaction.

<br>

* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Creating a vital panel via FHIR
2. Submit various vital signs into the same panel via FHIR
3. Perform a FHIR Observation Search to view the completed panel
<br>

* * *

### 1. FHIR Authentication

The rest of this guide will demonstrate many FHIR API calls into Canvas. Every example call below will include two places you will need to update to authenticate to the right Canvas Instance:

1. The `url` will show `https://fumage-example.canvasmedical.com/Observation`. You will need to replace `example` with the name of the Canvas instance you are using. 

2. One of the `header` elements will be `'Authorization: Bearer <token>'`. You will need to create this token following our steps laid out in [Customer Authentication](/api/customer-authentication)

### 2. Create a Vital Panel

First we will need to create the panel object to be able to save all the individual vital signs to. 