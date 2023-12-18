---
title: More PDF documents available through DocumentReference
date: 2023-12-11
tags: api
---
Customers have expressed a need to access more PDFs from Canvas via API, in order to share these with external parties or in patient-facing experience. As a result we have significantly expanded the scope of DocumentReference, to include the following documents:

- All PDFs added via Data Integration that have been parsed ("parsed" means they have been attached to a patient and tagged with required metadata like document type). Some examples of these PDFs include "Uncategorized clinical documents", "Consult report, "Advanced directive" and more.
- PDFs of chart notes. A version of the note PDF is saved every time a note is locked, and all versions are available via the API.
