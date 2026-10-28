# Changelog

This package follows [semantic versioning](https://semver.org). The API
version each release targets by default is `talki.API_VERSION`.

## Unreleased

For API version `2026-10-01`, as 0.2.0b1.

- `talki.<tag>.with_raw_response.<method>()`: the same call, returning a
  `talki.RawResponse` with the status, the headers (`ETag` to send back as
  `if_match=`, `X-Request-Id`, the rate limits) and `parse()`, the value.
- `body=` takes a dict as well as the model, typed by a TypedDict per request
  model (`talki.models.AppointmentCreateDict`, …). It is sent as written, with
  dates, datetimes and UUIDs as ISO strings and enums as their values.
- `talki.with_options(timeout=…, max_retries=…)`: the client with other
  settings for the calls made on it, sharing its connections and its token
  renewal.
- `Talki(user_agent="acme-crm/2.1")` adds an integration's name to the
  `User-Agent`.
- On `AsyncTalki`, a list that pages returns a `talki.pagination.AsyncPager`:
  `async for call in talki.calls.list()` without `await`. Awaiting it still
  gives the first page, so `await talki.calls.list()` is unchanged; but the
  method is no longer a coroutine function, so `asyncio.create_task()` no
  longer takes its result directly.

## 0.2.0b1 — 2026-10-23

For API version `2026-10-01`, as 0.1.0b1.

- A method per operation, on one attribute per tag: `talki.calls.list()`,
  `talki.appointments.create(body=…)`. It returns the model or raises the
  `ApiError` subclass, as `unwrap` does. The methods are generated from the
  OpenAPI document's tags and operation IDs.
- `AsyncTalki`: the same client with methods to await.
- A list that takes `cursor` returns a `talki.pagination.Page` (`AsyncPage`):
  the first page, whose iteration yields every row, fetching the pages after
  it; `iter_pages()` yields the pages.
- `Talki.close()` and `AsyncTalki.aclose()`, for a client kept without
  `with`. A closed client stays usable, and the same client can be opened
  with `with` more than once.
- `talki.__version__`, and a `User-Agent` naming this package's version,
  Python's and httpx's on every request, token requests included.
- `Talki()` and `AsyncTalki()` with no credential read the API key from
  `TALKI_API_KEY`.
- Logging on the `talki` logger: each answer at DEBUG (method, path, status,
  request ID, time), each retry and automatic token renewal at INFO, a
  renewal whose outcome is unknown at WARNING and one refused at ERROR. Never
  a query string, header, body or token.
- The operations under `talki.api`, `unwrap` and `pages` / `rows` are
  unchanged, for the whole `Response`. `Talki` still opens with `async with`
  for the async operations.

## 0.1.0b1 — 2026-10-23

First public release, for API version `2026-10-01`.

- Every `/v1` operation, sync and async, with typed models.
- `Talki`: API key, access token or self-renewing OAuth pair; `Talki-Version`
  pinned on the client; an automatic `Idempotency-Key` on writes; retries
  that honour `Retry-After` and never repeat a write that may have been saved.
- `unwrap` and typed exceptions per error `type`.
- `talki.pagination`: page and row iterators for lists and change feeds.
- `talki.webhooks`: signature checks for webhook and app events.
- `talki.oauth`: consent URL with PKCE, callback, code exchange, refresh and
  revocation.
- Enums parse values added after a release instead of failing.
