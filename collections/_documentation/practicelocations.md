---
title: "Practice Locations"
---

Practice locations allow you to configure your Canvas instance to support multiple regions, offices, or use cases. Practice locations are used to group schedules, drive billing workflows, customize outbound communications for both patients and other providers, and drive preferences in clinical workflows.

You will need to configure at least one Practice Location during your implementation. Post launch, you can continue to add additional locations as you grow. <br><br>

To set up a practice location, navigate to **Practice › Practice Locations ›** in your settings menu.


***
**Organization**<br> <br>
This will default to the organization that has been created for your instance. Canvas currently only supports one organization per instance.<br>

***
**Place of Service Code** <br><br>
This will be the default POS code for the practice. POS codes set at the Note Type level will take precedence but this serves as a backup <br>

***
**Full Name**<br> <br>
Name your location. This will show in <font color="red"> KOUPDATE WHERE IS THIS USED</font> 

***
**Short Name**<br> <br>
Name your location. This will show in <font color="red"> KOUPDATE WHERE IS THIS USED</font> 

***
**Background Image URL**<br> <br>
This image displays on the login page. Our default image is the XXXX. If you would like to customize this image, please reach out to support to have them provide the necessary URL. When submitting images we recommend 800 x 1200 <font color="red"> KOUPDATE HOW IS THIS SET BY LOCATION - get recommended size - what is our photo of</font> 

***
**Background Gradient**<br><br>
The background colors in the patient chart can be customized. The default setting is a gradient of blue to orange to mimic the sunset of our default background image. You can change this to match your brand colors if desired"

***
**Active**<br><br>
This should be checked if you are currently operating out of this location. Marking a practice location will remove them from your scheduling dropdowns. <font color="red"> KOUPDATE what happens when inactive</font> 

***
**Bill Through Organization**<br><br>
If all of your Practice Locations share the same billing information, you can select this checkbox to bill through the Organization. If you uncheck this box, the fields listed below will be leverage when creating claims. Reference the table below to see a side by side comparison. 

***
**Tax ID**<br><br>
Tax ID Number used in Box 25 (FEDERAL TAX I.D. NUMBER) on CMS1500 <br>

***
**Billing Location Name**<br><br>
Billing Name used in Box 33 (BILLING PROVIDER INFO & PH) on the CMS1500

***
**Group NPI number**<br><br>
Group NPI used in box 33a (BILLING PROVIDER GROUP NPI) on the CMS1500

***
**Taxonomy number**<br><br>
Taxonomy number is used in box 33b (Other ID#) on the CMS1500. Some payers require this. Max length of 10 characters. 

***
**Include ZZ qualifier for taxonomy code**<br><br>
This checkbox will include the ZZ qualifier before the taxonomy code on the CMS1500. A ZZ taxonomy qualifier may be required by some payers when submitting paper claims.<br><br>

#### Billing Though your Organization vs. Practice Locations

| Form item 	| Bill Through Organization == True             	| Bill Through Organization == False     	|
|-----------	|-----------------------------------------------	|----------------------------------------	|
| 25        	| Organization tax id                           	| Note  Pracictice Location tax id                   	|
| 32        	| Note location billing or first address        	| Note Practice Location billing or first address 	|
| 32 a      	| Note location npi_number                      	| Note Practice Location npi_number               	|
| 33        	| Organization billing address or first address 	| Note Practice Lcocation billing address          	|
| 33 a      	| Organization group npi number                 	| Note Practice Location group npi number         	|
| 33 b      	| Organization group taxonomy number            	| Note Practice Location taxonomy number          	|


#### Practice Addresses
#### Practice Location Contact Points
#### Practice Location Settings

***
**Pharmacy**<br><br>

***
**Imaging Center**<br><br>

***
**Service Area Zip Codes**<br><br>

***
**Preferred Lab Partner**<br><br>

***
**Preferred Lab Locations**<br><br>

***
**Scanner Integration**<br><br>

***
**Provider Message Text Message Template**<br><br>

***
**Provider Message Email Template**<br><br>

***
**Provider Message Email Subject**<br><br>




[//]: # (I have questions)