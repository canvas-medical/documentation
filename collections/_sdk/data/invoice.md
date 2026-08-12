---
title: "Invoice"
slug: "data-invoice"
excerpt: "A patient statement generated for a patient or guarantor, with its total, delivery method, and status."
hidden: false
---

## Introduction

The `Invoice` model represents a statement generated for a patient or their guarantor — who it was addressed to, what it totals, how it was sent, and where it stands. It is a read-only data model.

Invoices are produced by Canvas billing workflows rather than by plugins: automated statement runs, batch runs, and one-off statements each record their origin in `workflow`.

{% include alert.html type="info" content="Invoice records have no UUID <code>id</code> — they are identified by their integer <code>dbid</code>." %}

## Basic Usage

```python
from canvas_sdk.v1.data import Invoice

invoice = Invoice.objects.get(dbid=42)
```

If you have a `Patient` object, the statements addressed to them are available through the `invoices` reverse relation:

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
invoices = patient.invoices.all()
```

A [Claim](/sdk/data-claim/#claim) points at the most recent statement it appeared on:

```python
from canvas_sdk.v1.data import Claim

claim = Claim.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
invoice = claim.latest_invoice
```

## Filtering

```python
from canvas_sdk.v1.data.invoice import Invoice, InvoiceStatus, InvoiceWorkflow

# Active statements only
active = Invoice.objects.filter(status=InvoiceStatus.ACTIVE)

# Statements a staff member generated one at a time, rather than by a batch or automated run
adhoc = Invoice.objects.filter(workflow=InvoiceWorkflow.ADHOC)
```

`Invoice` is addressed through `recipient` rather than a `patient` field, so filter on `recipient` to scope to one patient:

```python
from canvas_sdk.v1.data import Invoice

invoices = Invoice.objects.filter(recipient__id="1eed3ea2a8d546a1b681a2a45de1d790")
```

## Accessing the statement PDF

`Invoice` holds the statement's amounts and delivery details, not the rendered file. Canvas attaches the PDF to a [DocumentReference](/sdk/data-document-reference/#the-related-object), which you reach by resolving the [ContentType](/sdk/data-content-type/) for the invoice and matching `object_id` against the invoice's `dbid`:

```python
from canvas_sdk.v1.data import ContentType, DocumentReference, Invoice

invoice = Invoice.objects.get(dbid=42)

content_type = ContentType.objects.filter(
    app_label="quality_and_revenue", model="invoicefull"
).first()

document = DocumentReference.objects.filter(
    content_type=content_type, object_id=invoice.dbid
).first()

url = document.document_url if document else None
```

## Attributes

### Invoice

| Field Name     | Type                                              |
|----------------|---------------------------------------------------|
| dbid           | Integer                                           |
| originator     | [CanvasUser](/sdk/data-canvasuser/)               |
| recipient      | [Patient](/sdk/data-patient/#patient)             |
| recipient_type | [InvoiceRecipients](#invoicerecipients)           |
| total_amount   | Decimal                                           |
| status         | [InvoiceStatus](#invoicestatus)                   |
| workflow       | [InvoiceWorkflow](#invoiceworkflow)               |
| error_message  | String                                            |
| sent_mean      | [InvoiceSentMeans](#invoicesentmeans)             |

`error_message` carries the reason a statement failed to go out, and is empty for statements that did not fail.

## Enumeration types

### InvoiceRecipients

Who the statement was addressed to.

| Value       | Label     |
|-------------|-----------|
| patient     | Patient   |
| guarantor   | Guarantor |

### InvoiceStatus

| Value    | Label    |
|----------|----------|
| active   | Active   |
| error    | Error    |
| archived | Archived |

### InvoiceWorkflow

How the statement was produced.

| Value     | Label     |
|-----------|-----------|
| automated | Automated |
| adhoc     | Adhoc     |
| batch     | Batch     |

### InvoiceSentMeans

| Value  | Label  |
|--------|--------|
| mail   | Mail   |
| e-mail | E-mail |
