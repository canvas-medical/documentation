---
permalink: /product-updates/commands-module/
layout: betas
title: "Beta | Commands Module"
date: 2024-01-22
---

{% include alert.html type="warning" content= "Newly migrated commands will be released to everyone (GA) once thoroughly tested. If you would like early access, you can help beta test newly migrated commands by reaching out to our product team. Email us (product@canvasmedical.com) or reach out to your Customer Success Manager if interested."  %}


The commands module is a new, standardized framework for building commands in Canvas. In this new framework, commands are defined by two elements:

1. **The form:** This is what the user sees in the front-end. It consists of the fields that the user can fill out, the actions the user can take, and how the command is laid out on the screen.

2. **The event handler:** This is Python code that carries out actions depending on actions the user takes in the user-facing form.

{% include alert.html type="info" content="In this new framework, the data entered by the user into the user-facing form is completely separated from the clinical data that it might affect. Currently, the two are intertwined."  %}




## Expected benefits

Commands migrated to the new framework will function similarly if not identically (minus any confusing quirks or bugs!). However, the following are benefits that we anticipate with commands SDK:

- **Improved performance.** The framework dramatically simplifies the data model behind commands in Canvas, and we expect that this much simpler data model will have a noticeable impact on note load times.
- **Zero chance for data loss to occur.** The simpler data model allows information to be captured consistently at several layers in the application – starting with the user’s browser cache – which means that your data is persisted in some form as soon as it’s entered.
- **A fully-auditable command lifecycle.** The framework tracks all changes to a command over time, which will enable detailed auditing, as well as version control features in the future.
- **Consistent keyboard controls.** The framework uses built-in browser accessibility features to provide a first-class keyboard navigation experience across all commands.
- **Customizable commands.** The framework will enable customers to customize existing commands and create new ones by implementing a simple interface consisting of a form and one or more event handlers (roughly outlined above).
- **Editing committed commands.** In order to maintain a complete audit trail, current commands cannot be edited after they have been committed. Instead, they must be entered-in-error and re-created, which is cumbersome and often annoying. The framework abstracts this requirement away, allowing commands to be edited after they are committed by handling the enter-in-error and re-creation lifecycle seamlessly behind the scenes.

## Progress

<table border="1">
  <thead>
    <tr>
      <th>Command</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Plan</td>
      <td> <span class="tag-complete"> Released - GA </span> </td>
    </tr>
    <tr> 
      <td>HPI</td>
      <td><span class="tag-beta-testing"> Released - Beta </span> </td>
    </tr>
     <tr> 
      <td>Reason for Visit</td>
      <td><span class="tag-in-progress"> In Progress </span> </td>
    </tr>
     <tr> 
      <td>Stop Medication</td>
      <td><span class="tag-in-progress"> In Progress </span> </td>
    </tr>
     <tr> 
      <td>Questionnaire</td>
      <td><span class="tag-in-progress"> In Progress </span> </td>
    </tr>
     <tr> 
      <td>Assess</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Medication Statement</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Goal</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Update Goal</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Diagnose</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
    <tr> 
      <td>Task</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
    <tr> 
      <td>Prescribe</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
    <tr> 
      <td>Immunization Statement</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Lab Order</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Image</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Refer</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
     <tr> 
      <td>Refill</td>
      <td><span class="tag-next-up"> Next up </span> </td>
    </tr>
  </tbody>
</table>