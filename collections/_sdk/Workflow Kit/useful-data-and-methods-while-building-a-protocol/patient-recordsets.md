---
title: "Patient Recordsets"
slug: "patient-recordsets"
excerpt: "Base class representing sorted sets of patient records (conditions, immunizations, etc.) for a patient."
hidden: false
createdAt: "2022-01-24T23:54:42.436Z"
updatedAt: "2023-05-17T21:49:08.755Z"
---
Patient recordsets are sorted sets of records (conditions, immunizations, etc.) for a patient that are available within protocols.  They come with all kinds of handy, chainable methods that allow you to iterate, filter, and find the records you're looking for. 

You can iterate through them and get to the record data:

```python
for condition in self.patient.conditions:
    print(f'Sorry, you have {condition['name']}')
```

 Use filters to filter on objects:

```python
self.patient.referrals.filter(order=None)  # find referrals where `"order": null`
self.patient.referrals.filter(timestamp__lt=arrow.now())
```

 Filters can use any of the following appended to the property name (with a `__` in between):

```
exact, iexact,
contains, icontains,
gt, gte, lt, lte,
startswith, endswith, istartswith, iendswith
```

If not specified, exact will be used by default.

To filter on a nested objects, use double underscore.

```python
self.patient.referrals.filter(report__status='NEW')
```

You can exclude records as well, using the same rules and operators as filter:

```python
self.patient.conditions.exclude(clinicalStatus='resolved')
self.patient.referrals.exclude(report__status='NEW')
self.patient.referrals.exclude(timestamp__gte=arrow.now())
```

You can also find records by value set:

```python
from canvas_workflow_kit.value_set.v2018 import Diabetes
  
self.patient.conditions.find(Diabetes)
```

Filter by date in various ways:

```python
from canvas_workflow_kit.timeframe import Timeframe

start_date = arrow.get('2021-01-01')
end_date = start_date.shift(years=1)
timeframe = Timeframe(start=start_date, end=end_date)
self.patient.conditions.intersects(timeframe)

now = arrow.now()
self.patient.conditions.before(now)

yesterday = now.shift(days=-1)
self.patient.conditions.after(yesterday)
```

Most methods are chainable:

```python
from canvas_workflow_kit.timeframe import Timeframe
from canvas_workflow_kit.value_set.v2018 import Diabetes

start_date = arrow.get('2021-01-01')
end_date = start_date.shift(years=1)
timeframe = Timeframe(start=start_date, end=end_date)

self.patient.conditions.find(Diabetes).intersects(timeframe)
```

 Except `first`, `last` and `last_value`, which pick the last record and extract a value from it:

```python
from canvas_workflow_kit.timeframe import Timeframe
from canvas_workflow_kit.value_set.v2018 import (Diabetes, Hba1CLaboratoryTest)

start_date = arrow.get('2021-01-01')
end_date = start_date.shift(years=1)
timeframe = Timeframe(start=start_date, end=end_date)

self.patient.conditions.find(Diabetes).intersects(timeframe).first()
self.patient.conditions.find(Diabetes).intersects(timeframe).last()
self.patient.lab_reports.find(Hba1CLaboratoryTest).within(timeframe).last_value()
```

Here is a full list of patient recordsets that are available in your protocols:

- Addresses `self.patient.addresses`
- Administrative Documents `self.patient.administrative_documents`
- Allergy Intolerances `self.patient.patient.allergy_intolerances`
- Appointments `self.patient.appointments`
- Billing Line Items `self.patient.billing_line_items`
- Patient's Care Team `self.patient.care_team_memberships`
- Conditions `self.patient.conditions`
- Consents `self.patient.consents`
- Patient's Contacts `self.patient.patient['contacts']`
- Patient's Coverages `self.patient.coverages`
- Patient Groups `self.patient.groups`
- Imaging Reports `self.patient.imaging_reports`
- Immunizations `self.patient.immunizations`
- Instructions `self.patient.instructions`
- Inpatient Stays `self.patient.inpatient_stay`
- Interviews `self.patient.interviews`
- Lab Orders `self.patient.lab_orders`
- Lab Reports `self.patient.lab_reports`
- Medications `self.patient.medications`
- Messages `self.patient.messages`
- Prescriptions `self.patient.prescriptions`
- Procedures `self.patient.procedures`
- Protocol Overrides `self.patient.protocol_overrides`
- Reason For Visits `self.patient.reason_for_visits`
- Referral Reports `self.patient.referral_reports`
- Referrals `self.patient.referrals`
- Suspect HCCS `self.patient.suspect_hccs`
- Upcoming Appointments `self.patient.upcoming_appointments`
- Upcoming Appointment Notes `self.patient.upcoming_appointment_notes`
- Tasks `self.patient.tasks`
- Patient's telecoms `self.patient.patient['telecom']`
- Vital Signs `self.patient.vital_signs`

And a few other helpful properties on the patient object:

- `self.patient.patient` --> an object of patient demographic information
- `self.patient.created` --> date the patient was created
- `self.patient.patient_key` 
- `self.patient.first_name`
- `self.patient.last_name`
- `self.patient.date_of_birth`
- `self.patient.birthday`
- `self.patient.age`
- `self.patient.is_female`
- `self.patient.is_male`
- `self.patient.is_african_american`
