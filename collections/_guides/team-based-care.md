---
title: "Team Based Care"
guide_for:
 - /api/group/
 - /api/careteam/
 - /documentation/roles/
 - /documenation/teams/
 - /documentation/permissions/
 - /documentation/care-team-roles/
 - /documentation/patient-groups/

---


Since the 1960s, teamwork has emerged as the preferred approach to collaboration in healthcare and is widely acknowledged for its ability to enhance healthcare quality. Studies show that medical care that involves interdisciplinary cooperation is linked to improved access, higher patient safety, reduced hospitalization rates, and fewer complications and medical errors. Medical professionals also experience significant advantages, such as increased job satisfaction and a decreased risk of burnout.

Although the benefits are well established, forming the right team to support your care model requires a careful balance between productivity and experience levels to ensure optimal care without compromising safety. The Canvas platform was purpose built to make this easier, supporting efficient team-based delivery through the following features and workflows.
<br>
<br>
* * *
## What you'll learn
In this guide, you will learn how to do the following:
1. Define the roles and responsibilities for your care team
2. Grant appropriate access levels
3. Route work to the right team or individual
<br><br>

* * *
### 1. Define roles and responsibilities 

Once you have determined your appropriate staffing model and hired a team, you can set up Roles, Teams, and Care Teams to ensure everyone can collaborate effectively. 
<br>
- [Roles](/documentation/roles/) : are configurable in Canvas and can drive a default permission set through Canvas managed [auth groups](/documentation/permissions/#model-permissions). <br>
- [Teams](/documentation/teams/) are used to group work. By assigning responsibilities to teams, you can drive how automated tasks in Canvas are assigned. For instance, you may want all delegated referrals to go to a care coordination team.<br>
- [Care Team Roles](/documentation/care-team-roles/) are used to define the role an individual plays in a patient’s care. Once created you can assign staff to patients with a care team role. <br>

Teams and care teams are available via the FHIR API and can be leveraged in protocols. Make sure to coordinate across teams to ensure they are set up with the appropriate code systems to be leveraged in your custom workflows.

Teams in Canvas map to the [FHIR Group](/api/group/) resource. You can do a FHIR Group Search to determine the Group ID associated with each team. The GroupID is most commonly leveraged when assigning ownership of tasks. 

Our [FHIR CareTeam](/api/careteam/) resource allows you to read a patients care team, assign practitioners to patients with care team roles using the update endpoint (acting as an upsert), and search for care team participation. Participation is often leveraged to then drive logic in your other workflows, including messaging and scheduling. 
<br>
<br>

* * *
### 2. Grant appropriate access levels

The minimum necessary rule requires that covered entities make reasonable efforts to limit access to protected health information to those in the workforce that need access based on their roles.

Permissions that control what a user can do in Canvas are assigned through [roles](/permissions/#default-permissions-based-on-role). 

Canvas also allows you to limit access to subsets of the population using established [patient groups](/documentation/patient-groups/). Once the patient groups are defined in your admin settings, you can partner with your engineering team to leverage protocols to programmatically add patients to the groups based on any patient attribute that is available to the Workflow Kit. 

{% include alert.html type="info" content="If you want to know what type of information is available to the Workflow Kit, replace ‘patient’ in the patient chart URL with ‘api/PatientProtocolInput'" %}
<br>
To add or remove a patient from a group in Canvas, we have made two helper functions that you can pass to the `set_updates` function. Both groups require the patient's key and the group's UUID. The group UUID can be found using a [Group Search](/api/group/#search). 

**ensure_patient_in_group(patient_key: str, group_externally_exposable_id: str)**
    - Creates a message to add a patient to a patient group if they are not already in that group.
**ensure_patient_not_in_group(patient_key: str, group_externally_exposable_id: str)**
    - Creates a message that removes a patient from a patient group if they are currently in the group.

The protocol below groups patients based on having a consent on file.

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

If you cannot use one of the existing data points within a patient's profile, writing identifiers using the [FHIR Patient Create](/api/patient/) endpoint may be a good option. Using this attribute allows you to leverage external data (like payer program enrollments) to define your groups.


 

<br>
<br>

* * *
### 3. Routing work to the right team or individual

You’ll need to determine how you’ll leverage your care team, what types of tasks should be delegated, and to whom they should be assigned. Configuring [teams](/documentation/teams/) allows you to assign the Canvas automated tasks to a team; however, the way we’ve grouped responsibilities may not be granular enough for you. You can use Protocols to re-route tasks based on their titles. Given a known task title, you can reassign to an individual or team, and also add labels. 

Use the following framework to determine how our automated tasks can be rerouted to create efficiencies. <br><br>
When <b>X</b> occurs: When a task is created <br>
Under <b>Y</b> conditions: `targeted_task_title ` = Y <br>
I want <b>Z</b> to happen: Assign to `group_name` or `pracitioner` and add `label(s)` <br>

The example below looks for the task name referral_task_title = "Refer patient to Psychiatry (TBD)", updates the team assignment, and adds an `internal referral` label. 

``` python
import requests
from canvas_workflow_kit.protocol import ClinicalQualityMeasure, ProtocolResult
from canvas_workflow_kit.constants import CHANGE_TYPE


class BehvaioralReferralTaskUpdate(ClinicalQualityMeasure):

    class Meta:
        title = "Behavioral Referral Task Update"
        version = "2023-v01"
        description = "This protocol updates the label and team for a task created "
        information = "https://link_to_protocol_information"
        types = ["Task"]
        compute_on_change_types = [CHANGE_TYPE.TASK]
        authors = ["Canvas Example Medical Association (CEMA)"]
        notification_only = True

    token = None
    task_id = None

    # TODO: These are hard coded variables that can be updated based on your needs

    # The group ID you can retreive from a FHIR Group Search call
    group_fhir_id = "Group/e3fabb40-1ccc-4bb4-9e64-e813f27bf2e2"

    # This is the name of the Team/Group you want to use when re-assigning a task
    group_name = "Behavioral Health Coordinators"

    # This is the label you want to add to the task we are updating
    task_label = "Internal Referral"

    # This is the exact title of the Task we are trying to find and update
    targeted_task_title = "Refer patient to Psychiatry (TBD)"

    ##################### HELPER FUNCTIONS ##################################

    def get_fhir_api_token(self):
        """Given the Client ID and Client Secret for authentication to FHIR,
        return a bearer token"""

        grant_type = "client_credentials"
        client_id = self.settings.CLIENT_ID
        client_secret = self.settings.CLIENT_SECRET

        token_response = requests.request(
            "POST",
            f"https://{self.settings.INSTANCE_NAME}.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}",
        )

        if token_response.status_code != 200:
            raise Exception('Unable to get a valid FHIR bearer token')

        return token_response.json().get("access_token")

    def get_fhir_task(self):
        """Given a Task ID, request a FHIR Task Resource"""

        if not self.token or not self.task_id:
            return None

        response = requests.get(
            (
                f"https://fhir-{self.settings.INSTANCE_NAME}.canvasmedical.com/"
                f"Task?identifier={self.task_id}"
            ),
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )

        if response.status_code != 200:
            raise Exception('Failed to get FHIR Task')

        resources = response.json().get("entry", [])
        if len(resources) == 0:
            return None

        return resources[0].get("resource")

    def update_fhir_task(self, task):
        """Given a Task ID and Task Resource perform a FHIR Task Update"""

        if not self.token or not self.task_id:
            return None

        response = requests.put(
            (
                f"https://fhir-{self.settings.INSTANCE_NAME}.canvasmedical.com/"
                f"Task/{self.task_id}"
            ),
            json=task,
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

        if response.status_code != 200:
            raise Exception(f"Failed to mark Task as completed with {response.status_code} and payload {payload}")

    def edit_task(self, task):
        """Given a Task update the payload to supply a Group extension and label"""

        # Add an extension for Group assignee in the task payload
        new_extension = {
            "url": "http://schemas.canvasmedical.com/fhir/extensions/task-group",
            "valueReference": {
                "reference": self.group_fhir_id,
                "display": self.group_name,
            },
        }
        extension = [*task.get("extension", []), new_extension]

        # add label to the task payload
        new_input = {
            "type": {"text": "label"},
            "valueString": self.task_label,
        }
        input = [*task.get("input", []), new_input]

        new_task = task | {"extension": extension, "input": input}
        return {k: v for k, v in new_task.items() if k != "note"}

    def is_targeted_task(self):
        """Returns true if the task has the title we are targetting """

        return (
            len(
                self.patient.tasks.filter(
                    externallyExposableId=self.task_id, title=self.targeted_task_title
                )
            )
            == 1
        )

    ##################### END HELPER FUNCTIONS ##################################

    def compute_results(self):
        """ This is the main function that will check if the task that triggered this protocol
        is the one that we are hoping to update. If it is, we fetch the task payload from FHIR
        and update the assignee and label
        """

        # First get a FHIR API Token
        if not (token := self.get_fhir_api_token()):
            return result
        self.token = token

        result = ProtocolResult()

        field_changes = self.field_changes or {}
        self.task_id = str(field_changes.get("external_id", ""))
        created = field_changes.get("created") == True
        if not created or not self.task_id or not self.is_targeted_task():
            return result

        if not (task := self.get_fhir_task()):
            return result

        self.update_fhir_task(self.edit_task(task))

        return result

```






