from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_del_email_response_200 import PostPanelApiClientsDelEmailResponse200
from ...types import UNSET, Response


def _get_kwargs(
    email: str,
    *,
    keep_traffic: int,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["keepTraffic"] = keep_traffic

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/del/{email}".format(
            email=quote(str(email), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsDelEmailResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsDelEmailResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsDelEmailResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    keep_traffic: int,
) -> Response[PostPanelApiClientsDelEmailResponse200]:
    """Delete a client by email. Removes it from every attached inbound and drops its traffic record unless
    keepTraffic=1 is passed.

    Args:
        email (str):
        keep_traffic (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelEmailResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        keep_traffic=keep_traffic,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    keep_traffic: int,
) -> PostPanelApiClientsDelEmailResponse200 | None:
    """Delete a client by email. Removes it from every attached inbound and drops its traffic record unless
    keepTraffic=1 is passed.

    Args:
        email (str):
        keep_traffic (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelEmailResponse200
    """

    return sync_detailed(
        email=email,
        client=client,
        keep_traffic=keep_traffic,
    ).parsed


async def asyncio_detailed(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    keep_traffic: int,
) -> Response[PostPanelApiClientsDelEmailResponse200]:
    """Delete a client by email. Removes it from every attached inbound and drops its traffic record unless
    keepTraffic=1 is passed.

    Args:
        email (str):
        keep_traffic (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsDelEmailResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        keep_traffic=keep_traffic,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    keep_traffic: int,
) -> PostPanelApiClientsDelEmailResponse200 | None:
    """Delete a client by email. Removes it from every attached inbound and drops its traffic record unless
    keepTraffic=1 is passed.

    Args:
        email (str):
        keep_traffic (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsDelEmailResponse200
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
            keep_traffic=keep_traffic,
        )
    ).parsed
