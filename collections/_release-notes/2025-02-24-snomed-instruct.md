---
title: Support for SNOMED and Unstructured Codes in Instruct Commands
layout: productupdates
tags: plugins sdk breaking-change
date: 2025-02-24
---
Instruct commands can now be originated using SNOMED or unstructured codes. This work includes a **breaking change**. The instruction field has been renamed to `coding`. Please update implementations accordingly. [Read more.](/sdk/commands/#instruct)
