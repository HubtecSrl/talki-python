# Changelog

This package follows [semantic versioning](https://semver.org). The API
version each release targets by default is `talki.API_VERSION`.

## 0.7.0b1 — 2026-11-20

For API version `2026-10-01`, as 0.6.0b1, with what has been added to it since.
One change to existing types: see the second list.

- `talki.whatsapp`: the business's WhatsApp chats, which Talki can answer on
  the business's own WhatsApp Business number. The owner connects the number in
  the Talki app; the API cannot.
- `talki.whatsapp.get()` returns the connected number and how Talki answers its
  chats: `mode` (`off`, Talki reads and stores nothing; `always`; or
  `scheduled`, only inside `schedule`, ranges in Rome time), `available` and
  `blocked_reason`, this period's `usage` against the plan's cap, and the
  owner's `pending_questions`. `after_hours_schedule` is every time the main
  location's weekly hours leave closed, ready to send as `schedule`.
  `update(body=…)` changes the mode, the schedule, or both. Turning the answers
  on from `off` raises `PermissionDeniedError` (`plan_feature_unavailable`)
  without a plan that includes WhatsApp chats, and `ConflictError` without a
  connected number (`whatsapp_not_connected`) or while Talki does not answer
  WhatsApp chats for any account yet (`whatsapp_chats_unavailable`). `get`
  needs `whatsapp:read`, `update` needs `whatsapp:write`.
- `talki.whatsapp.list_conversations()` pages through the conversations Talki
  took part in or kept out of, newest first; `needs_answer=True` lists those
  waiting for the owner's «è un cliente?». `get_conversation(id)` returns one:
  the contact, its `outcome`, a short `summary` once it closes (when Talki
  replied or handed the chat to the owner), the `question` and the
  `appointment_ids` booked in it. Both need `whatsapp:read`.
- `talki.whatsapp.get_conversation_messages(id)`: a conversation's messages,
  oldest first. It needs `transcripts:read`, which `whatsapp:read` does not
  grant. Messages are kept 30 days: after that `messages_expired` is true, the
  messages are deleted and the conversation stays.
- `talki.whatsapp.answer_conversation(id, body={"answer": …})` answers «è un
  cliente?» for the owner, on any conversation, asked or not: `customer` (Talki
  answers the contact, now if WhatsApp's 24-hour window is open), `ignore`
  (never), or `owner` (the owner replies). `customer` and `ignore` set a contact
  rule: past the account's 500 rules it raises `ConflictError`
  (`whatsapp_contact_rule_limit_reached`). Needs `whatsapp:write`. On a plan
  without WhatsApp chats, `answer_conversation`, `create_contact_rule` and
  `update_contact_rule` raise `PermissionDeniedError`
  (`plan_feature_unavailable`), as `update` does.
- `talki.whatsapp.list_contact_rules()`, `create_contact_rule`,
  `update_contact_rule` and `delete_contact_rule`: the numbers Talki never
  answers (`ignore`) or answers as customers without judging first
  (`customer`), at most 500. A number holds one rule: adding a second raises
  `ConflictError` (`whatsapp_contact_rule_exists`), so change it with
  `update_contact_rule`. A rule you create counts towards the 20 creations per
  minute shared with services, resources, tags and caller rules. Listing needs
  `whatsapp:read`, the others `whatsapp:write`.
- `talki.whatsapp.delete_conversations()` deletes every stored conversation and
  its messages. The contact rules, the appointments booked in a chat and the
  unresolved requests it left stay. It needs the opt-in `whatsapp:delete` scope
  and live mode (`livemode_required` in test mode), and raises `ConflictError`
  (`whatsapp_answers_on`) while Talki answers the chats: set `mode` to `off`
  first.
- `UnresolvedRequest.source` (`call` or `whatsapp`) and
  `UnresolvedRequest.whatsapp_conversation_id`: a request can come from a
  WhatsApp chat Talki answered. Its `call_id` is then null and its `location_id`
  is the main location. `whatsapp_conversation_id` turns null once
  `delete_conversations` deletes the chat; the request stays. `source` is a
  `str`: treat a value you do not know as a request to handle all the same. The
  `unresolved_request.updated` event carries both.
- Three webhook events. `whatsapp.conversation_ended`: a conversation closed,
  about 30 minutes after its last message, with its outcome (and its summary
  when Talki replied or handed it to the owner); sent again if it reopens and
  closes once more. A conversation closed otherwise (two chats of the contact
  merged, or found still open when the contact wrote again much later) sends
  none: `list_conversations()` lists it all the same.
  `whatsapp.question_asked`: Talki kept silent with an unknown contact and asks
  the owner «è un cliente?», once per contact. Both carry the `WhatsAppConversation`. `whatsapp.message_sent`:
  after a call, the assistant sent the caller a WhatsApp message from the
  business's number, with their consent, and WhatsApp accepted it; it carries
  the `Call` and the message's type and language, not its text.
  `construct_event` returns them like any other event. An OAuth app gets the
  first two by subscribing, with `whatsapp:read`, and `whatsapp.message_sent`
  with `calls:read`.
- `ErrorDetail.code` lists five new codes: `whatsapp_not_connected`,
  `whatsapp_chats_unavailable`, `whatsapp_answers_on`,
  `whatsapp_contact_rule_exists` and `whatsapp_contact_rule_limit_reached`.
- `call_auto_delete_days` on `Account` and `AccountUpdate`: how many days after
  it started a call is deleted for good, read or not (`30`, `60`, `90` or
  `180`), or `None` to keep calls until the 365-day retention limit. Deletion
  runs once a night, as `talki.calls.delete` would, and sends `call.deleted`
  for each call. Setting a number needs the `calls:delete` scope as well as
  `account:write`, and is refused in test mode (`livemode_required`). The
  account's own setting: the same at every location.

What changes for existing code:

- `UnresolvedRequest` requires `source` and `whatsapp_conversation_id`: an
  `UnresolvedRequest(…)` built by hand needs them. Its `call_id`, already typed
  `str | None`, is now null for every request from WhatsApp too, not only once
  the call has aged out of retention.

## 0.6.0b1 — 2026-11-10

For API version `2026-10-01`, as 0.5.0b1, with what has been added to it since.
One change to existing types: see the second list.

- `talki.agent_test`: chat in text with the account's assistant, to check how it
  answers before a caller does. `send(body={"message": …})` returns an
  `AgentTestReply` with the `reply`, the `session_id` to send with the next
  message, `turn` and `max_turns`, `expires_at`, `daily_remaining` and
  `tools_called`. Nothing is saved in Talki: a booking the assistant makes is not
  made. Your app's own partner tools do run, sent with `test_drive: true`, writes
  included. `location_id` picks the location whose assistant answers.
  `end(session_id)` drops a session before it expires. Both need `account:write`
  and `knowledge:read`. Past the daily allowance of test messages the API answers
  `429` with a `Retry-After` until midnight. This package waits only for a
  `Retry-After` of 60 seconds or less, as for the limit per minute, so it raises
  `RateLimitError`, whose `retry_after` says how long. While testing through the
  API is switched off, `send` raises `ServerError` (`agent_test_unavailable`).
- `talki.usage.get_history(location_id=…)`: the months of one location's calls.
  The locations' months add up to the account's. A `location_id` of no location
  of the account raises `InvalidRequestError` (`resource_not_found`, `404`).
  `talki.usage.get()` stays one meter for the whole account.
- `call_auto_archive_days` can be `180`: `AccountCallAutoArchiveDaysType0` and
  `AccountUpdateCallAutoArchiveDaysType0` have `VALUE_180`. Earlier versions
  of this package read an account set to `180` as a plain `int`.
- `RefusedCall.reason`, and the keys of `RefusedCallSummary.by_reason`, can be
  `suspended`: the partner that manages the account suspended the service. Its
  `action` is `reactivate_subscription`.
- `ErrorDetail.code` lists three new codes: `account_suspended`,
  `agent_test_session_full` and `agent_test_unavailable`.
- `Usage.included_seconds` can be the monthly minutes set by the partner that
  manages the account, when they are lower than the plan's or the plan has no
  limit. `Usage.unlimited` is then false. The same figure is in
  `included_seconds` and `minutes_included` of the `usage.threshold_reached`
  event, and `minutes_included` of `usage.extra_credits_low`.
- Docstrings corrected with the document's descriptions, among them that a
  premium-rate or shared-cost number is refused as a transfer target
  (`TransferNumberInput.phone`), unless the list being replaced already holds it.

What changes for existing code:

- `AccountCallAutoArchiveDaysType0` and `AccountUpdateCallAutoArchiveDaysType0`
  have a new member, `VALUE_180`. A `match` a type checker holds to every member
  (with `assert_never`) needs a case for it.

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
  `delete_page()` is typed by the enum `talki.models.DocumentAlso`, not
  `Literal["copies"]`. `also="copies"` sends the same request, but a type checker
  refuses it. `replace_file()` takes both.
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
