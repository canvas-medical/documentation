---
title: "Accessing Resource Attachment Files"
layout: apipage
---

Several Canvas FHIR resources include a `url` attribute that points to an attachment file stored in S3. When you read or search these resources, the `url` value will be a `/files/` path on the Canvas FHIR server. Fetching that URL requires a **Bearer token** and returns a **302 redirect** to a pre-signed S3 URL.

## Endpoints that return file URLs

| Resource | URL pattern |
|---|---|
| [Consent](/api/consent) | `GET /Consent/{id}/files/sourceAttachment` |
| [DiagnosticReport](/api/diagnosticreport) | `GET /DiagnosticReport/{id}/files/presentedForm` |
| [DocumentReference](/api/documentreference) | `GET /DocumentReference/{id}/files/content` |
| [Media](/api/media) | `GET /Media/{id}/files/content` |
| [Patient](/api/patient) | `GET /Patient/{id}/files/photo` |
| [Practitioner](/api/practitioner) | `GET /Practitioner/{id}/files/signature` |

## The redirect and the dual-auth problem

When you make an authenticated `GET` request to one of these `/files/` URLs, the server validates your Bearer token and responds with a **redirect** and will contain a URL in the response header. If the URL is to S3 it already contains authentication credentials in its query parameters and **expires after 10 minutes**.

Most HTTP clients (including `requests` in Python and `curl` by default) automatically follow redirects **and forward all headers**, including `Authorization`. When S3 receives both the pre-signed query parameters *and* an `Authorization` header, it rejects the request with a dual-auth error:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error>
  <Code>InvalidArgument</Code>
  <Message>Only one auth mechanism allowed; only the X-Amz-Algorithm
  query parameter or the Authorization header should be specified,
  not both.</Message>
  <ArgumentName>Authorization</ArgumentName>
  <ArgumentValue>Bearer xxxxxxxxx</ArgumentValue>
  <RequestId>...</RequestId>
  <HostId>...</HostId>
</Error>
```

The solution is to **not follow the redirect automatically** so you can strip the `Authorization` header before requesting the pre-signed S3 URL.

## Python example

Use `allow_redirects=False` to capture the 302 response, then make a second request to the pre-signed URL without the `Authorization` header:

```python
import requests

base_url = "https://fumage-{instance}.canvasmedical.com"
token = "your_bearer_token"

# Step 1: Request the file URL without following the redirect
file_url = f"{base_url}/DocumentReference/abc123/files/content"
response = requests.get(
    file_url,
    headers={"Authorization": f"Bearer {token}"},
    allow_redirects=False,
)

# Step 2: Get the pre-signed S3 URL from the Location header
presigned_url = response.headers["Location"]

# Step 3: Download the file — no Authorization header needed
file_response = requests.get(presigned_url)

with open("downloaded_file.pdf", "wb") as f:
    f.write(file_response.content)
```

## curl example

With `curl`, use `-s` to suppress the progress bar and capture the redirect `Location` header, then fetch the pre-signed URL separately:

```bash
# Step 1: Get the pre-signed URL from the redirect
PRESIGNED_URL=$(curl -s -o /dev/null -w '%{redirect_url}' \
  -H "Authorization: Bearer $TOKEN" \
  "https://fumage-{instance}.canvasmedical.com/DocumentReference/abc123/files/content")

# Step 2: Download the file
curl -o downloaded_file.pdf "$PRESIGNED_URL"
```

## Getting the filename from resource metadata

The pre-signed S3 URL does not contain the original filename. To determine the filename or content type, read it from the resource's attributes before downloading. For example:

- **DocumentReference**: `content[0].attachment.title` and `content[0].attachment.contentType`
- **Media**: `content.title` and `content.contentType`
- **Consent**: `sourceAttachment.title` and `sourceAttachment.contentType`
- **DiagnosticReport**: `presentedForm[0].contentType`
- **Patient**: `photo[0].contentType`
- **Practitioner**: `photo[0].contentType`
