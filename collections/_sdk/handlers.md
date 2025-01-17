---
title: "Handlers"
disable_anchorlist: true
---

The handlers module lets you define reactions to events.

Handlers respond to [Events](/sdk/events/) and return zero, one, or many [Effects](/sdk/effects/).

There are some special types of handlers, like [Protocols](/sdk/protocols/)
and [CronTasks](/sdk/handlers-crontask/). These offer a differentiated
interface for their particular use-cases. For example, CronTasks only ever
respond to the `CRON` event, require a schedule to be specified, and expect
the `execute` method to be implemented rather than `compute`.

<div class="handler-cards">
    <a href="/sdk/handlers-action-buttons/">
        <div class="handler-card">
            <div class="handler-card-header">
                <h2>Action Button</h2>
                <span>Add a button that executes your custom code when clicked.</span>
            </div>
            <img class="hover-primary" src="/assets/images/sdk/handlers/ActionButton.png" alt="Abridged source code of an action button implementation."/>
            <img class="hover-secondary" src="/assets/images/sdk/handlers/action-button-in-action.png" alt="Image of an action button in a note header."/>
        </div>
    </a>
    <a href="/sdk/handlers-applications/">
        <div class="handler-card">
            <div class="handler-card-header">
                <h2>Application</h2>
                <span>Launch an iframe when your icon is clicked in the app drawer.</span>
            </div>
            <img class="hover-primary" src="/assets/images/sdk/handlers/Application-cropped.png" alt="Abridged source code of an application implementation."/>
            <img class="hover-secondary" src="/assets/images/sdk/handlers/application-applied.png" alt="Image of application icons in the app drawer."/>
        </div>
    </a>
    <a href="/sdk/handlers-crontask/">
        <div class="handler-card">
            <div class="handler-card-header">
                <h2>Cron Task</h2>
                <span>Execute your code on a cron-like schedule.</span>
            </div>
            <img class="hover-primary" src="/assets/images/sdk/handlers/CronTask-cropped.png" alt="Abridged source code of an action button implementation."/>
            <img class="hover-secondary" src="/assets/images/sdk/handlers/mr-cron.png" alt="Picture of Mr. Cron, the little time monster that remembers which tasks should be executed at any given time."/>
        </div>
    </a>
    <a href="/sdk/handlers-basehandler/">
        <div class="handler-card">
            <div class="handler-card-header">
                <h2>Base Handler</h2>
                <span>Respond to events with your custom code.</span>
            </div>
            <img class="hover-primary" src="/assets/images/sdk/handlers/BaseHandler-cropped.png" alt="Abridged source code of a base handler implementation."/>
            <img class="hover-secondary" src="/assets/images/sdk/handlers/base-handler-can-lend-a-hand.png" alt="Stylized text that reads 'When X occurs, under Y conditions, I want Z to happen'."/>
        </div>
    </a>
</div>


<br/>
<br/>
<br/>
<br/>
