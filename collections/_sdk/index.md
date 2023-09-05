---
slug: /
title: "SDK Overview"
layout: sdklandingpage
---


## The Canvas Workflow Kit

The Canvas Workflow Kit was built to support clinical quality measures. It is extremely powerful in that regard, but effective care modeling requires much more control and customization than it allows. We have extended it to create additional interventions, beyond the original recommendations, but the triggers are still limited to patient changes. 
<br>
<br>
## The Canvas SDK

It was evident in partnering with our customers in their care modeling journeys that a true SDK was needed to unlock critical use cases. There are many advantages to the new architecture, including but not limited to:

* The Canvas SDK will leverage full python packages, instead of the single sandboxed python files used today, supporting a better developer experience
* Plugins will expand coverage of the application, extending beyond patient events. You will be able to respond to user based events, application events, cron-based events, etc. 
* The Commands Module will improve performance and allow for the customization of commands to support your care model. 

Check out our documentation [here](https://canvas-medical.github.io/canvas-core/quickstart/plugins.html). We are working on integrating it into this site. 

{% include alert.html type="info" content=" <b>Plugins are currently in beta.</b> If you are interested in participating, please reach out to product@canvasmedical.com." %}
<br>
## Which should I use?

We are working to build the existing functionality into the new structure. If you have a new workflow you would like to support, we would love to hear about it and determine if plugins are the right choice. It will be some time before plugins can support the traditional clinical quality measure structure. You should continue to leverage protocols for creating clinical recommendations based on patient data. 

Part of our project will be to determine how to migrate all of your existing protocols to the new structure. More to come when ready. 







