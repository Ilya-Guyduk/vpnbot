from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_inbounds_id_del_all_clients_response_200 import (
    PostPanelApiInboundsIdDelAllClientsResponse200,
)
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/inbounds/{id}/delAllClients".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiInboundsIdDelAllClientsResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiInboundsIdDelAllClientsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiInboundsIdDelAllClientsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiInboundsIdDelAllClientsResponse200]:
    """Remove every client attached to a single inbound while keeping the inbound itself. Collects emails
    from settings.clients[] and feeds them into the optimized bulk-delete path (runtime user removal +
    traffic-row cleanup + SyncInbound). Destructive and cannot be undone.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiInboundsIdDelAllClientsResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiInboundsIdDelAllClientsResponse200 | None:
    """Remove every client attached to a single inbound while keeping the inbound itself. Collects emails
    from settings.clients[] and feeds them into the optimized bulk-delete path (runtime user removal +
    traffic-row cleanup + SyncInbound). Destructive and cannot be undone.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiInboundsIdDelAllClientsResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiInboundsIdDelAllClientsResponse200]:
    """Remove every client attached to a single inbound while keeping the inbound itself. Collects emails
    from settings.clients[] and feeds them into the optimized bulk-delete path (runtime user removal +
    traffic-row cleanup + SyncInbound). Destructive and cannot be undone.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiInboundsIdDelAllClientsResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiInboundsIdDelAllClientsResponse200 | None:
    """Remove every client attached to a single inbound while keeping the inbound itself. Collects emails
    from settings.clients[] and feeds them into the optimized bulk-delete path (runtime user removal +
    traffic-row cleanup + SyncInbound). Destructive and cannot be undone.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiInboundsIdDelAllClientsResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
