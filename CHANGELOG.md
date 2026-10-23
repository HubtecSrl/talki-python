# Changelog

This package follows [semantic versioning](https://semver.org). The API
version each release targets by default is `talki.API_VERSION`.

## 0.1.0b1 — unreleased

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
