---
title: Storage
---

# Storage

The Storage API is responsible for handling object storage. It provides
a simple interface for storing, retrieving and removing files.

## Basic Usage

The storage interface is simple, and should be used for all storage
operations.

``` python
from canvas_core import storage
import io

path = "tests/my_file.txt"

# You can work with any file-like object.
obj = io.StringIO()

# Persist a file to the object store at a given path.
storage.save_file(obj, path)

# Open a persisted object like any other file.
with storage.open_object(path, mode="rw") as obj:
    # do something

# Get the signed URL for a persisted object.
storage.get_object_url(path)
# https://s3.amazonaws.com/...

# Delete the persisted object at the given path.
storage.delete_object(path)

# Get a persisted object as a file (but don't forget to close it when you're done!).
file = storage.get_file(path)
# do something
file.close()

# Write bytes to the object at the given path.
storage.write_object(path, b"test string")

# Read the contents of the object at the given path (as bytes)
storage.read_object(path)
# b"test string"
```

## API Reference

::: {.automodule members=""}
canvas_core.storage
:::
