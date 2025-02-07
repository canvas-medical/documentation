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

## Making concurrent requests with Http

There is an interface for executing HTTP requests in parallel.

The `batch_requests` method will execute the requests in parallel using multithreading, and return once all the requests
have completed.

The first parameter to the method is an iterable of `BatchableRequest` objects. These can be created with the following
helper functions:

```
batch_get
batch_post
batch_put
batch_patch
```

The parameters that these helper functions accept match what the corresponding single-request methods accept.

The `timeout` parameter allows for specifying a timeout value in seconds; if a request has not completed before the
timeout value, an error will be returned for that request. The maximum allowed value for `timeout` is 30 seconds. If
`timeout` is not specified, it will be set to the maximum value.

The return value will be a list of responses to the requests. The order of the return value will correspond to the order
of the provided requests.

**Parameters**:

| Name             | Type                         | Required | Description                   |
|:-----------------|:-----------------------------|:---------|:------------------------------|
| `batch_requests` | _Iterable[BatchableRequest]_ | `true`   | The list of batched requests. |
| `timeout`        | _integer_                    | `false`  | The timeout value in seconds. |

**Example**:

```python
from canvas_sdk.utils import Http, batch_get, batch_post, batch_put, batch_patch

http = Http()

requests = [
    batch_get("https://my-url.com/", headers={"Authorization": f"Bearer token"}),
    batch_post("https://my-url.com/", headers={"Authorization": f"Bearer token"}, json={"post": "json"}),
    batch_put("https://my-url.com/", headers={"Authorization": f"Bearer token"}, data="this-is-my-data"),
    batch_patch("https://my-url.com/", headers={"Authorization": f"Bearer token"}, json={"patch": "json"})
]

responses = http.batch_requests(requests, timeout=10)
```
