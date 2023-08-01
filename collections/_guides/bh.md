---
title: "Care Modeling: Behavioral Health"
guide_for:
 - /api/patient/
 - /api/coverage/
 - /api/consent/
 - /api/questionnaireresponse/
 - /documentation/configuringquestionnaires/
---

Most of today’s EMR’s work like cash registers, treating patient interactions as transactional. The transactional design forces data to be captured and represented in the same transactional manner. This ultimately pushes the clinician to think transactionally. The Canvas approach to charting is fundamentally different. We invented Narrative Charting in order to model the actual work of the clinician instead. We start all of our notes with a blank canvas and allow you to pull in Commands to document what is relevant for that patient and interaction. This works extremely well for behavioral health, as our application doesn’t force your clinicians to navigate through a set workflow or the typical SOAP note, if it’s not necessary to do so.

In addition to our entirely new way of charting, our FHIR API and Workflow Kit make Canvas extremely extensible. You can build both a differentiated patient experience and influence the in-application workflows using the available read and write endpoints, and Protocols.

## Launching your Behavioral Health Care Model: Questions to Ask
The world is facing a mental health crisis and you want to help tackle it 🙌. With recent cultural changes, scientific and technological advancements, improved data sharing, and a shift towards consumerism, the behavioral health space is prime for disruption.  To be successful and drive value, you’ll need to differentiate on your care model. You’ll likely start by asking the questions outlined below. Once you’ve settled on a direction for each, we’ve outlined recommended next steps to get started. <br> <br> 

### What problem and/or population are we addressing?  
What is your target population? Does your care model support a broad range of mental health concerns for all genders and ages (everything in the DSM), or are you focused on adolescents suffering from eating disorders? Recognizing your Diagnostic Range is a critical starting point, as it informs the complexity of your healthcare practice.<br><br>
<b>After defining your target population you may want to:</b> <br><br>
👉Customize search results throughout the application to reduce noise and drive focus.<br>
👉Configure clinical templates in order to collect the necessary data to inform your clinical decision <br>making.
### How will we treat our patients?
Next you’ll need to determine what services and treatments you plan to offer. As your Scope of Interventions broadens - and your care model gets more complex - you will also need to apply more rigor in your safety framework.<br><br>
<b>After determining your scope of interventions you can:</b><br><br>
👉Set up staff permissions to ensure team members can perform the duties of their role<br>
👉Suggest alternative interventions when clinically appropriate <br>
### What is the makeup of our Care Team? 
As the demand for behavioral health services continues to rise, various factors, including an aging workforce, recruitment and retention challenges, geographic disparities, and financial barriers, have contributed to the scarcity of providers. As a result, fewer than half of people with a mental illness were able to access timely care in 2021. Innovating on the makeup of your care team can help to address this shortage and set you apart. Canvas was built to support interdisciplinary care teams that take advantage of team members’ strengths, bring in more assistive clinical workers, and allow everybody to operate at the top of their license.
<br><br>
<b>Effective [Team Based Care]({{site.baseurl}}/guides/team-based-care/) is made possible through:</b> <br><br>
👉 Defining roles and responsibilities<br>
👉 Granting appropriate access<br>
👉 Routing work to the right team or individual<br>
### How will we acquire patients?
Strategy around how you source and onboard new patients (or clients) is necessary to successfully attract and connect with individuals in need of mental health services, establish a positive first impression, gather comprehensive patient information, and prioritize the well-being and safety of patients throughout their care journey.<br><br>
You’ve acquired prospective patients, now you can:<br><br>
👉 Create your patient profiles to get started<br>
👉 Surface custom data points to ensure your care team has the necessary information<br>
👉 Incorporate patient collected data to expedite onboarding<br>
👉 Partner with Zus to avoid having to hunt down and manually enter historical records
### How will we interact with our patients/clients?
Understanding and effectively managing interaction modes in your behavioral healthcare model is crucial to providing a seamless and efficient patient experience. Implementing interconnected synchronous and asynchronous communication channels, guided by well-structured Utilization Policies, can streamline your operations, enhance patient engagement, and ultimately improve care outcomes.<br><br>
Depending on how you choose to interact with your patients, you may need to:<br><br>
👉Set your availability and define your appointment settings to maximize scheduling efficiency <br>
👉Create appointments using the API to support patient or third-party scheduling <br>
👉Sync Canvas appointments to your external calendars to reflect true availability <br>
👉Send  and receive patient messages to coordinate care between visits <br>
👉 Use Questionnaires to check in on your patient between visits<br>
👉Leverage tasks to organize queue-based work <br>
### How can we drive efficiency in our workflows? 
In the context of Care Modeling, content falls into two buckets: patient-facing content and care team-facing content. Once the content is defined, building in automation in the form of templates, macros, and guidance is crucial to effectively scale. <br><br>
To support your clinicians in delivering high quality care, you can: <br><br>
👉Create automations to accelerate documentation<br>
👉Develop recommendations to promote standards of care and alert clinicians of potential safety concerns<br>
### How will we get paid?  
Although listed last, payment should not be an afterthought. Incentives are important and your care model will undoubtedly be influenced by your payment model. We built our fully integrated Revenue module to support all models, including direct-to-consumer (D2C), self-insured employers (SIE), fee-for-service reimbursement (FFS), and/or value-based contracting (VBC)<br><br>
To get paid, you may need to:<br><br>
👉Set up your instance to document and charge for the services you provide<br>
👉Use our API to automate your revenue cycle<br>

The examples below are only a starting point to give you some ideas of how you could leverage Canvas’s capabilities. You’ll find that we’ve barely scratched the surface and the opportunities are endless as you navigate through your Care Modeling journey.








