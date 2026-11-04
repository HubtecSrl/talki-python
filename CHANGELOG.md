# Changelog

This package follows [semantic versioning](https://semver.org). The API
version each release targets by default is `talki.API_VERSION`.

## 0.5.0b1 — 2026-11-04

For API version `2026-10-01`, as 0.4.0b1, with what has been added and corrected
in it since. Some of it changes existing types: see the second list.

- `talki.contacts.list(phone=…)` and `tag_id=` find contacts by number or by tag.
  Either makes the list a search, not the change feed: newest contact first,
  `next_cursor` null on the last page, and a cursor works only in the mode that
  issued it, so resume a sync from the unfiltered list.
- `Appointment.notes`: the note on a booking, what `create` sent as `notes` or
  what the assistant wrote on a call, null when there is none.
- `call.ringing`: a webhook event sent while an inbound call rings, before the
  assistant picks up, with `call_id`, `location_id`, `caller` (`contact_id`,
  `phone_number`, `display_name`, `vip`) and `started_at` in its `data`.
  `construct_event` returns it like any other event. An endpoint subscribed to
  every event starts receiving it; an OAuth app gets it by subscribing, with
  `calls:read`. Not every ring is followed by a `Call`.
- The OpenAPI document describes every event's payload under `webhooks`. This
  package still generates no types from it: `construct_event` returns a dict.
- The `usage.threshold_reached` and `usage.extra_credits_low` events carry the
  names `GET /v1/usage` uses, such as `used_seconds` and `included_seconds`. The
  older `seconds_*` names and `extra_seconds_balance` still come, with the same
  values, and are deprecated.
- Docstrings corrected with the document's descriptions, among them what
  `talki.sandbox.reset()` deletes (webhook endpoints included) and what
  `location_id=` changes on `talki.account.update()`.

What changes for existing code:

- These are now a `datetime`, like every other timestamp, not a `str`:
  `CallTransfer.at`, `period_start` and `period_end` of `CallStats` and
  `RefusedCallSummary`, `Usage.period_start`, `UsageHistory.retained_since`,
  `UsageMonth.start` and `end`. `to_dict()` writes them with `+00:00`, not `Z`.
- A withheld caller's number is null, where the API could send `+` or
  `+nonymous`. `PendingContact.phone_number` and `CallStatsCaller.phone_number`
  are now `str | None`. Already typed so, and null now too:
  `Call.caller.phone_number`, a refused call's `caller.phone_number`,
  `UnresolvedRequest.caller_phone` and `AppointmentClient.phone_number`. A pending
  contact with no number can only be discarded. `CallStats.top_callers` counts
  every call with no number as one entry.
- `Appointment` requires `notes`: an `Appointment(…)` built by hand needs it.
- `CallTransfer.at` and `transferred_at` on `call.transferred` are in UTC, with
  `Z`, where a real call gave the account's local offset. The instant is the
  same. `CallTransfer.target_label` is the label as the owner wrote it; calls
  stored earlier can differ in case, so compare it case-insensitively.
- The update models no longer type `None` on the fields the API refuses it for,
  with a `400`, as it did before: on `AccountUpdate`, `CallUpdate`,
  `CallerRuleUpdate`, `ClosureUpdate`, `DocumentUpdate`, `ServiceUpdate` and
  `UnresolvedRequestUpdate`. Given `None` anyway, `answers_as`, `kind`, `status`
  and `transfer_numbers` now raise in `to_dict()`, before anything is sent.
- For the same reason `answers_as`, `kind` and `status` on those models take the
  enum only: `CallerRuleUpdate(kind="vip")`, which used to send, now raises
  `AttributeError`. Use `CallerRuleKind.VIP`, or a dict body, which is sent as
  written.
- `also=` on `talki.documents.update()`, `replace()`, `delete()` and
  `delete_page()` is typed by an enum per method (`UpdateDocumentAlsoType0.COPIES`
  and so on, in `talki.models`), not `Literal["copies"]`. `also="copies"` sends
  the same request, but a type checker refuses it. `replace_file()` takes both.
- `talki.appointments.reschedule()` of a booking of one service with a
  `duration_minutes` must keep that length, or the length it has now. A move that
  changes it, one edge alone included, raises `InvalidRequestError`.
- Your own `idempotency_key=` on a retry: a response a retry can change is no
  longer replayed when the request saved nothing, and the retry runs it again.
  That covers a `400` asking for a different request (`invalid_parameter` and the
  like), a `415`, and a `409` `request_conflict`, `document_not_ready` or
  `check_in_progress`. A refusal that holds until the state changes (a time taken,
  a list full) is still replayed for 24 hours: once its cause is gone, retry with
  a new key.
- A sandbox scenario's `events`, on `talki.sandbox.list_scenarios()` and
  `create_call()`, start with `call.ringing`, and are no longer all a call sends:
  a caller who gives a name can send `pending_contact.created` too. Assert that
  the listed events arrive, not that nothing else does.
- A change feed's cursor issued now, used on another feed, raises
  `InvalidRequestError` (`invalid_cursor`), where it could skip rows. A cursor
  stored earlier still works until 2027-02-01, after which it raises the same and
  the walk restarts. The first page read with it returns a new one to store.

## 0.4.0b1 — 2026-11-02

For API version `2026-10-01`, as 0.3.0b1, with the operations added to it since.

- `talki.documents`: the knowledge base by API, notes, websites and files.
  `list`, `get`, `create`, `update`, `replace`, `delete`, `get_text`, and for a
  website `discover_pages`, `list_pages` and `delete_page`.
- `talki.documents.upload()` and `replace_file()` send a file (a path, bytes,
  an open file or a `talki.types.File`) as `multipart/form-data`. `get_file()`
  and `download()`, the same method, return it as a `talki.types.File` with the
  name and type it was uploaded with.
- A `multipart/form-data` body, `create()` and `replace()` given a
  `DocumentUpload` or `DocumentFileReplace` included, is encoded whole with a
  random boundary, so a request turned away unrun is retried like any other.
  A `talki.types.File` without a `file_name` raises `ValueError` before sending.
- `ErrorDetail.code` lists two new codes, `document_not_ready` and
  `unsupported_file_type`.
- The lowest supported `anyio` is 3.0.1.
- `Account.call_auto_archive_days` and `AccountUpdate.call_auto_archive_days`:
  how many days after it started a read call is archived on its own.

## 0.3.0b1 — 2026-10-28

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
  method is no longer a coroutine function: `asyncio.create_task()` and
  `TaskGroup.create_task()` no longer take its result, nor anyio's
  `start_soon` the method, and `inspect.iscoroutinefunction()` is False for it.
  `asyncio.gather()` and `asyncio.wait_for()` still take it.

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
