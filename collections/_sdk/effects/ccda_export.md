---
title: "CreateCCDAExport"
slug: "effect-create-ccda-export"
excerpt: "Effect to create a CCDA (Consolidated Clinical Document Architecture) document for a patient."
hidden: false
---

Creates a CCDA document for a patient with the provided XML content. This effect allows plugins to generate and store CCDA XML documents, which can be used for clinical document exchange, patient summaries, or referrals.

## Attributes

| Name           | Type           | Required | Description                                                                 |
|----------------|----------------|----------|-----------------------------------------------------------------------------|
| `patient_id`   | `str`          | Yes      | The patient's key (UUID).                                                   |
| `content`      | `str`          | Yes      | The CCDA XML content as a string. Must be valid XML.                        |
| `document_type`| `DocumentType` | No       | Type of CCDA document. Defaults to `DocumentType.CCD`.                      |

## DocumentType Enum

| Value      | Description                                      |
|------------|--------------------------------------------------|
| `CCD`      | Continuity of Care Document (default)            |
| `Referral` | Referral document                                |

## Validation

The effect performs the following validations before execution:

- **Patient Exists**: Verifies that a patient with the given `patient_id` exists in the system.
- **Valid XML**: Validates that the `content` field contains well-formed XML. Malformed XML will result in a validation error.
- **Required Fields**: Both `patient_id` and `content` must be non-empty strings.

## Example Usage

### Basic CCD Creation

```python
from canvas_sdk.effects.ccda import CreateCCDAExport, DocumentType

# Sample CCDA XML content
ccda_xml = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
    <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
    <id root="document-id"/>
    <code code="34133-9" displayName="Summarization of Episode Note"
          codeSystem="2.16.840.1.113883.6.1"/>
    <title>Patient Summary</title>
    <effectiveTime value="20240101120000"/>
    <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
    <languageCode code="en-US"/>
</ClinicalDocument>"""

effect = CreateCCDAExport(
    patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    content=ccda_xml,
    document_type=DocumentType.CCD
)

return [effect.apply()]
```

### Creating a Referral Document

```python
from canvas_sdk.effects.ccda import CreateCCDAExport, DocumentType

effect = CreateCCDAExport(
    patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    content=referral_xml_content,
    document_type=DocumentType.REFERRAL
)

return [effect.apply()]
```

### Using Default Document Type

When `document_type` is not specified, it defaults to `CCD`:

```python
from canvas_sdk.effects.ccda import CreateCCDAExport

effect = CreateCCDAExport(
    patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    content=ccda_xml
)

# document_type will be "CCD"
return [effect.apply()]
```

## Use Cases

- **Clinical Document Exchange**: Generate CCDAs for sharing patient information with external systems or providers.
- **Patient Summaries**: Create Continuity of Care Documents containing a patient's clinical summary.
- **Referral Documentation**: Generate referral documents when referring patients to specialists.
- **Integration with External Systems**: Produce standardized CCDA documents for healthcare interoperability.

## Notes

- The created CCDA is stored and associated with the patient record.

<br/>
<br/>
<br/>
