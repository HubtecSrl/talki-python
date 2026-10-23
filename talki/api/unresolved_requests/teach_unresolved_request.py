from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.unresolved_request_teach import UnresolvedRequestTeach
from ...models.unresolved_request_teaching import UnresolvedRequestTeaching
from ...types import UNSET, Response, Unset


def _get_kwargs(
    request_id: str,
    *,
    body: UnresolvedRequestTeach,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(talki_version, Unset):
        headers["Talki-Version"] = talki_version

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/unresolved_requests/{request_id}/teach".format(
            request_id=quote(str(request_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
) -> ErrorEnvelope | UnresolvedRequestTeaching | None:
    if response.status_code >= 400 and not _is_envelope(response):
        if client.raise_on_unexpected_status:
            raise errors.UnexpectedStatus(response.status_code, response.content)
        return None
    if response.status_code == 202:
        response_202 = UnresolvedRequestTeaching.from_dict(response.json())

        return response_202

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

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = ErrorEnvelope.from_dict(response.json())

        return response_413

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
) -> Response[ErrorEnvelope | UnresolvedRequestTeaching]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    request_id: str,
    *,
    client: AuthenticatedClient,
    body: UnresolvedRequestTeach,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UnresolvedRequestTeaching]:
    """Teach the assistant an answer

     Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
    caller: the request's location's, another location's, or every location's (`all`). The business
    sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
    business what to teach. The assistant uses the answer shortly after the `202`, once the note is
    indexed. Teaching the same request again adds another entry. Refused for a request that is not
    `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
    account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        request_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (UnresolvedRequestTeach): The general answer to a resolved request's question,
            written as the business would say it to any caller. It is added to a FAQ note the business
            sees and edits in Talki. It is not the request's `answer`, which records what one caller
            was told, and does not change it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UnresolvedRequestTeaching]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    request_id: str,
    *,
    client: AuthenticatedClient,
    body: UnresolvedRequestTeach,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | UnresolvedRequestTeaching | None:
    """Teach the assistant an answer

     Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
    caller: the request's location's, another location's, or every location's (`all`). The business
    sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
    business what to teach. The assistant uses the answer shortly after the `202`, once the note is
    indexed. Teaching the same request again adds another entry. Refused for a request that is not
    `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
    account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        request_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (UnresolvedRequestTeach): The general answer to a resolved request's question,
            written as the business would say it to any caller. It is added to a FAQ note the business
            sees and edits in Talki. It is not the request's `answer`, which records what one caller
            was told, and does not change it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UnresolvedRequestTeaching
    """

    return sync_detailed(
        request_id=request_id,
        client=client,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    request_id: str,
    *,
    client: AuthenticatedClient,
    body: UnresolvedRequestTeach,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | UnresolvedRequestTeaching]:
    """Teach the assistant an answer

     Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
    caller: the request's location's, another location's, or every location's (`all`). The business
    sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
    business what to teach. The assistant uses the answer shortly after the `202`, once the note is
    indexed. Teaching the same request again adds another entry. Refused for a request that is not
    `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
    account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        request_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (UnresolvedRequestTeach): The general answer to a resolved request's question,
            written as the business would say it to any caller. It is added to a FAQ note the business
            sees and edits in Talki. It is not the request's `answer`, which records what one caller
            was told, and does not change it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | UnresolvedRequestTeaching]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
        body=body,
        talki_version=talki_version,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    request_id: str,
    *,
    client: AuthenticatedClient,
    body: UnresolvedRequestTeach,
    talki_version: str | Unset = UNSET,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | UnresolvedRequestTeaching | None:
    """Teach the assistant an answer

     Add the general answer to a resolved request's question to a FAQ note the assistant uses with every
    caller: the request's location's, another location's, or every location's (`all`). The business
    sees, rewords and removes it in Talki, and nothing asks for its approval first, so agree with the
    business what to teach. The assistant uses the answer shortly after the `202`, once the note is
    indexed. Teaching the same request again adds another entry. Refused for a request that is not
    `resolved` (`unresolved_request_not_resolved`), when the note is full (`faq_full`) and when the
    account's knowledge storage is full (`payload_too_large`). Requires `Idempotency-Key`. Requires
    `knowledge:write`. Limited to 120 requests per minute per account (API key) or per installation
    (OAuth).

    Args:
        request_id (str):
        talki_version (str | Unset):  Example: 2026-10-01.
        idempotency_key (str | Unset): Required by this operation. Omitted, the request is refused
            unless the client adds one, as `talki.Talki` does.
        body (UnresolvedRequestTeach): The general answer to a resolved request's question,
            written as the business would say it to any caller. It is added to a FAQ note the business
            sees and edits in Talki. It is not the request's `answer`, which records what one caller
            was told, and does not change it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | UnresolvedRequestTeaching
    """

    return (
        await asyncio_detailed(
            request_id=request_id,
            client=client,
            body=body,
            talki_version=talki_version,
            idempotency_key=idempotency_key,
        )
    ).parsed
