from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_clients_sub_links_sub_id_response_200 import GetPanelApiClientsSubLinksSubIdResponse200
from ...types import Response


def _get_kwargs(
    sub_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/clients/subLinks/{sub_id}".format(
            sub_id=quote(str(sub_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiClientsSubLinksSubIdResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiClientsSubLinksSubIdResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiClientsSubLinksSubIdResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sub_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiClientsSubLinksSubIdResponse200]:
    """Return every protocol URL (vless://, vmess://, trojan://, ss://, hysteria://, hy2://) for clients
    matching the subscription ID. Same result set as /sub/<subId>, but as a JSON array — no base64. When
    an inbound has streamSettings.externalProxy set, one URL is emitted per external proxy. Empty array
    when the subId has no enabled clients.

    Args:
        sub_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsSubLinksSubIdResponse200]
    """

    kwargs = _get_kwargs(
        sub_id=sub_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sub_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiClientsSubLinksSubIdResponse200 | None:
    """Return every protocol URL (vless://, vmess://, trojan://, ss://, hysteria://, hy2://) for clients
    matching the subscription ID. Same result set as /sub/<subId>, but as a JSON array — no base64. When
    an inbound has streamSettings.externalProxy set, one URL is emitted per external proxy. Empty array
    when the subId has no enabled clients.

    Args:
        sub_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsSubLinksSubIdResponse200
    """

    return sync_detailed(
        sub_id=sub_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sub_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiClientsSubLinksSubIdResponse200]:
    """Return every protocol URL (vless://, vmess://, trojan://, ss://, hysteria://, hy2://) for clients
    matching the subscription ID. Same result set as /sub/<subId>, but as a JSON array — no base64. When
    an inbound has streamSettings.externalProxy set, one URL is emitted per external proxy. Empty array
    when the subId has no enabled clients.

    Args:
        sub_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsSubLinksSubIdResponse200]
    """

    kwargs = _get_kwargs(
        sub_id=sub_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sub_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiClientsSubLinksSubIdResponse200 | None:
    """Return every protocol URL (vless://, vmess://, trojan://, ss://, hysteria://, hy2://) for clients
    matching the subscription ID. Same result set as /sub/<subId>, but as a JSON array — no base64. When
    an inbound has streamSettings.externalProxy set, one URL is emitted per external proxy. Empty array
    when the subId has no enabled clients.

    Args:
        sub_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsSubLinksSubIdResponse200
    """

    return (
        await asyncio_detailed(
            sub_id=sub_id,
            client=client,
        )
    ).parsed
