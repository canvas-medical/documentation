---
title: "Snapshot"
slug: "data-snapshot"
excerpt: "Images captured via the Canvas iOS application."
hidden: false
---

# Snapshot Models

The `Snapshot` and `SnapshotImage` models represent images captured via the Canvas iOS application or uploaded directly through the coverages modal. A `Snapshot` groups related images together, while each `SnapshotImage` represents an individual image with presigned URL support for secure access.

Snapshots are primarily used to store coverage card images. To navigate from a [`Coverage`](/sdk/data-coverage/#coverage) to its linked `Snapshot`, use `coverage.snapshot`. There is currently no way to navigate from a `Snapshot` back to its associated `Coverage`.

## Basic Usage

```python
from canvas_sdk.v1.data import Snapshot, SnapshotImage

# Get all snapshots
snapshots = Snapshot.objects.all()

# Get a specific snapshot
snapshot = Snapshot.objects.get(dbid=42)

# Get images for a snapshot
images = snapshot.images.all()

# Get all snapshot images
all_images = SnapshotImage.objects.all()
```

## Accessing Image Files

The `image_url` property on `SnapshotImage` returns a presigned S3 URL for securely accessing the image file.

```python
from canvas_sdk.v1.data import SnapshotImage

image = SnapshotImage.objects.exclude(image="").first()

# Returns a presigned S3 URL (valid for 1 hour)
url = image.image_url
```

## Attributes

### Snapshot

| Field Name       | Type                               |
|------------------|------------------------------------|
| dbid             | Integer                            |
| created          | DateTime                           |
| modified         | DateTime                           |
| originator       | [CanvasUser](/sdk/data-canvasuser) |
| committer        | [CanvasUser](/sdk/data-canvasuser) |
| deleted          | Boolean                            |
| entered_in_error | Boolean                            |
| title            | String                             |
| description      | String                             |
| images           | [SnapshotImage](#snapshotimage)[]  |

### SnapshotImage

| Field Name  | Type                        |
|-------------|-----------------------------|
| dbid        | Integer                     |
| created     | DateTime                    |
| modified    | DateTime                    |
| snapshot    | [Snapshot](#snapshot)       |
| image       | String                      |
| title       | String                      |
| instruction | String                      |
| tag         | String                      |
| image_url   | String (property) — presigned S3 URL |
