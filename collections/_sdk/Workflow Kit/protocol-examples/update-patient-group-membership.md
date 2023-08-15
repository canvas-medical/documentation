---
title: "Update Patient Group Membership"
slug: "update-patient-group-membership"
hidden: false
createdAt: "2022-08-23T15:50:55.067Z"
updatedAt: "2022-08-24T16:29:52.491Z"
---
This example is a protocol that updates a Patients Groups Membership based on a Patient Consent. The example group operates on an opt-out basis, so patients are added to the group if they don't have the consent and removed if the consent has a state of `rejected`


**[Update Patient Group Membership code ](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/patient_grouping.py)**

After everything is uploaded and set up properly, once a rejected consent is added to a patient, they will be removed from the group.

This protocol utilizes functionality described in [Create/Update Canvas Resources from a Protocol](https://docs.canvasmedical.com/docs/createupdate-canvas-resources-from-a-protocol)