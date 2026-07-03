from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_del_orphans_response_200 import PostPanelApiClientsDelOrphansResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/delOrphans",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsDelOrphansResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsDelOrphansResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsDelOrphansResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsDelOrphansResponse200]:
    """Delete every client that is not attached to any inbound, along with its traffic record, IP log, and
    external links. Useful for clearing clients left unattached after their inbounds were removed.
    Returns the deleted count. Cannot be undone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelOrphansResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsDelOrphansResponse200 | None:
    """Delete every client that is not attached to any inbound, along with its traffic record, IP log, and
    external links. Useful for clearing clients left unattached after their inbounds were removed.
    Returns the deleted count. Cannot be undone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelOrphansResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsDelOrphansResponse200]:
    """Delete every client that is not attached to any inbound, along with its traffic record, IP log, and
    external links. Useful for clearing clients left unattached after their inbounds were removed.
    Returns the deleted count. Cannot be undone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelOrphansResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsDelOrphansResponse200 | None:
    """Delete every client that is not attached to any inbound, along with its traffic record, IP log, and
    external links. Useful for clearing clients left unattached after their inbounds were removed.
    Returns the deleted count. Cannot be undone.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelOrphansResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
