from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_active_inbounds_response_200 import PostPanelApiClientsActiveInboundsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/activeInbounds",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsActiveInboundsResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsActiveInboundsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsActiveInboundsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsActiveInboundsResponse200]:
    """Inbound tags that carried traffic within the heartbeat window, grouped by the hosting node's
    panelGuid. Pairs with onlinesByGuid so the inbounds page only marks a multi-inbound client online on
    the inbounds it actually used. Nodes that do not report per-inbound activity are absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsActiveInboundsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsActiveInboundsResponse200 | None:
    """Inbound tags that carried traffic within the heartbeat window, grouped by the hosting node's
    panelGuid. Pairs with onlinesByGuid so the inbounds page only marks a multi-inbound client online on
    the inbounds it actually used. Nodes that do not report per-inbound activity are absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsActiveInboundsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsActiveInboundsResponse200]:
    """Inbound tags that carried traffic within the heartbeat window, grouped by the hosting node's
    panelGuid. Pairs with onlinesByGuid so the inbounds page only marks a multi-inbound client online on
    the inbounds it actually used. Nodes that do not report per-inbound activity are absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsActiveInboundsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsActiveInboundsResponse200 | None:
    """Inbound tags that carried traffic within the heartbeat window, grouped by the hosting node's
    panelGuid. Pairs with onlinesByGuid so the inbounds page only marks a multi-inbound client online on
    the inbounds it actually used. Nodes that do not report per-inbound activity are absent.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsActiveInboundsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
