---
slug: /
title: "The Canvas SDK"
layout: sdk
---

## Get started

Here are some step-by-step guides to get you started:


<div class="sdk-card-list">
    <a href="/guides/your-first-plugin">
        <div class="sdk-card">
            <span class="cardHeading">Your First Plugin</span>
            <p>This guide steps you through installing the Canvas SDK, creating a plugin, and deploying it to a Canvas instance.</p>
        </div>
    </a>
    <a href="/guides/creating-webhooks-with-the-canvas-sdk">
        <div class="sdk-card">
            <span class="cardHeading">Creating Webhooks</span>
            <p>Make automatic API requests based on Canvas events</p>
        </div>
    </a>
    <a href="/guides/customize-search-results">
        <div class="sdk-card">
            <span class="cardHeading">Customize Search Results</span>
            <p>Add your own logic to surface the right options with the appropriate context</p>
        </div>
    </a>
</div>
And here are some other [guides](/guides)

## What is the Canvas SDK?

The Canvas SDK is your toolkit for customizing workflows natively across the full Canvas platform: scheduling, charting, billing, and more. It is a [python package](https://pypi.org/project/canvas/) used to develop and deploy plugins, which then run in this [open source runtime environment](https://github.com/canvas-medical/canvas-plugins) on your Canvas instance.

Plugins, the custom packages you author with the Canvas SDK, run in a sandboxed process directly on the Canvas instance. The Canvas application emits many [events](/sdk/events) at runtime, which you can choose to respond to and produce some number of [effects](/sdk/effects). These effects are then interpreted by the Canvas application, which applies the changes your plugin returned. Events are accompanied by contextual information, and your plugin has access to additional information through the [data module](/sdk/data), which exposes a subset of the Canvas application database through a series of [Django ORM classes](https://docs.djangoproject.com/en/5.1/ref/models/querysets/) backed by read-only views.

<p>
  <object alt="Diagram of the Canvas Plugins Runtime Environment" type="image/svg+xml" data="/assets/images/sdk/canvas_plugins_runtime_diagram.svg" style="width: 90%;"></object>
</p>

## Where can I get additional help?

Our [open-source GitHub repo](https://github.com/canvas-medical/canvas-plugins) has a [discussions](https://github.com/canvas-medical/canvas-plugins/discussions) section, where you can request help or suggest improvements. We also welcome [issue reports](https://github.com/canvas-medical/canvas-plugins/issues) and [pull requests](https://github.com/canvas-medical/canvas-plugins/pulls)!

Ready? [Get started!](#get-started)

<br/>
<br/>
<br/>
