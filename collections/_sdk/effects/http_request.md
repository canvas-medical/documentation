---
title: "HTTP Request"
slug: "effect-http-request"
excerpt: "Have the platform issue an HTTP request on behalf of a plugin."
hidden: false
---

The `HttpRequestEffect` lets a plugin ask the Canvas platform to issue an HTTP request on its behalf. The plugin returns the effect from a handler and the platform performs the call.

We recommend running the request asynchronously by chaining [`.set_async(...)`](#async-execution) onto the applied effect. The request is then handed off to the platform's async runner, which manages delay, retries, and backoff so the handler doesn't block on the network. Setting `retry_on_status_codes` automatically opts into async execution (equivalent to `.set_async(delay_seconds=0)`), so you only need to call `.set_async(...)` explicitly to add a delay or set `max_retries`.

Without `.set_async(...)` and without `retry_on_status_codes`, the effect is executed inline.

## Attributes

| Name                    | Type                          | Required | Description                                                                                                                                                                                       |
|-------------------------|-------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `url`                   | `str`                         | Yes      | The URL to request. Must be non-empty. Cannot resolve to a private or loopback address (see [Security](#security--network-behavior)).                                                             |
| `method`                | [`HttpMethod`](#httpmethod)   | No       | The HTTP method to use. Defaults to `HttpMethod.GET`.                                                                                                                                             |
| `headers`               | `dict[str, str]` or `None`    | No       | Request headers. Header values are transmitted as-is — store credentials in the plugin's [`secrets`](/sdk/secrets/) and reference them here rather than hard-coding them.                         |
| `body`                  | `str` or `None`               | No       | The request body, as a string. For JSON payloads, serialize with `json.dumps(...)` and set the appropriate `Content-Type` header.                                                                 |
| `retry_on_status_codes` | `list[int]` or `None`         | No       | HTTP status codes that should trigger a retry. Each value must be in the range `100`–`599`. Setting this automatically routes the request through the async runner (equivalent to `.set_async(delay_seconds=0)`); use `.set_async(...)` only to override the delay or set `max_retries`. |

## `HttpMethod`

A `StrEnum` of the supported HTTP methods. You can also pass the string value as well.

| Member               | Value      |
|----------------------|------------|
| `HttpMethod.GET`     | `"GET"`    |
| `HttpMethod.POST`    | `"POST"`   |
| `HttpMethod.PUT`     | `"PUT"`    |
| `HttpMethod.PATCH`   | `"PATCH"`  |
| `HttpMethod.DELETE` | `"DELETE"` |


## Security & Network Behavior

The platform applies several safeguards before executing the request:

- **SSRF protection.** The host is resolved and rejected if it points at a private (RFC 1918), loopback, link-local (including the `169.254.169.254` cloud metadata address), multicast, reserved, or unspecified address. Both literal IPs (e.g. `http://10.0.0.1/`) and hostnames that resolve to such addresses are blocked.
- **Redirect behavior.** GET requests follow redirects normally. Non-GET methods (POST, PUT, PATCH, DELETE) are made with `allow_redirects=False`, so a `3xx` response is returned as-is rather than re-posting data to a different host.
- **Request timeout.** Each request has a 30-second timeout. Requests that exceed it are aborted.
- **Connection errors are swallowed.** If the upstream service is unreachable or the request fails at the transport layer, the failure is logged and the effect pipeline continues — it does not raise back into your handler.
- **Redacted logging.** The platform logs the request method, host, path, and final status code. Query strings, fragments, request headers, request bodies, and response bodies are never logged, so credentials passed via query string or `Authorization` headers do not leak into platform logs.

## Async Execution

Chain `.set_async(...)` onto the result of `.apply()` to have the platform schedule the request through its async runner instead of running it inline with the handler. You can read more about async effect execution [here](/sdk/effects/#async-execution).

When `retry_on_status_codes` is set on the effect, the SDK automatically sets `delay_seconds=0` (async-now) so the request is routed through the async runner — you don't need to call `.set_async()` separately just for retries. The async runner uses `retry_on_status_codes` (in combination with `max_retries`) to decide whether a response should trigger a retry.

## Handling Credentials

Header values are transmitted to the upstream service exactly as provided. Do not hard-code API tokens or other credentials into your plugin source. Instead, declare them as [secrets](/sdk/secrets/) in `CANVAS_MANIFEST.json` and read them at runtime via `self.secrets` on the handler.

## Example Usage

### Send a POST request asynchronously

```python
import json

from canvas_sdk.effects import EventType
from canvas_sdk.effects.http_request import HttpMethod, HttpRequestEffect
from canvas_sdk.handlers import BaseHandler


class MyHandler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)

    def compute(self):
        http_effect = HttpRequestEffect(
            url="https://api.example.com/submit",
            method=HttpMethod.POST,
            headers={
                "Authorization": f"Bearer {self.secrets['MY_API_TOKEN']}",
                "Content-Type": "application/json",
            },
            body=json.dumps({"patient_id": self.target}),
            retry_on_status_codes=[500, 502, 503],
        )

        # retry_on_status_codes already implies async-now; .set_async() is here to add max_retries
        return [http_effect.apply().set_async(max_retries=3)]
```

### Issue a simple GET request

```python?partial=True
http_effect = HttpRequestEffect(
    url="https://api.example.com/status",
)

return [http_effect.apply().set_async(delay_seconds=0)]
```

### Schedule a delayed request

```python?partial=True
# Run the request 60 seconds from now
http_effect = HttpRequestEffect(
    url="https://api.example.com/sync",
    method=HttpMethod.PUT,
    body=json.dumps({"status": "ready"}),
    headers={"Content-Type": "application/json"},
)

return [http_effect.apply().set_async(delay_seconds=60)]
```

## Validation

Construction is validated by Pydantic and will raise a `ValidationError` for:

- An empty `url`.
- A `method` that is not a member of `HttpMethod`.
- A `retry_on_status_codes` entry that is not an integer or falls outside the `100`–`599` range.

<br/>
<br/>
<br/>
