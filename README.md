# talki

The Python client for the [Talki API](https://developers.talki.it) (`/v1`):
typed, sync and async, generated from the published OpenAPI document, with a
hand-written layer for errors, retries, paging, webhooks and OAuth.

```sh
pip install --pre talki   # or: uv add --prerelease=allow talki
```

Python 3.11 or later. Depends on httpx, attrs and anyio.

> **Beta.** The API contract is versioned by date (`Talki-Version`) and does
> not break within a version; this package's own interface may still change
> before 1.0. See the [changelog](https://github.com/HubtecSrl/talki-python/blob/main/CHANGELOG.md).

## Call the API

```python
from talki import Talki, unwrap
from talki.api.account import get_account
from talki.api.appointments import create_appointment

with Talki(api_key="talki_test_…") as talki:  # or access_token="talki_at_…"
    account = unwrap(get_account.sync_detailed(client=talki.client))
    print(account.business_name)

    appointment = unwrap(create_appointment.sync_detailed(client=talki.client, body=...))
```

- Every operation is a module under `talki.api.<tag>` (its operation ID in snake
  case) with four functions: `sync`, `sync_detailed`, `asyncio` and
  `asyncio_detailed`. Each takes `client=talki.client`. Open `Talki` with
  `with` for the sync ones and `async with` for the async ones, so its
  connections are closed.
- `unwrap(response)` takes a `*_detailed` answer and returns its model, or None
  for `204 No Content`; it raises for anything else (below). Its return type is
  the operation's model.
- The `*_detailed` answer is a `talki.types.Response` with `status_code`,
  `headers` (`ETag`, `Idempotency-Replayed`, the rate-limit headers,
  `X-Request-Id`), `content` and `parsed`.
- `sync` and `asyncio` return the parsed body alone: the model, an
  `ErrorEnvelope` for a declared error status, or `None` for a status the
  operation does not declare, for an error that is not JSON, and for a `204`.
  Prefer `unwrap` over reading these apart.
- `talki.types.UNSET` is a field left out, `None` an explicit `null`. In an
  update body (`AccountUpdate`, `ServiceUpdate`, …) UNSET leaves the field as
  it is and `None` sends `null`, which clears a field that allows it.

## Errors

`unwrap` raises a subclass of `talki.ApiError` (itself a `talki.TalkiError`)
chosen by the envelope's `type`: `InvalidRequestError`, `AuthenticationError`,
`PermissionDeniedError`, `ConflictError`, `RateLimitError` (with
`retry_after`), `ServerError`. An error with no envelope, such as a proxy's answer,
is classed by its HTTP status with `code` None (a maintenance page is a 503), and a `type` this client does
not know raises `ApiError` itself. Each carries `status`, `type`, `code`,
`message`, `request_id`, `headers` and `body`. Branch on `code`; quote
`request_id` to Talki.

```python
from talki import ConflictError

try:
    unwrap(create_appointment.sync_detailed(client=talki.client, body=booking))
except ConflictError as error:
    if error.code == "slot_unavailable":
        ...
```

## Retries

`Talki` retries, `max_retries` times (default 2):

- any request that never left (connection refused, connect or pool timeout);
- any request answered 429 or `409 request_in_progress`, which the API turns
  away before running it;
- a read answered 500, 502, 503 or 504, or whose connection broke after sending;
- a write with an `Idempotency-Key` answered 502, 503 or 504 by a gateway (not
  the API's error envelope).

Never retried: a write the API itself answered with a 5xx, or whose connection
broke after sending (a read timeout among them), since either may come after
the write was saved. Its key keeps a repeat from applying it twice: the API
answers the key of a write that saved and then failed with that same 500 for
24 hours, and releases a key only when nothing was saved. Read the resource to
learn which happened before writing again.

It waits as `Retry-After` asks, up to 60 seconds; an answer asking for longer
is not retried but returned, as `RateLimitError` (with `retry_after`) for a 429.
Without `Retry-After` it backs off exponentially with jitter. `timeout` applies
to each attempt. `max_retries=0` turns retries off.

## Enums

A set of values whose description says "New values may be added" is a plain
`str` here; handle a value you do not know. Every other set is a `StrEnum`, and
gains a value only with a new dated version. Even so, a value an enum does not
list still parses: it is an instance of the enum, equal to its string, with a
name like a listed member's, so a response is never refused for it.

- To tell a listed value from another, use `value in list(SomeEnum)`, never
  `value in SomeEnum`: for an unlisted value the latter differs between Python
  versions.
- Enums in requests are not checked here either: an unlisted value is sent, and
  the API answers `400 invalid_parameter`.

## Version and idempotency

- `Talki` sends `Talki-Version: talki.API_VERSION`, the contract this package
  was generated from. `Talki(version="…")` pins another, and `version=None`
  sends none, so the version pinned on the key or app applies. Each operation
  also takes `talki_version=` for one request.
- `Talki` gives every write without an `Idempotency-Key` a new one, so its own
  retries are never applied twice. To retry a write yourself with the same key,
  pass your own with `idempotency_key=` (`talki.new_idempotency_key()` makes
  one); after an httpx error the key sent is
  also in `error.request.headers["Idempotency-Key"]`. `409 request_in_progress`
  means the first request with that key is still running and its outcome is
  unknown: retry later with the same key. `auto_idempotency=False` sends none
  unless given. Operations that require a key take it as optional here:
  without `Talki`, omitting it is refused with `400 idempotency_key_required`.
- `Talki(proxy="http://…")` sends every request through a proxy; the proxy
  environment variables are not read.

## Paging and feeds

Operations that take `cursor=` return `data`, `has_more` and `next_cursor`.
`talki.pagination` walks them: pass the operation's `sync_detailed` (or
`asyncio_detailed` to `apages`) and its arguments.

```python
from talki.pagination import pages, position, rows
from talki.api.calls import list_calls
from talki.api.appointments import list_appointments

for call in rows(pages(list_calls.sync_detailed, client=talki.client, limit=100)):
    ...

for page in pages(list_appointments.sync_detailed, client=talki.client, cursor=stored):
    save(page.data)
    stored = position(page, stored)  # store it with the rows
```

`pages` stops when `has_more` is false, raises the `ApiError` of a page that
fails after yielding those before it, and keeps each page's row type. A page
that says `has_more` but gives no new cursor raises `PaginationError`.
`position` is for change feeds: a plain list's last page has no cursor though
it holds rows.

The change feeds (appointments, contacts, services, resources, unresolved
requests, and calls with `sync=True`) return `next_cursor` on every non-empty
page, the last included: store every non-null one and resume from it. Keep the
filters the same for a whole walk. A cursor used with another `location_id` is
refused; any other changed filter is accepted and skips the rows the first
walk filtered out.

## Webhooks

A webhook endpoint and an app's `events_url` receive events signed in
`X-Talki-Signature`. Check it on the raw body, before parsing:

```python
from talki.webhooks import SignatureVerificationError, construct_event, signature_of

try:
    event = construct_event(raw_body, signature_of(headers), secret)
except SignatureVerificationError:
    ...  # answer 400 and ignore it
```

- `construct_event` returns the envelope as a dict; `verify_signature` only
  checks. Both take the body as the bytes received (a `str` is refused), and
  refuse a signature more than 300 seconds from now.
- `signature_of(headers)` finds the header whatever its case.
- While a secret is rotated with an overlap, either secret verifies; pass a list
  when you hold more than one.
- Deliveries are not ordered and may repeat: deduplicate on the event's `id`,
  and order changes to one object by its `updated_at`. An account that also
  has its own webhook endpoint at the same URL sends the same change twice,
  with different `id`s.

## OAuth apps

`talki.oauth` covers an app installed on Talki accounts: the consent URL with
PKCE, the callback, the code exchange, refresh and revocation, and a pair that
renews itself.

```python
import secrets
from talki import Talki
from talki.oauth import OAuthApp, Pkce, authorization_url, read_callback

app = OAuthApp(client_id, client_secret)  # base_url=…, for another deployment
pkce, state = Pkce.new(), secrets.token_urlsafe(16)
url = authorization_url(client_id, redirect_uri, ["calls:read"], state=state, pkce=pkce)
# … send the customer's browser to url; then, on the callback:
code = read_callback(callback_url, state=state)
tokens = app.exchange_code(code, redirect_uri=redirect_uri, code_verifier=pkce.verifier)
save(tokens)

talki = Talki(tokens=tokens, oauth_app=app, on_token_refresh=save)
```

- With `oauth_app`, `Talki` renews the pair a minute before it expires, and
  when the API answers `401` with `error="invalid_token"`, then sends the
  request again. `talki.tokens` is the pair in use (a new one waiting to be
  stored is not in use yet). `oauth_app` must talk to the same `base_url` as
  `Talki`.
- **The refresh token rotates on every renewal, and presenting a rotated one
  again revokes the installation.** One `Talki` serialises its renewals across
  threads, event loops and sync and async calls. Keep one `Talki` per
  installation per process, and never renew one pair from two of them.
- A renewal whose outcome is unknown (its answer lost or timed out, or a
  gateway's 502, 503 or 504) may have rotated the pair. The server takes the
  same refresh token once more within 60 seconds of that rotation, so `Talki`
  presents it again in the same request, 10 seconds after the outcome was
  lost (so as not to overlap the first), while that is still inside the 60
  seconds. When it is not (a `timeout` above 45 seconds), the request raises and
  the next one presents it again, which works only if the first never reached
  the server: otherwise the customer has to reconnect.
- Never call the same `Talki` from `on_token_refresh`, nor synchronously from
  async code that uses it: either would wait on its own renewal, so it raises
  `RuntimeError` instead.
- `on_token_refresh` is called with the new pair before it is used: store it
  there. If it raises, the pair stays pending in memory and every request
  raises until a later call stores it; the replaced refresh token is never
  presented again. A process that ends with a pair unstored can renew once more
  with the old refresh token within 60 seconds; after that the customer has to
  reconnect.
- Once the API refuses the refresh token (`invalid_grant`: the customer
  disconnected, the pair was revoked, or Talki disabled the app) or the app's
  credentials
  (`invalid_client`), every request raises that `OAuthError` without asking
  again. Build a new `Talki` once fixed.
- A code works once: never retry `exchange_code` with the same code.
- The token endpoints answer in RFC 6749's shape, raised as `OAuthError`
  (`error`, `description`, `status`).
- Against another deployment, pass its addresses: `OAuthApp(base_url=…)`,
  `Talki(base_url=…)`, `authorization_url(authorize_url=…)` and
  `read_callback(issuer=…)`.

## Not covered yet

The partner routes (`/oauth/app/*`, `/oauth/managed-accounts`,
`/oauth/enrollments`) and typed webhook event payloads are not in the OpenAPI
document yet, so not in this package. See the
[API reference](https://developers.talki.it) for them.

## Versions

This package follows semantic versioning of its own. `talki.API_VERSION` is
the dated API version it was generated from and sends by default; a release
that moves to a newer API version says so in the changelog.

## Development

Most of `talki/` is generated, never edited by hand: `scripts/generate.py`
runs openapi-python-client (pinned in `pyproject.toml`) over
`openapi/talki-v1.yaml` with the templates in `codegen/templates/`, and keeps
the hand-written modules listed in the script (`_talki.py`, `_transport.py`,
`exceptions.py`, `oauth.py`, `pagination.py`, `webhooks.py`).

```sh
uv sync
uv run scripts/pull_spec.py        # fetch the current OpenAPI document
uv run scripts/generate.py         # regenerate talki/ from it
uv run scripts/generate.py --check # CI: fail if talki/ is stale
uv run pytest
uv run mypy
uv run ruff check . && uv run ruff format --check .
```

To change generated code, change a template or `codegen/config.yaml`; a
change to the API itself belongs in the API.

## License

[MIT](https://github.com/HubtecSrl/talki-python/blob/main/LICENSE)
