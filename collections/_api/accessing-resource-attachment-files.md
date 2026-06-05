---
title: "Accessing Resource Attachment Files"
layout: apipage
---

Several Canvas FHIR resources include a `url` attribute that points to an attachment file stored in S3. When you read or search these resources, the `url` value will be a `/files/` path on the Canvas FHIR server. Fetching that URL requires a **Bearer token** and returns a **redirect** to a pre-signed S3 URL that **expires after 10 minutes**.

There are two ways to retrieve the file, depending on whether you want the raw file content or the pre-signed URL itself.

## Endpoints that return file URLs

| Resource | URL pattern |
|---|---|
| [Consent](/api/consent) | `GET /Consent/{id}/files/sourceAttachment` |
| [DiagnosticReport](/api/diagnosticreport) | `GET /DiagnosticReport/{id}/files/presentedForm` |
| [DocumentReference](/api/documentreference) | `GET /DocumentReference/{id}/files/content` |
| [Media](/api/media) | `GET /Media/{id}/files/content` |
| [Patient](/api/patient) | `GET /Patient/{id}/files/photo` |
| [Practitioner](/api/practitioner) | `GET /Practitioner/{id}/files/signature` |

## Option 1: Follow the redirect to get the file content

The simplest approach is to let your HTTP client follow the redirect automatically. The pre-signed S3 URL contains its own authentication in the query parameters, so no additional headers are needed for the second request.

{% tabs attachment-follow-redirect %}

  {% tab attachment-follow-redirect curl %}
```bash
curl -L -o downloaded_file.pdf \
  -H "Authorization: Bearer $TOKEN" \
  "https://fumage-{instance}.canvasmedical.com/DocumentReference/abc123/files/content"
```
  {% endtab %}

  {% tab attachment-follow-redirect python %}
```python
import requests

base_url = "https://fumage-{instance}.canvasmedical.com"
token = "your_bearer_token"

file_url = f"{base_url}/DocumentReference/abc123/files/content"
response = requests.get(
    file_url,
    headers={"Authorization": f"Bearer {token}"},
)

with open("downloaded_file.pdf", "wb") as f:
    f.write(response.content)
```
  {% endtab %}

  {% tab attachment-follow-redirect javascript %}
```javascript
const response = await axios.get(url, {
  headers: { Authorization: `Bearer ${token}` },
  responseType: 'arraybuffer',
});
// response.data contains the raw file content
writeFileSync('downloaded_file.pdf', Buffer.from(response.data));
```
  {% endtab %}

{% endtabs %}

## Option 2: Capture the pre-signed URL without following the redirect

If you need the pre-signed S3 URL itself — for example, to load it in an `<iframe>`, pass it to a frontend, or open it in a browser — you can configure your client to not follow redirects, and read the `Location` header in the response.

{% tabs attachment-capture-url %}

  {% tab attachment-capture-url curl %}
```bash
PRESIGNED_URL=$(curl -s -o /dev/null -w '%{redirect_url}' \
  -H "Authorization: Bearer $TOKEN" \
  "https://fumage-{instance}.canvasmedical.com/DocumentReference/abc123/files/content")

echo "$PRESIGNED_URL"
```
  {% endtab %}

  {% tab attachment-capture-url python %}
```python
import requests

base_url = "https://fumage-{instance}.canvasmedical.com"
token = "your_bearer_token"

file_url = f"{base_url}/DocumentReference/abc123/files/content"
response = requests.get(
    file_url,
    headers={"Authorization": f"Bearer {token}"},
    allow_redirects=False,
)

presigned_url = response.headers["Location"]
# This URL works without auth and expires after 10 minutes
```
  {% endtab %}

  {% tab attachment-capture-url javascript %}
```javascript
const response = await axios.get(url, {
  maxRedirects: 0,
  validateStatus: (status) => status === 307,
  headers: { Authorization: `Bearer ${token}` },
});

const presignedUrl = response.headers['location'];
// This URL works without auth — use it in an iframe, open in browser, etc.
```
  {% endtab %}

{% endtabs %}

## Note on HTTP client redirect behavior

Per [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110#section-15.4), compliant HTTP clients should strip the `Authorization` header when following a redirect to a different host. However, some HTTP clients do not do this, which can cause S3 to reject the request with a dual-auth error:

```xml
<Error>
  <Code>InvalidArgument</Code>
  <Message>Only one auth mechanism allowed; only the X-Amz-Algorithm
  query parameter or the Authorization header should be specified,
  not both.</Message>
</Error>
```

If you encounter this error, your client is forwarding the Bearer token to S3. Use **Option 2** above to handle the redirect manually, or configure your client to strip authorization headers on cross-origin redirects.
