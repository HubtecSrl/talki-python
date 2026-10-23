import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.closure_list import ClosureList
from ...models.error_envelope import ErrorEnvelope
from ...models.list_closures_kind import ListClosuresKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    params: dict[str, Any] = {}

    json_from_: None | str | Unset
    if isinstance(from_, Unset):
        json_from_ = UNSET
    elif isinstance(from_, datetime.date):
        json_from_ = from_.isoformat()
    else:
        json_from_ = from_
    params["from"] = json_from_

    json_to: None | str | Unset
    if isinstance(to, Unset):
        json_to = UNSET
    elif isinstance(to, datetime.date):
        json_to = to.isoformat()
    else:
        json_to = to
    params["to"] = json_to

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    json_location_id: None | str | Unset
    if isinstance(location_id, Unset):
        json_location_id = UNSET
    else:
        json_location_id = location_id
    params["location_id"] = json_location_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/closures",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _is_envelope(response: httpx.Response) -> bool:
    """Whether an error answer is the API's `{"error": {…}}`."""
    if "json" not in response.headers.get("content-type", ""):
        return False
    try:
        body = response.json()
    except ValueError:
        return False
    return isinstance(body, dict) and isinstance(body.get("error"), dict)


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ClosureList | ErrorEnvelope | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 200:
        response_200 = ClosureList.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorEnvelope.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = ErrorEnvelope.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = ErrorEnvelope.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ClosureList | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ClosureList | ErrorEnvelope]:
    """List closures

     Return the closures, special openings or both overlapping a range of local days, earliest first, in
    one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
    that location, including those of every location. Requires `account:read`. Limited to 600 requests
    per minute per account (API key) or per installation (OAuth).

    Args:
        from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
        to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
            year after `from`. At most 366 days after `from`.
        kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
            openings, `all` for both. Default: ListClosuresKind.CLOSED.
        location_id (None | str | Unset): Only those that apply at this location, an id from `GET
            /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
            closure of every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClosureList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        kind=kind,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ClosureList | ErrorEnvelope | None:
    """List closures

     Return the closures, special openings or both overlapping a range of local days, earliest first, in
    one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
    that location, including those of every location. Requires `account:read`. Limited to 600 requests
    per minute per account (API key) or per installation (OAuth).

    Args:
        from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
        to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
            year after `from`. At most 366 days after `from`.
        kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
            openings, `all` for both. Default: ListClosuresKind.CLOSED.
        location_id (None | str | Unset): Only those that apply at this location, an id from `GET
            /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
            closure of every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClosureList | ErrorEnvelope
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
        kind=kind,
        location_id=location_id,
        talki_version=talki_version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> Response[ClosureList | ErrorEnvelope]:
    """List closures

     Return the closures, special openings or both overlapping a range of local days, earliest first, in
    one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
    that location, including those of every location. Requires `account:read`. Limited to 600 requests
    per minute per account (API key) or per installation (OAuth).

    Args:
        from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
        to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
            year after `from`. At most 366 days after `from`.
        kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
            openings, `all` for both. Default: ListClosuresKind.CLOSED.
        location_id (None | str | Unset): Only those that apply at this location, an id from `GET
            /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
            closure of every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClosureList | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
        kind=kind,
        location_id=location_id,
        talki_version=talki_version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    from_: datetime.date | None | Unset = UNSET,
    to: datetime.date | None | Unset = UNSET,
    kind: ListClosuresKind | Unset = ListClosuresKind.CLOSED,
    location_id: None | str | Unset = UNSET,
    talki_version: str | Unset = UNSET,
) -> ClosureList | ErrorEnvelope | None:
    """List closures

     Return the closures, special openings or both overlapping a range of local days, earliest first, in
    one page. Closures only unless `kind` says otherwise. With `location_id`, only those that apply at
    that location, including those of every location. Requires `account:read`. Limited to 600 requests
    per minute per account (API key) or per installation (OAuth).

    Args:
        from_ (datetime.date | None | Unset): First day to list, `YYYY-MM-DD`. Defaults to today.
        to (datetime.date | None | Unset): Last day to list, included, `YYYY-MM-DD`. Defaults to a
            year after `from`. At most 366 days after `from`.
        kind (ListClosuresKind | Unset): `closed` (the default) for closures, `open` for special
            openings, `all` for both. Default: ListClosuresKind.CLOSED.
        location_id (None | str | Unset): Only those that apply at this location, an id from `GET
            /v1/locations`: its own, and those of every location (`location_id` null). Omit for every
            closure of every location.
        talki_version (str | Unset):  Example: 2026-10-01.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClosureList | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
            kind=kind,
            location_id=location_id,
            talki_version=talki_version,
        )
    ).parsed
