---
title: "Action Center"
layout: documentation
---

### Introduction
The action center in Canvas is used to manage tasks and action items related to patient care. In the action center, your care team will interact with tasks, documents, messages, and other items requiring action or collaboration across your team. 

### Key objectives
In this article, you will learn how to:
- <a href="#my-tasks">Manage tasks</a> (link to section)
- Refill medications  (link to section)
- Review new lab results (link to section)
- Review new image results  (link to section)
- Review new consult reports  (link to section)
- Review uncategorized reports  (link to section)
- View new patient messages  (link to section)
- See other types of actions you can take from the Action Center  (link to section)

### My Tasks

Tasks in Canvas are to-do’s for the care team. They can be created programmatically with our Task Create API, or manually using the task command in the patient’s chart or through a prompt command using Canvas chat.


{:refdef: style="text-align: center;"}
![My tasks button](/assets/images/my-tasks-button-highlight.png){:width="100%"}
{: refdef}


Tasks are managed via the task list from the action center. The task list defaults to all opened tasks assigned to you or your teams.

{:refdef: style="text-align: center;"}
![My tasks list](/assets/images/my-tasks-list.png){:width="100%"}
{: refdef}

Tasks contain the following information:
- Task name
- Patient name
- Follow up due
- Activity
- Created
- Assignee
- Team
- Linked items
- Labels

The task list view can further be filtered by status, creator, or label and each column name can be clicked to sort the list by ascending/descending order. 

When interacting with Tasks, you can perform the following actions:
- Filter
- Sort
- Label
  - Associate
  - Create
  - Edit
- Comment
- Reassign
- Complete

{:refdef: style="text-align: center;"}
![My tasks](/assets/images/task-list.gif){:width="100%"}
{: refdef}

<details>
  <summary>Filter Tasks</summary>
<pre>

- Navigate to the Task header where you can filter tasks by the following filters:
 - <strong>Assignee:</strong> Defaults to "Me or my teams"
   - Other options include:
     - Other staff
     - Other teams
     - Specific individuals
 - <strong>Status:</strong> Defaults to Open
   - Users can multi-select from open, completed, and closed
 - <strong>Creator:</strong> Defaults to Any
   - Users can select specific individuals
  - <strong>Label:</strong> Defaults to Any
    - Users can multi-select from any label previously created or No labels

</pre>

{% include alert.html type="info" content="When using the search function of the Label filter to multi-select labels you will have to scroll and click the check boxes instead of searching and pressing enter to make your selections.  However, at present you can use the search function and scroll/click when searching for just one label." %}
</details>

<details>
  <summary>Sort Tasks</summary>
<pre>

- Navigate to the Task List which sorts to oldest task that needs completion
- Locate the task list column headers which include the following:
  - <strong>Task</strong>
  - <strong>Patient</strong>
  - <strong>Follow-up due</strong>
  - <strong>Activity</strong>
  - <strong>Created</strong>
  - <strong>Assignee</strong>
  - <strong>Team</strong>
  - <strong>Label</strong>
- Click on the desired column heading
  - <strong>Click once:</strong> Sort in Ascending
  - <strong>Click twice:</strong> Sort in Descending

</pre>
</details>

<details>
  <summary>Label a Task</summary>
<pre>

- Navigate to the desired task from the Task List
- Click on the underlined <strong>No labels</strong> within the Labels column or the ![button](/assets/images/plus-button.png) icon next to an already existing label
- Search for the appropriate label
  - Free text or scroll through menu
- Select the appropriate label(s) from the drop-down 

</pre>
</details>


### Refill requests
### New labs
### New imaging
### New consult reports
### New uncategorized reports
### Patient messages

[FAQ’s](#FAQ) 



