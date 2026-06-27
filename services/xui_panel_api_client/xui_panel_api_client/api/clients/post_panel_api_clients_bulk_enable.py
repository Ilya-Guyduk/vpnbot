from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_bulk_enable_body import PostPanelApiClientsBulkEnableBody
from ...models.post_panel_api_clients_bulk_enable_response_200 import PostPanelApiClientsBulkEnableResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsBulkEnableBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/bulkEnable",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsBulkEnableResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsBulkEnableResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsBulkEnableResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkEnableBody,
) -> Response[PostPanelApiClientsBulkEnableResponse200]:
    """Enable many clients in one call. Emails are grouped by inbound and applied with a single read-
    modify-write per inbound; the running Xray (local or remote node) is updated to add each user. Note
    that enabling a client whose quota is exhausted or whose expiry has passed only flips the flag — the
    traffic loop will disable it again on the next tick. Returns the changed count and per-email skip
    reasons.

    Args:
        body (PostPanelApiClientsBulkEnableBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkEnableResponse200]
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
    body: PostPanelApiClientsBulkEnableBody,
) -> PostPanelApiClientsBulkEnableResponse200 | None:
    """Enable many clients in one call. Emails are grouped by inbound and applied with a single read-
    modify-write per inbound; the running Xray (local or remote node) is updated to add each user. Note
    that enabling a client whose quota is exhausted or whose expiry has passed only flips the flag — the
    traffic loop will disable it again on the next tick. Returns the changed count and per-email skip
    reasons.

    Args:
        body (PostPanelApiClientsBulkEnableBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkEnableResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkEnableBody,
) -> Response[PostPanelApiClientsBulkEnableResponse200]:
    """Enable many clients in one call. Emails are grouped by inbound and applied with a single read-
    modify-write per inbound; the running Xray (local or remote node) is updated to add each user. Note
    that enabling a client whose quota is exhausted or whose expiry has passed only flips the flag — the
    traffic loop will disable it again on the next tick. Returns the changed count and per-email skip
    reasons.

    Args:
        body (PostPanelApiClientsBulkEnableBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkEnableResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkEnableBody,
) -> PostPanelApiClientsBulkEnableResponse200 | None:
    """Enable many clients in one call. Emails are grouped by inbound and applied with a single read-
    modify-write per inbound; the running Xray (local or remote node) is updated to add each user. Note
    that enabling a client whose quota is exhausted or whose expiry has passed only flips the flag — the
    traffic loop will disable it again on the next tick. Returns the changed count and per-email skip
    reasons.

    Args:
        body (PostPanelApiClientsBulkEnableBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkEnableResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
