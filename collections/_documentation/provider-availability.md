---
title: "Provider Availability"
layout: documentation
---
Scheduling patient appointments occurs within Canvas but to manage provider availability, Canvas uses an integration with Google Calendar. 
<br>
<br>
## Linking GSuite
Your implementation will include linking either your existing GSuite or a Canvas provided account in order to manage availability. If you need to make adjustments post implementation, please reach out to our support team. 
<br>
<br>

## Setting Availability

You will use calendars to both create availability as well as block it. [Adding a calendar](https://support.google.com/calendar/answer/37095?hl=en) in gCal using the naming conventions outlined below will create the connection to Canvas. You can also add a staff key to the description to ensure that future name changes do not impact the ability to sync. Keys can be found on each staff profile page.

![new-gcal](/assets/images/new-gcal.png){:width="80%"}

{% include alert.html type="danger" content="When creating calendars in gCal, make sure to use the same time zone that was used when configuring your instance" %}
<br>
### Calendars used to create availability

* **"First Last: Clinic" Calendar (one calendar per provider):** This defines the times that a particular provider is available for patient appointments. (e.g. John Smith: Clinic) If a provider has different availability across multiple practice locations, you can create unique provider calendars for each location using the following naming convention: "First Last: Clinic: Practice Location Name". (e.g. John Smith: Clinic: Canvas Clinic Oakland and John Smith: Clinic: Canvas Clinic San Francisco)

* **"First Last: Clinic: Location"**  If a provider has different availability across multiple practice locations, you can create unique provider calendars for each location using the following naming convention: "First Last: Clinic: Practice Location Name". (e.g. John Smith: Clinic: Canvas Clinic Oakland and John Smith: Clinic: Canvas Clinic San Francisco)
<br><br>
![clinic calendar](/assets/images/clinic-calendars.png){:width="90%"}

### Calendars used to block availability

* **"Organization Admin" Calendar:** This defines the times that the entire organization is unavailable for patient appointments. This is typically used for all-staff meetings or lunch hours. (e.g. Organization Admin) If there is more than one practice location the naming convention for that particular calendar will be the following "Organization Admin: Name".

* **"First Last: Admin" Calendar (one calendar per provider):** This defines the times that particular provider is unavailable for patient appointments. This is used to set large blocks of time off for vacation or sick leave or to set small blocks of time aside for the provider to work on administrative tasks (e.g. John Smith: Admin). This will be displayed in Canvas across all clinics and each individual clinic by location.

* **"Same-Day Hold" Calendar:** These times are reserved for same-day appointments for the entire practice or per provider (e.g. Same-Day Hold or First Last: Same-Day Hold). These times will not show up as available when an appointment is being scheduled until the day of the appointment: If I set a same-day hold from 430-5pm on April 5th, this means that these time slots will show as unavailable for appointments until April 5th.

* **"Next-Day Hold"Calendar:**  These times are reserved for next-day appointments for the entire practice or per provider **(Next-Day Hold or First Last: Next-Day Hold)**. These times will not show up as available until the morning of the day prior to the hold itself: If I set a next-day hold from 1030am-11am on April 5th, this means that these time slots will show as unavailable for appointments until the morning of April 4th. 

![calendar blocks](/assets/images/calendar-blocks.png){:width="90%"}




