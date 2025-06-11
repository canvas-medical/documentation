---
title: 06.11.2025
layout: productupdates  
tags: ui bugfix config
date: 2025-06-11
---

Today's release includes the following updates: 

- **Configuration option to submit SSN with claims**<br/>
  In Settings, Insurers records will have the option to submit claims with SSN. By default, the checkbox is not selected and SSN will not be added to submitted claims.

- **Ability to assign teams to Labs, Imaging, Consults, and Uncategorized Reports**<br/>
  Users will be able to assign teams in addition to individuals in [Data Integration](https://canvas-medical.help.usepylon.com/articles/7371085164-data-integration) and for [Labs](https://canvas-medical.help.usepylon.com/articles/1652834476-processing-lab-reports), [Imaging](https://canvas-medical.help.usepylon.com/articles/7566748234-process-image-results), [Consults](https://canvas-medical.help.usepylon.com/articles/8177085140-consult-report-review), and [Uncategorized reports](https://canvas-medical.help.usepylon.com/articles/2240101532-command-uncategorized-document-review). The filter for “Me or my teams” will show all reports that are assigned to an individual or to the person’s teams, even if assigned to a different individual. A red badge icon displays on any reports that are assigned to the logged in individual or their team, if no individual is assigned. Team assignments are now supported via [FHIR DocumentReference](/api/documentreference) endpoints.

- **New appointment icons to show visit/note type**<br/>
  To make it easier for users to know what the visit type is prior to checking, appointments on the patient chart will also display the visit or note type icon. [Read more.](https://canvas-medical.help.usepylon.com/articles/4617508394-managing-appointments)

- **Allow support of comparator in FHIR Diagnostic Report Create**<br/>
  For lab values with a valueQuantity, there is now support for the comparator values of <, >, <=, >= to be passed. [Read more.](/api/diagnosticreport-operations)

- **Bug fixes**
	- Fix a bug where signatures were not saving when annotating PDFs.
	- Improved the UI responsiveness for smaller screen sizes when documenting notes in the patient timeline.
	- Fixes the note printout when an assess coding gap command is entered in error and causes all the commands in the printout to have an incorrect strikethrough
