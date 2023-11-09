---
title: "Scheduled Reports"
layout: documentation
---

Reporting is key to understanding how your care model is performing. There will be data that you may want to reference on a regular basis. Scheduled reports allow you to automate the reporting process in Canvas using Google Delivered Planned Reports. You can access Google Delivered Planned Reports within your admin settings. 

## Adding Google Delivered Planned Reports
To add a Google Delivered Planned Reports, click add Google Delivered Planned Reports + in the top right corner and then complete the following form.

**Command:** Canvas has built some standard reports that you can select from. A description of each is listed below. You can also choose ‘custom sql query’ 

{% include alert.html type="info" content="Canvas uses PostgreSQL to deliver this data" %}

**Google spreadsheet id:** The spreadID is the last string of characters in the URL for your spreadsheet. For example, in the URL `https://docs.google.com/spreadsheets/d/1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDE8p-Bll4hps/edit#gid=0`, the spreadsheet ID is `1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDE8p-Bll4hps`.

{% include alert.html type="warning" content="The Google Sheet must be located in the Canvas Shared Resources folder that was created for you during implementation. That folder is also shared with a Canvas user with write permissions needed to load the data into the sheet. The two users are: 
<ul>
  <li>canvas-sheets@astute-nuance-203013.iam.gserviceaccount.com</li>
  <li>dev-canvas-sheets@astute-nuance-203013.iam.gserviceaccount.com</li>
</ul>"  %}

**Frequency:** Choose how often you would like the report to run

**Planned day:** This is only necessary if you selected weekly or monthly for your frequency. If you selected weekly, then choose the day of the week. If you selected monthly, then choose the day of the month. 

**Planned hour:** The time that the report will run. Reports run at the top of the hour for your organization's timezone. 

**Status** This defaults to 'active' for new reports. You can select 'inactive' if you want to delay using this new report. 

**Alert email:** The system will also send an email to this address when the spreadsheet is populated with results.

**Data management:** You can choose whether to append the results to the existing tab, or add a new tab for each run. You may want to add to existing tab if your report only includes incremental changes from the last run. 

**Sql query:** Add your query if you selected custome SQL query above

**Title:** Name your report.

## Updating Google Delivered Planned Reports

To edit a Google Delivered Planned Report, click into an existing report and make changes as needed. 
