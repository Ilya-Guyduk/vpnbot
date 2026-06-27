from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_clients_get_email_response_200 import GetPanelApiClientsGetEmailResponse200
from ...types import Response


def _get_kwargs(
    email: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/clients/get/{email}".format(
            email=quote(str(email), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiClientsGetEmailResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiClientsGetEmailResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiClientsGetEmailResponse200]:
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
) -> Response[GetPanelApiClientsGetEmailResponse200]:
    """Fetch one client by email, including the inbound IDs and external config IDs it is attached to.

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsGetEmailResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiClientsGetEmailResponse200 | None:
    """Fetch one client by email, including the inbound IDs and external config IDs it is attached to.

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsGetEmailResponse200
    """

    return sync_detailed(
        email=email,
        client=client,
    ).parsed


async def asyncio_detailed(
    email: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiClientsGetEmailResponse200]:
    """Fetch one client by email, including the inbound IDs and external config IDs it is attached to.

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsGetEmailResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiClientsGetEmailResponse200 | None:
    """Fetch one client by email, including the inbound IDs and external config IDs it is attached to.

    Args:
        email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsGetEmailResponse200
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
        )
    ).parsed
