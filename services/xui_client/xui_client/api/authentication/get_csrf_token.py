from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_csrf_token_response_200 import GetCsrfTokenResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/csrf-token",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetCsrfTokenResponse200 | None:
    if response.status_code == 200:
        response_200 = GetCsrfTokenResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetCsrfTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetCsrfTokenResponse200]:
    """Mint a CSRF token for the current session. The SPA replays it in the X-CSRF-Token header on unsafe
    requests. Bearer-token callers can skip this — the middleware short-circuits CSRF for authenticated
    API requests.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetCsrfTokenResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> GetCsrfTokenResponse200 | None:
    """Mint a CSRF token for the current session. The SPA replays it in the X-CSRF-Token header on unsafe
    requests. Bearer-token callers can skip this — the middleware short-circuits CSRF for authenticated
    API requests.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetCsrfTokenResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetCsrfTokenResponse200]:
    """Mint a CSRF token for the current session. The SPA replays it in the X-CSRF-Token header on unsafe
    requests. Bearer-token callers can skip this — the middleware short-circuits CSRF for authenticated
    API requests.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetCsrfTokenResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> GetCsrfTokenResponse200 | None:
    """Mint a CSRF token for the current session. The SPA replays it in the X-CSRF-Token header on unsafe
    requests. Bearer-token callers can skip this — the middleware short-circuits CSRF for authenticated
    API requests.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetCsrfTokenResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
