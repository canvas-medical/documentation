---
title: "Team Based Care"
guide_for:
 - /api/patient/
---


Since the 1960s, teamwork has emerged as the preferred approach to collaboration in healthcare and is widely acknowledged for its ability to enhance healthcare quality. Studies show that medical care that involves interdisciplinary cooperation is linked to improved access, higher patient safety, reduced hospitalization rates, and fewer complications and medical errors. Medical professionals also experience significant advantages, such as increased job satisfaction and a decreased risk of burnout.

Although the benefits are well established, forming the right team to support your care model requires a careful balance between productivity and experience levels to ensure optimal care without compromising safety. The Canvas platform was purpose built to make this easier, supporting efficient team-based delivery through the following features and workflows.
<br>
<br>
### Defining roles and responsibilities 



{% tabs DRR %}

{% tab DRR  Developers %}

Once you’ve determined your appropriate staffing model and hired a team, your Super Users will need to set up [Roles](https://canvas-medical.zendesk.com/hc/en-us/articles/12851926883859-Creating-and-modifying-roles), [Teams](https://canvas-medical.zendesk.com/hc/en-us/articles/360057499933-Admin-Teams), and [Care teams](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) to ensure everyone can collaborate effectively. Make sure to advise them on what code systems and values will best support leveraging the data programmatically, either through your custom developed workflows using the Workflow Kit or API, or for reporting purposes.  

<b>Teams</b> in Canvas map to the [FHIR Group]({{site.baseurl}}/api/group/) Resource.
<br><br>
After working with your Super Users to set up Teams in your admin settings, they can be leveraged in the [FHIR Task Create]({{site.baseurl}}/api/task/) endpoint. You can do a FHIR Group Search to determine the Group ID associated with each Team and then assign a Task to that Team using the task-group extension.
```
"extension": [
  {
    "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
    "valueReference": {
      "reference": "Group/9bf1d726-8c04-4aed-8b0e-e066f4d54b13"
    }
  }
], 
```
<br>
A patient's <b>Care Team</b> can also be defined by assigning internal users (represented through the practitioner resource) to a patient's Care Team with a set role that has been configured in your admin settings (i.e. Primary Care Provider or Care Manager). A code and system is necessary here as well, so coordinate with your Super Users to make sure you are aligned. 
<br><br>
Our [FHIR CareTeam]({{site.baseurl}}/api/careteam/) resource allows you to read a patients care team, assign practitioners to patients with careteam roles using the update endpoint (acting as an upsert), and search for care team participation. Participation is often leveraged to then drive logic in your other workflows, including messaging and scheduling. 

{% endtab %}

{% tab DRR Super Users %}
Once you’ve determined your appropriate staffing model and hired a team, you can set up Roles, Teams, and Care Teams to ensure everyone can collaborate effectively. 
<br><br>
[Roles](https://canvas-medical.zendesk.com/hc/en-us/articles/12851926883859-Creating-and-modifying-roles): are configurable in Canvas and can drive a default permission set though [Auth Groups](https://canvas-medical.zendesk.com/hc/en-us/articles/13143167734291-User-permissions). <br>
[Teams](https://canvas-medical.zendesk.com/hc/en-us/articles/360057499933-Admin-Teams) are used to group work. By assigning responsibilities to teams, you can drive how automated tasks in Canvas are assigned. For instance, you may want all delegated referrals to go to a care coordination team.<br>
[Care teams](https://canvas-medical.zendesk.com/hc/en-us/articles/4409741845011-Care-Teams) are used to define the role an individual plays in a patient’s care. Once created you can assign staff to patients with a Care Team role. <br><br>
Teams and Care Teams are exposed via the FHIR API and can be leveraged in Protocols. Make sure to coordinate with your engineers to ensure they are set up with the appropriate code systems. When making changes or additions, make sure to communicate those internal so that any custom workflows can be updated as well.  

{% endtab %}

{% endtabs %}


<br>
### Granting appropriate access



{% tabs GAA %}

{% tab GAA Developers %}
Restriciting access to specific groups of patients can be accomplished by assigning [object permissions via auth groups](https://canvas-medical.zendesk.com/hc/en-us/articles/13143167734291-User-permissions). You can leverage any available data point available to the Workflow Kit to programtically create these groupings. You may need to partner with your Super Users to understand how each group should be defined, leveraging the Canvas data model. <br><br> If you cannot use one of the existing data points within a patient's profile, writing identifiers using the [FHIR Patient Create]({{site.baseurl}}/api/patient/) endpoint may be a good option. Using this attribute allows you to leverage external data (like payer program enrollments) to define your groups.

The Protocol below groups patients based on having a consent on file.

```python
# type: ignores

from canvas_workflow_kit import events
from canvas_workflow_kit.constants import CHANGE_TYPE
from canvas_workflow_kit.internal.integration_messages import (
    ensure_patient_in_group,
    ensure_patient_not_in_group
)    
from canvas_workflow_kit.protocol import (
    STATUS_NOT_APPLICABLE,
    ClinicalQualityMeasure,
    ProtocolResult
)


class PatientGrouping(ClinicalQualityMeasure):
    """
    Protocol that updates a patients membership in a group depending on a given consent. 
    This particular example is of an opt-out based group membership.
    """

    # Consent codes can be found in the Admin view
    CONSENT_CODE = 'A0001'  # replace with your opt-out consent's coding

    class Meta:
        title = 'Patient Grouping'

        version = '1.0.0'

        information = ''

        description = (
            'Protocol that updates a patients membership in a group depending on a given consent. '
            'This particular example is of an opt-out based group membership. ')

        identifiers = ['PatientGrouping']

        types = ['CQM']

        responds_to_event_types = [
            events.HEALTH_MAINTENANCE,
        ]

        authors = [
            'Canvas'
        ]

        compute_on_change_types = [
            CHANGE_TYPE.CONSENT
        ]

        funding_source = ''

        references = ['Written by Canvas']

    def has_opt_out(self) -> bool:
        consents = self.patient.consents.filter(category__code=self.CONSENT_CODE)
        
        if consents:
            state = consents[0]['state']
            return state == 'rejected'

        return False

    def compute_results(self) -> ProtocolResult:
        result = ProtocolResult()
        result.status = STATUS_NOT_APPLICABLE
       
        patient_key = self.patient.patient['key']

        # Get this UUID from the api_group.externally_exposable_id field
        patient_group_uuid = '00000000-0000-0000-0000-000000000000'  # Replace with your group's UUID.

        # This particular group operates on an opt-out policy, so a patient should be 
        # in the group unless they have the opt-out consent
        if self.has_opt_out():
            group_update = ensure_patient_not_in_group(patient_key, patient_group_uuid)
        else:
            group_update = ensure_patient_in_group(patient_key, patient_group_uuid)

        self.set_updates([group_update])

        return result
```

{% endtab %}

{% tab GAA Super Users %}
The minimum necessary rule requires that covered entities make reasonable efforts to limit access to protected health information to those in the workforce that need access based on their roles. Canvas allows you to limit access to established [Patient Groups](https://canvas-medical.zendesk.com/hc/en-us/articles/14701005818515-Patient-groups), ensuring that appropriate privacy restrictions are in place. Once the Patient Groups are defined in your admin settings, you can partner with your engineering team to leverage Protocols to programmatically add patients to the groups based on any patient attribute that is available to the Workflow Kit. 

{% include alert.html type="info" content="If you want to know what type of information is available to the Workflow Kit, replace ‘patient’ in the patient chart URL with ‘api/PatientProtocolInput'" %}

 

{% endtab %}

{% endtabs %}


<br>
<br>

### Routing work to the right team or individual



{% tabs RTI %}

{% tab RTI Developers %}
hi
{% endtab %}

{% tab RTI Super User %}
hello
{% endtab %}

{% endtabs %}


