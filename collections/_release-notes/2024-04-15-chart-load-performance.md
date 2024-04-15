---
title: Improves Performance Loading Charts and Inserting/Deleting Notes
date: 2024-04-15
layout: productupdates
tags: ui 
---
We've optimized our notes query by splitting it into two separate queries: one for retrieving static command schema data and another for dynamic commands. This enhancement allows us to cache the static data, resulting in faster load times. 