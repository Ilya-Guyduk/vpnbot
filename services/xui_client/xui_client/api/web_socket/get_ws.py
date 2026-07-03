from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_ws_response_200 import GetWsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ws",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> GetWsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetWsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[GetWsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetWsResponse200]:
    """Upgrade an HTTP connection to a WebSocket. Requires an authenticated session cookie (Bearer token
    auth is not supported here). Returns 101 Switching Protocols on success. The server then pushes JSON
    messages described below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> GetWsResponse200 | None:
    """Upgrade an HTTP connection to a WebSocket. Requires an authenticated session cookie (Bearer token
    auth is not supported here). Returns 101 Switching Protocols on success. The server then pushes JSON
    messages described below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetWsResponse200]:
    """Upgrade an HTTP connection to a WebSocket. Requires an authenticated session cookie (Bearer token
    auth is not supported here). Returns 101 Switching Protocols on success. The server then pushes JSON
    messages described below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> GetWsResponse200 | None:
    """Upgrade an HTTP connection to a WebSocket. Requires an authenticated session cookie (Bearer token
    auth is not supported here). Returns 101 Switching Protocols on success. The server then pushes JSON
    messages described below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
