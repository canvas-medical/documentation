---
title: "Task Update"
slug: "task-update"
excerpt: "Update a task that already exists in Canvas"
hidden: false
createdAt: "2022-06-27T14:24:21.127Z"
updatedAt: "2022-07-28T00:18:07.836Z"
---
This endpoint is identical to the [Task Create](ref:task-create) endpoint with the exception of passing the Task id as a path parameter. 

**Note: ** 

- Any note comments included in the Update message body will not be checked if they already exist in Canvas. Canvas will always assume each Note is an addition to the Task Comments.
- Omitting the `group extension` and `authoredOn` in an update body does not delete the contents of that field. They remain set to the last value they were assigned. 
- Omitting the `description`, `owner`, `restriction` and `input` attributes will delete the contents of the field in the Canvas database. In order to have a Task keep the values in these fields after an update, they must be included.