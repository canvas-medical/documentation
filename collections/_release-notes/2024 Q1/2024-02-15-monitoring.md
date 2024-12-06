---
title: Adds Monitoring
layout: productupdates
tags: ui 
date: 2024-02-15
---
- We added additional tags to our web worker metrics to give us visibility into uneven usage caused by (for example) session stickiness at the load balancer level.
- We added additional metadata to error reports when individual commands or notes crash to improve our ability to stay on top of those errors.
- We improved release notation within our internal systems, allowing support staff and engineers to better see if regressions are caused by a release in the time immediately following that release.
- We increased the accuracy of our request/response durations by accounting for time spent doing request logging.
- We added the ability to track the request backlog for all web workers, allowing us to track the size of the request queue over time.
