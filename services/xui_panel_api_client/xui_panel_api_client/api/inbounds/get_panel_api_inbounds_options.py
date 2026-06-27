from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_inbounds_options_response_200 import GetPanelApiInboundsOptionsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/inbounds/options",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiInboundsOptionsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiInboundsOptionsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiInboundsOptionsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiInboundsOptionsResponse200]:
    """Lightweight picker projection of the authenticated user’s inbounds. Returns id, remark, tag,
    protocol, port, a server-computed tlsFlowCapable flag (true for VLESS on TCP with tls or reality, or
    on XHTTP with VLESS encryption / vlessenc enabled), and ssMethod (the Shadowsocks cipher, empty for
    non-Shadowsocks inbounds — used by the client UI to generate a valid Shadowsocks 2022 PSK). Use this
    for dropdowns and attach pickers — it skips settings, streamSettings, and clientStats so the payload
    stays small even on panels with thousands of clients.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiInboundsOptionsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiInboundsOptionsResponse200 | None:
    """Lightweight picker projection of the authenticated user’s inbounds. Returns id, remark, tag,
    protocol, port, a server-computed tlsFlowCapable flag (true for VLESS on TCP with tls or reality, or
    on XHTTP with VLESS encryption / vlessenc enabled), and ssMethod (the Shadowsocks cipher, empty for
    non-Shadowsocks inbounds — used by the client UI to generate a valid Shadowsocks 2022 PSK). Use this
    for dropdowns and attach pickers — it skips settings, streamSettings, and clientStats so the payload
    stays small even on panels with thousands of clients.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiInboundsOptionsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiInboundsOptionsResponse200]:
    """Lightweight picker projection of the authenticated user’s inbounds. Returns id, remark, tag,
    protocol, port, a server-computed tlsFlowCapable flag (true for VLESS on TCP with tls or reality, or
    on XHTTP with VLESS encryption / vlessenc enabled), and ssMethod (the Shadowsocks cipher, empty for
    non-Shadowsocks inbounds — used by the client UI to generate a valid Shadowsocks 2022 PSK). Use this
    for dropdowns and attach pickers — it skips settings, streamSettings, and clientStats so the payload
    stays small even on panels with thousands of clients.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiInboundsOptionsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiInboundsOptionsResponse200 | None:
    """Lightweight picker projection of the authenticated user’s inbounds. Returns id, remark, tag,
    protocol, port, a server-computed tlsFlowCapable flag (true for VLESS on TCP with tls or reality, or
    on XHTTP with VLESS encryption / vlessenc enabled), and ssMethod (the Shadowsocks cipher, empty for
    non-Shadowsocks inbounds — used by the client UI to generate a valid Shadowsocks 2022 PSK). Use this
    for dropdowns and attach pickers — it skips settings, streamSettings, and clientStats so the payload
    stays small even on panels with thousands of clients.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiInboundsOptionsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
