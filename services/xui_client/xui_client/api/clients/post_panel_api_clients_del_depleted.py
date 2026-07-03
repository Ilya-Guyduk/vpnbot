from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_del_depleted_response_200 import PostPanelApiClientsDelDepletedResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/delDepleted",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsDelDepletedResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsDelDepletedResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsDelDepletedResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsDelDepletedResponse200]:
    """Delete every client whose traffic quota is exhausted (used >= total, when reset is disabled) or
    whose expiry has passed. Returns the deleted count and triggers an Xray restart when any client was
    on a running inbound.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelDepletedResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsDelDepletedResponse200 | None:
    """Delete every client whose traffic quota is exhausted (used >= total, when reset is disabled) or
    whose expiry has passed. Returns the deleted count and triggers an Xray restart when any client was
    on a running inbound.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelDepletedResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiClientsDelDepletedResponse200]:
    """Delete every client whose traffic quota is exhausted (used >= total, when reset is disabled) or
    whose expiry has passed. Returns the deleted count and triggers an Xray restart when any client was
    on a running inbound.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelDepletedResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiClientsDelDepletedResponse200 | None:
    """Delete every client whose traffic quota is exhausted (used >= total, when reset is disabled) or
    whose expiry has passed. Returns the deleted count and triggers an Xray restart when any client was
    on a running inbound.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelDepletedResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
