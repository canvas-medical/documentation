---
title: AWS S3
slug: clients-aws-s3
hidden: false
---

The Canvas SDK AWS S3 client provides a simple interface for interacting with Amazon S3 storage, including uploading, downloading, listing, and deleting objects, as well as generating presigned URLs for temporary access.

## Requirements

- **AWS Access Key ID**: Your AWS access key
- **AWS Secret Access Key**: Your AWS secret key
- **AWS Region**: The region where your bucket is located (e.g., `us-east-1`)
- **S3 Bucket Name**: The name of your S3 bucket

## Imports

The AWS S3 client is included in the Canvas SDK. Import the necessary components:

```python
from canvas_sdk.clients.aws import S3, Credentials, S3Item
```

Or import from specific modules:

```python
from canvas_sdk.clients.aws.libraries import S3
from canvas_sdk.clients.aws.structures import Credentials, S3Item
```

## Initialize the Client

```python
from canvas_sdk.clients.aws import S3, Credentials

credentials = Credentials(
    key="your_aws_access_key_id",
    secret="your_aws_secret_access_key",
    region="us-east-1",
    bucket="your-bucket-name"
)

client = S3(credentials)
```

## Check if Client is Ready

```python
if client.is_ready():
    print("S3 client is configured and ready")
else:
    print("Missing credentials")
```

## Upload a Text File

```python
from canvas_sdk.clients.aws import S3, Credentials

credentials = Credentials(
    key="your_access_key",
    secret="your_secret_key",
    region="us-east-1",
    bucket="my-bucket"
)

client = S3(credentials)

# Upload text content
response = client.upload_text_to_s3("path/to/file.txt", "Hello, World!")

if response and response.status_code == 200:
    print("Text file uploaded successfully!")
```

## Upload a Binary File

```python
# Upload binary content (e.g., an image)
with open("local_image.png", "rb") as f:
    binary_data = f.read()

response = client.upload_binary_to_s3(
    "images/uploaded_image.png",
    binary_data,
    "image/png"
)

if response and response.status_code == 200:
    print("Binary file uploaded successfully!")
```

## Download a File

```python
response = client.access_s3_object("path/to/file.txt")

if response:
    content = response.content
    print(f"Downloaded content: {content.decode('utf-8')}")
```

## List Objects in Bucket

```python
# List all objects with a prefix
items = client.list_s3_objects("documents/")

if items:
    for item in items:
        print(f"Key: {item.key}, Size: {item.size} bytes, Modified: {item.last_modified}")
```

## Delete an Object

```python
response = client.delete_object("path/to/file.txt")

if response and response.status_code == 204:
    print("Object deleted successfully!")
```

## Generate a Presigned URL

```python
# Generate a URL valid for 1 hour (3600 seconds)
url = client.generate_presigned_url("path/to/file.txt", expiration=3600)

if url:
    print(f"Presigned URL: {url}")
```

## S3

The main class for interacting with AWS S3.

### Constructor

```python
S3(credentials: Credentials)
```

| Parameter     | Type          | Description                              |
|---------------|---------------|------------------------------------------|
| `credentials` | `Credentials` | AWS credentials for S3 access            |

### Methods

#### `is_ready() -> bool`

Check if all required credentials are provided.

**Returns:** `True` if all credentials (key, secret, region, bucket) are non-empty, `False` otherwise.

#### `access_s3_object(object_key: str) -> Response | None`

Download an object from S3.

**Parameters:**

| Parameter    | Type  | Description                    |
|--------------|-------|--------------------------------|
| `object_key` | `str` | S3 object key (path) to access |

**Returns:** `requests.Response` containing the object data, or `None` if credentials are not ready.

#### `upload_text_to_s3(object_key: str, data: str) -> Response | None`

Upload text data to S3 as `text/plain`.

**Parameters:**

| Parameter    | Type  | Description                          |
|--------------|-------|--------------------------------------|
| `object_key` | `str` | S3 object key (path) to create/update|
| `data`       | `str` | Text content to upload               |

**Returns:** `requests.Response` from S3, or `None` if credentials are not ready.

#### `upload_binary_to_s3(object_key: str, binary_data: bytes, content_type: str) -> Response | None`

Upload binary data to S3.

**Parameters:**

| Parameter      | Type    | Description                          |
|----------------|---------|--------------------------------------|
| `object_key`   | `str`   | S3 object key (path) to create/update|
| `binary_data`  | `bytes` | Binary content to upload             |
| `content_type` | `str`   | MIME type (e.g., `image/png`)        |

**Returns:** `requests.Response` from S3, or `None` if credentials are not ready.

#### `delete_object(object_key: str) -> Response | None`

Delete an object from S3.

**Parameters:**

| Parameter    | Type  | Description                  |
|--------------|-------|------------------------------|
| `object_key` | `str` | S3 object key (path) to delete|

**Returns:** `requests.Response` from S3, or `None` if credentials are not ready.

#### `list_s3_objects(prefix: str) -> list[S3Item] | None`

List all objects in S3 with the given prefix. Handles pagination automatically.

**Parameters:**

| Parameter | Type  | Description                            |
|-----------|-------|----------------------------------------|
| `prefix`  | `str` | S3 key prefix to filter objects        |

**Returns:** List of `S3Item` objects with metadata, or `None` if credentials are not ready.

**Raises:** `Exception` if S3 returns a non-200 status code.

#### `generate_presigned_url(object_key: str, expiration: int) -> str | None`

Generate a presigned URL for temporary access to an S3 object.

**Parameters:**

| Parameter    | Type  | Description                          |
|--------------|-------|--------------------------------------|
| `object_key` | `str` | S3 object key (path)                 |
| `expiration` | `int` | URL expiration time in seconds       |

**Returns:** Presigned URL string, or `None` if credentials are not ready.

---

## Data Structures

### Credentials

AWS credentials for S3 access.

| Field    | Type  | Description                              |
|----------|-------|------------------------------------------|
| `key`    | `str` | AWS access key ID                        |
| `secret` | `str` | AWS secret access key                    |
| `region` | `str` | AWS region (e.g., `us-east-1`)           |
| `bucket` | `str` | S3 bucket name                           |

**Example:**

```python
from canvas_sdk.clients.aws import Credentials

credentials = Credentials(
    key="AKIAIOSFODNN7EXAMPLE",
    secret="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region="us-west-2",
    bucket="my-application-bucket"
)
```

### S3Item

S3 object metadata returned by `list_s3_objects`.

| Field           | Type       | Description                          |
|-----------------|------------|--------------------------------------|
| `key`           | `str`      | Object key (path) in the S3 bucket   |
| `size`          | `int`      | Object size in bytes                 |
| `last_modified` | `datetime` | Timestamp of the last modification   |

**Example:**

```python
items = client.list_s3_objects("documents/")

for item in items:
    print(f"File: {item.key}")
    print(f"Size: {item.size} bytes")
    print(f"Last Modified: {item.last_modified}")
```

---

## Complete Plugin Example

Here's a complete example of using the S3 client in a Canvas plugin:

```python
from http import HTTPStatus

from canvas_sdk.clients.aws import S3, Credentials
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import JSONResponse, PlainTextResponse, Response
from canvas_sdk.handlers.simple_api import Credentials as APICredentials, SimpleAPI, api


class S3Handler(SimpleAPI):
    """Simple API handler for S3 operations."""

    def authenticate(self, credentials: APICredentials) -> bool:
        return True

    def _s3_client(self) -> S3:
        """Create S3 client from plugin secrets."""
        return S3(
            Credentials(
                key=self.secrets["S3Key"],
                secret=self.secrets["S3Secret"],
                region=self.secrets["S3Region"],
                bucket=self.secrets["S3Bucket"],
            )
        )

    @api.get("/list")
    def list_files(self) -> list[Response | Effect]:
        """List all files in the bucket."""
        client = self._s3_client()
        if client.is_ready():
            items = client.list_s3_objects("")
            content = [{"key": p.key, "size": p.size} for p in items]
            return [JSONResponse(content, status_code=HTTPStatus.OK)]
        return []

    @api.get("/download/<file_key>")
    def download_file(self) -> list[Response | Effect]:
        """Download a file by key."""
        file_key = self.request.path_params["file_key"]
        client = self._s3_client()
        if client.is_ready() and file_key:
            response = client.access_s3_object(file_key)
            return [Response(response.content, status_code=HTTPStatus.OK)]
        return []

    @api.post("/upload/<file_key>")
    def upload_file(self) -> list[Response | Effect]:
        """Upload a file."""
        file_key = self.request.path_params["file_key"]
        client = self._s3_client()
        content = self.request.body
        content_type = self.request.content_type

        if client.is_ready() and file_key:
            if content_type == "text/plain":
                response = client.upload_text_to_s3(file_key, content.decode("utf-8"))
            else:
                response = client.upload_binary_to_s3(file_key, content, content_type)
            return [Response(response.content, status_code=response.status_code)]
        return []

    @api.delete("/delete/<file_key>")
    def delete_file(self) -> list[Response | Effect]:
        """Delete a file by key."""
        file_key = self.request.path_params["file_key"]
        client = self._s3_client()
        if client.is_ready() and file_key:
            response = client.delete_object(file_key)
            return [Response(response.content, status_code=HTTPStatus.OK)]
        return []

    @api.get("/presigned/<file_key>")
    def get_presigned_url(self) -> list[Response | Effect]:
        """Generate a presigned URL for temporary access."""
        file_key = self.request.path_params["file_key"]
        client = self._s3_client()
        if client.is_ready() and file_key:
            url = client.generate_presigned_url(file_key, 3600)  # 1 hour
            return [PlainTextResponse(url, status_code=HTTPStatus.OK)]
        return []
```

---

## Error Handling

The S3 client methods return `None` when credentials are not ready. For list operations, an `Exception` is raised if S3 returns an error status code.

```python
# Check credentials before operations
if not client.is_ready():
    print("S3 credentials are not configured")
    return

# Handle list errors
try:
    items = client.list_s3_objects("prefix/")
except Exception as e:
    print(f"S3 error: {e}")

# Check response status for uploads/downloads
response = client.upload_text_to_s3("file.txt", "content")
if response:
    if response.status_code == 200:
        print("Upload successful")
    else:
        print(f"Upload failed with status {response.status_code}")
else:
    print("Credentials not ready")
```

---

## AWS Signature V4 Authentication

The S3 client implements AWS Signature Version 4 for request authentication. This is handled automatically - you only need to provide valid credentials. The client:

- Signs all requests with HMAC-SHA256
- Generates proper canonical requests
- Handles date/time formatting for AWS
- Supports presigned URLs for temporary access

---

## Additional Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
- [S3 REST API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)
- [Example Plugin](/sdk/example-aws_s3/) - Documentation for the example plugin
- [Source Code](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/aws_s3) - View the source on GitHub
