from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_inbounds_id_fallbacks_response_200 import GetPanelApiInboundsIdFallbacksResponse200
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/inbounds/{id}/fallbacks".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiInboundsIdFallbacksResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiInboundsIdFallbacksResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiInboundsIdFallbacksResponse200]:
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
) -> Response[GetPanelApiInboundsIdFallbacksResponse200]:
    """List the fallback rules attached to a master VLESS/Trojan TCP-TLS inbound. Each rule links one child
    inbound (the dest) to optional SNI/ALPN/path/dest/xver match criteria. When dest is empty the child
    inbound's listen+port is used.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiInboundsIdFallbacksResponse200]
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
) -> GetPanelApiInboundsIdFallbacksResponse200 | None:
    """List the fallback rules attached to a master VLESS/Trojan TCP-TLS inbound. Each rule links one child
    inbound (the dest) to optional SNI/ALPN/path/dest/xver match criteria. When dest is empty the child
    inbound's listen+port is used.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiInboundsIdFallbacksResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiInboundsIdFallbacksResponse200]:
    """List the fallback rules attached to a master VLESS/Trojan TCP-TLS inbound. Each rule links one child
    inbound (the dest) to optional SNI/ALPN/path/dest/xver match criteria. When dest is empty the child
    inbound's listen+port is used.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiInboundsIdFallbacksResponse200]
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
) -> GetPanelApiInboundsIdFallbacksResponse200 | None:
    """List the fallback rules attached to a master VLESS/Trojan TCP-TLS inbound. Each rule links one child
    inbound (the dest) to optional SNI/ALPN/path/dest/xver match criteria. When dest is empty the child
    inbound's listen+port is used.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiInboundsIdFallbacksResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
