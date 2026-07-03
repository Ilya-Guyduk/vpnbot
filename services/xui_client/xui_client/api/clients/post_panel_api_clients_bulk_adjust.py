from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_bulk_adjust_body import PostPanelApiClientsBulkAdjustBody
from ...models.post_panel_api_clients_bulk_adjust_response_200 import PostPanelApiClientsBulkAdjustResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsBulkAdjustBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/bulkAdjust",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsBulkAdjustResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsBulkAdjustResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsBulkAdjustResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAdjustBody,
) -> Response[PostPanelApiClientsBulkAdjustResponse200]:
    r"""Shift expiry and/or traffic quota for many clients in one call. addDays/addBytes may be negative.
    Clients with unlimited expiry (expiryTime=0) or unlimited traffic (totalGB=0) are skipped for the
    corresponding field — bulk extend never converts unlimited to limited. The optional flow directive
    sets the XTLS flow on every client: \"none\" clears it, \"xtls-rprx-vision\"/\"xtls-rprx-vision-
    udp443\" set it where the inbound supports it (omit or \"\" to leave it unchanged). Returns the
    adjusted count and per-email skip reasons.

    Args:
        body (PostPanelApiClientsBulkAdjustBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkAdjustResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAdjustBody,
) -> PostPanelApiClientsBulkAdjustResponse200 | None:
    r"""Shift expiry and/or traffic quota for many clients in one call. addDays/addBytes may be negative.
    Clients with unlimited expiry (expiryTime=0) or unlimited traffic (totalGB=0) are skipped for the
    corresponding field — bulk extend never converts unlimited to limited. The optional flow directive
    sets the XTLS flow on every client: \"none\" clears it, \"xtls-rprx-vision\"/\"xtls-rprx-vision-
    udp443\" set it where the inbound supports it (omit or \"\" to leave it unchanged). Returns the
    adjusted count and per-email skip reasons.

    Args:
        body (PostPanelApiClientsBulkAdjustBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkAdjustResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAdjustBody,
) -> Response[PostPanelApiClientsBulkAdjustResponse200]:
    r"""Shift expiry and/or traffic quota for many clients in one call. addDays/addBytes may be negative.
    Clients with unlimited expiry (expiryTime=0) or unlimited traffic (totalGB=0) are skipped for the
    corresponding field — bulk extend never converts unlimited to limited. The optional flow directive
    sets the XTLS flow on every client: \"none\" clears it, \"xtls-rprx-vision\"/\"xtls-rprx-vision-
    udp443\" set it where the inbound supports it (omit or \"\" to leave it unchanged). Returns the
    adjusted count and per-email skip reasons.

    Args:
        body (PostPanelApiClientsBulkAdjustBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkAdjustResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAdjustBody,
) -> PostPanelApiClientsBulkAdjustResponse200 | None:
    r"""Shift expiry and/or traffic quota for many clients in one call. addDays/addBytes may be negative.
    Clients with unlimited expiry (expiryTime=0) or unlimited traffic (totalGB=0) are skipped for the
    corresponding field — bulk extend never converts unlimited to limited. The optional flow directive
    sets the XTLS flow on every client: \"none\" clears it, \"xtls-rprx-vision\"/\"xtls-rprx-vision-
    udp443\" set it where the inbound supports it (omit or \"\" to leave it unchanged). Returns the
    adjusted count and per-email skip reasons.

    Args:
        body (PostPanelApiClientsBulkAdjustBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkAdjustResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
