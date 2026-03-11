---
title: "CreateCCDA"
slug: "effect-create-ccda-export"
excerpt: "Effect to create a C-CDA (Consolidated Clinical Document Architecture) document for a patient."
hidden: false
---

The `CreateCCDA` effect creates a C-CDA document for a patient with the provided XML content. This effect allows plugins to store C-CDA XML documents, which can be used for clinical document exchange, patient summaries, or referrals.

This effect stores a C-CDA document, generating or otherwise sourcing that document is the responsibility of the plugin.

## Attributes

| Name           | Type           | Required | Description                                                                 |
|----------------|----------------|----------|-----------------------------------------------------------------------------|
| `patient_id`   | `str`          | Yes      | The patient's key (UUID).                                                   |
| `content`      | `str`          | Yes      | The C-CDA XML content as a string. Must be valid XML.                        |
| `document_type` | `DocumentType` | No       | Type of C-CDA document. Defaults to `DocumentType.CCD`.                      |

## DocumentType Enum

| Value      | Description                                      |
|------------|--------------------------------------------------|
| `CCD`      | Continuity of Care Document (default)            |
| `REFERRAL` | Referral document                                |

## Validation

The effect performs the following validations before execution:

- **Patient Exists**: Verifies that a patient with the given `patient_id` exists in the system.
- **Valid XML**: Validates that the `content` field contains well-formed XML. Malformed XML will result in a validation error.
- **Required Fields**: Both `patient_id` and `content` must be non-empty strings.

## Example Usage

### Basic CCD Creation

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.ccda import CreateCCDA, DocumentType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_UPDATED)]

    def compute(self) -> list[Effect]:
        # Sample C-CDA XML content
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

        effect = CreateCCDA(
            patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            content=ccda_xml,
            document_type=DocumentType.CCD,
        )

        return [effect.apply()]
```

### Creating a Referral Document

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.ccda import CreateCCDA, DocumentType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_UPDATED)]

    def compute(self) -> list[Effect]:
        referral_xml_content = "<ClinicalDocument>...</ClinicalDocument>"

        effect = CreateCCDA(
            patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            content=referral_xml_content,
            document_type=DocumentType.REFERRAL,
        )

        return [effect.apply()]
```

### Using Default Document Type

When `document_type` is not specified, it defaults to `CCD`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.ccda import CreateCCDA
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.PATIENT_UPDATED)]

    def compute(self) -> list[Effect]:
        ccda_xml = "<ClinicalDocument>...</ClinicalDocument>"

        effect = CreateCCDA(
            patient_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            content=ccda_xml,
        )

        # document_type defaults to DocumentType.CCD
        return [effect.apply()]
```

## Use Cases

- **Clinical Document Exchange**: Generate C-CDAs for sharing patient information with external systems or providers.
- **Patient Summaries**: Create Continuity of Care Documents containing a patient's clinical summary.
- **Referral Documentation**: Generate referral documents when referring patients to specialists.
- **Integration with External Systems**: Produce standardized C-CDA documents for healthcare interoperability.

## Notes

- The C-CDA XML content is stored as a file on the patient's record.
- The created document can be accessed via the FHIR DocumentReference endpoint.

<br/>
<br/>
<br/>
