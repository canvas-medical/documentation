---
title: Ensures Associated DocumentReference is Created for Lab Reports
date: 2024-06-03
layout: productupdates
tags: bugfix api
---
This work addresses an issue that delayed and/or sporadically prevented the creation of a documentreference resource when adding lab reports via Data Integration beginning in April. We will backfill the missing documents over the next week to ensure all lab reports are available via the FHIR API. 