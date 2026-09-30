---
title: "Receipt"
slug: "data-receipt"
excerpt: "A read-only, Canvas-generated payment receipt, one per payment collection, with a presigned URL to its PDF."
hidden: false
---

# Receipt

The `Receipt` model represents the single canonical payment receipt Canvas generates for a payment collection. It is read-only: Canvas creates one receipt per [PaymentCollection](/sdk/data-posting/#paymentcollection), and the model exposes that existing receipt PDF through a presigned URL. It does not create, edit, or regenerate receipts.

## Basic Usage

```python
from canvas_sdk.v1.data import Receipt

receipt = Receipt.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
```

Each receipt belongs to one [PaymentCollection](/sdk/data-posting/#paymentcollection), and you can reach it from the collection through the one-to-one reverse accessor:

```python
from canvas_sdk.v1.data import PaymentCollection

collection = PaymentCollection.objects.get(id="f47ac10b-58cc-4372-a567-0e02b2c3d479")
receipt = collection.receipt  # the one-to-one Receipt; raises if the collection has none
```

## Finding a patient's receipts

A patient-portal plugin should reach only the authenticated patient's receipts. Walk there from the patient's own payments rather than querying `Receipt` directly.

Each of the patient's payments (`patient.payments`, a [BulkPatientPosting](/sdk/data-posting/#bulkpatientposting) queryset) belongs to one `payment_collection`, which has at most one receipt. A collection may not have one yet, so the code must handle its absence.

```python
from canvas_sdk.v1.data import Patient

patient = Patient.objects.get(id="b80b1cdc2e6a4aca90ccebc02e683f35")

receipts = []
for payment in patient.payments.select_related("payment_collection__receipt"):
    # The reverse accessor raises when a collection has no receipt, so default to None.
    receipt = getattr(payment.payment_collection, "receipt", None)
    # A patient-portal plugin must not surface a deleted or entered-in-error receipt.
    # The reverse accessor bypasses the default deleted=False filter, so screen it here.
    if receipt is None or receipt.deleted or receipt.entered_in_error_id is not None:
        continue
    receipts.append(receipt)
```

{% include alert.html type="warning" content="Canvas does not set a committer on receipts, so <code>Receipt.objects.committed()</code> returns no receipts. Filter on <code>entered_in_error</code> instead, as above." %}

## Accessing the receipt PDF

The `receipt_url` property returns a presigned S3 URL for the receipt PDF. The URL is valid for one hour and is regenerated on each access, so fetch it at render time rather than persisting or caching it. It returns `None` when the receipt has no PDF. The `receipt` field itself holds the stored file path, not a URL, so use `receipt_url` to link a patient to their PDF.

```python
from canvas_sdk.v1.data import Receipt

receipt = Receipt.objects.get(id="d2194110-5c9a-4842-8733-ef09ea5ead11")
url = receipt.receipt_url  # presigned S3 URL (valid for 1 hour), or None
```

## Attributes

### Receipt

| Field Name                            | Type                                                        |
|---------------------------------------|-------------------------------------------------------------|
| id                                    | UUID                                                        |
| dbid                                  | Integer                                                     |
| created                               | DateTime                                                    |
| modified                              | DateTime                                                    |
| originator                            | [CanvasUser](/sdk/data-canvasuser/)                         |
| committer                             | [CanvasUser](/sdk/data-canvasuser/)                         |
| entered\_in\_error                    | [CanvasUser](/sdk/data-canvasuser/)                         |
| deleted                               | Boolean                                                     |
| payment\_collection                   | [PaymentCollection](/sdk/data-posting/#paymentcollection)   |
| account\_balance\_before\_collection  | Decimal                                                     |
| account\_balance\_after\_collection   | Decimal                                                     |
| discount                              | Decimal                                                     |
| template                              | String                                                      |
| receipt                               | String                                                      |
| receipt\_url                          | String (property) (property): presigned S3 URL, or None               |

`account_balance_before_collection` and `account_balance_after_collection` are point-in-time snapshots of the patient's account balance captured when the receipt was generated, not live balances. `discount` is the discount amount snapshotted on the receipt, and is `0.00` when no discount was applied. `template` has a value only on legacy per-claim receipts generated before the current revenue schema. On other receipts it is usually `None`, so check `if receipt.template:` rather than comparing it to an empty string.

**Computed Properties**:

* `total_posted_amount`: Total posted with the payment collection: the sum of payments and write-off adjustments across its active postings.
* `copay_amount`: The amount posted as copays on the payment collection.

## See also

* [Posting](/sdk/data-posting/): `PaymentCollection`, `BulkPatientPosting`, and `PatientPosting`.
* [Patient](/sdk/data-patient/#patient): the starting point for a patient-scoped receipt walk.
* [DocumentReference](/sdk/data-document-reference/): the other model that serves a stored file through a presigned URL.
