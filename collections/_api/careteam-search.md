---
title: "CareTeam Search"
slug: "careteam-search"
excerpt: "Search CareTeams for a particular patient or practitioner"
hidden: false
createdAt: "2021-08-27T23:11:06.127Z"
updatedAt: "2022-06-06T14:45:56.451Z"
---
## Creating a Care Team for a Patient in Canvas

See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) to see how to add practitioners to a patient's care team. 
[block:api-header]
{
  "title": "Supported Participant Types"
}
[/block]
While the FHIR spec allows for multiple "person" types to be participants in a Care Team, Canvas only supports Staff members (FHIR Practitioner Types) to be participants in a Care Team. Thus, when searching by participant, we only support Practitioner references. 

To figure out how to set up Care Teams, see our [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams)