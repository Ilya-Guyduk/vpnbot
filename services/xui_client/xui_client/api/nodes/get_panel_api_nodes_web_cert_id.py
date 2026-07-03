from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_nodes_web_cert_id_response_200 import GetPanelApiNodesWebCertIdResponse200
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/nodes/webCert/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiNodesWebCertIdResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiNodesWebCertIdResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiNodesWebCertIdResponse200]:
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
) -> Response[GetPanelApiNodesWebCertIdResponse200]:
    r"""Fetch a node's own web TLS certificate/key file paths (proxied to the node). Used by the inbound
    form's \"Set Cert from Panel\" so a node-assigned inbound gets paths that exist on the node, not the
    central panel.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiNodesWebCertIdResponse200]
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
) -> GetPanelApiNodesWebCertIdResponse200 | None:
    r"""Fetch a node's own web TLS certificate/key file paths (proxied to the node). Used by the inbound
    form's \"Set Cert from Panel\" so a node-assigned inbound gets paths that exist on the node, not the
    central panel.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiNodesWebCertIdResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiNodesWebCertIdResponse200]:
    r"""Fetch a node's own web TLS certificate/key file paths (proxied to the node). Used by the inbound
    form's \"Set Cert from Panel\" so a node-assigned inbound gets paths that exist on the node, not the
    central panel.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiNodesWebCertIdResponse200]
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
) -> GetPanelApiNodesWebCertIdResponse200 | None:
    r"""Fetch a node's own web TLS certificate/key file paths (proxied to the node). Used by the inbound
    form's \"Set Cert from Panel\" so a node-assigned inbound gets paths that exist on the node, not the
    central panel.

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiNodesWebCertIdResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
