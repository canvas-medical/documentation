---
title: "Utils"
---

## Making requests with Http

The Canvas SDK offers a helper class for completing HTTP calls.

```python
from canvas_sdk.utils import Http
http = Http()
```

### get

Sends a GET request.

**Parameters**:

| Name      | Type     | Required | Description                            |
| :-------- | :------- | :------- | :------------------------------------- |
| `url`     | _string_ | `true`   | The url of the request.                |
| `headers` | _dict_   | `false`  | The headers to include in the request. |

**Example**:

```python
http = Http()
http.get("https://my-url.com/", headers={"Authorization": f"Bearer token"})
```

### post

Sends a POST request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
http = Http()
http.post(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"post": "json"},
    data="this-is-my-data"
)
```

### put

Sends a PUT request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
http = Http()
http.put(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"put": "json"},
    data="this-is-my-data"
)
```

### patch

Sends a PATCH request.

**Parameters**:

| Name      | Type               | Required | Description                            |
| :-------- | :----------------- | :------- | :------------------------------------- |
| `url`     | _string_           | `true`   | The url of the request.                |
| `headers` | _dict_             | `false`  | The headers to include in the request. |
| `json`    | _dict_             | `false`  | The json to include in the request.    |
| `data`    | _dict_ or _string_ | `false`  | The data to include in the request.    |

**Example**:

```python
http = Http()
http.patch(
    "https://my-url.com/",
    headers={"Authorization": f"Bearer token"},
    json={"patch": "json"},
    data="this-is-my-data"
)
```
