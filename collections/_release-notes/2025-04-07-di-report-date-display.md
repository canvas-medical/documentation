---
title: Lab/Imaging/Consult/Uncategorized Clinical reports from Data Integration to display as Clinical date as date and not datetime
tags: ui
layout: productupdates
date: 2025-04-07
---

When users upload and manually associate a Lab, Imaging, Consult, Uncategorized Clincial reports in Data Integration (DI), users enter in a date for Clinical Date. However, on the patient chart, these reports were displaying this information as a datetime, with the time always showing as midnight. This change will now show the information as a date. Reports that are electronically ordered or do not pass through DI and POC tests are not impacted by this change and will continue showing as datetime.