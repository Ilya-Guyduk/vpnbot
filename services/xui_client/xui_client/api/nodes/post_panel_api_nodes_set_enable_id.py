from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_nodes_set_enable_id_body import PostPanelApiNodesSetEnableIdBody
from ...models.post_panel_api_nodes_set_enable_id_response_200 import PostPanelApiNodesSetEnableIdResponse200
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: PostPanelApiNodesSetEnableIdBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/nodes/setEnable/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiNodesSetEnableIdResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiNodesSetEnableIdResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiNodesSetEnableIdResponse200]:
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
    body: PostPanelApiNodesSetEnableIdBody,
) -> Response[PostPanelApiNodesSetEnableIdResponse200]:
    """Pause or resume traffic sync with this node.

    Args:
        id (int):
        body (PostPanelApiNodesSetEnableIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesSetEnableIdResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesSetEnableIdBody,
) -> PostPanelApiNodesSetEnableIdResponse200 | None:
    """Pause or resume traffic sync with this node.

    Args:
        id (int):
        body (PostPanelApiNodesSetEnableIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesSetEnableIdResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesSetEnableIdBody,
) -> Response[PostPanelApiNodesSetEnableIdResponse200]:
    """Pause or resume traffic sync with this node.

    Args:
        id (int):
        body (PostPanelApiNodesSetEnableIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesSetEnableIdResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesSetEnableIdBody,
) -> PostPanelApiNodesSetEnableIdResponse200 | None:
    """Pause or resume traffic sync with this node.

    Args:
        id (int):
        body (PostPanelApiNodesSetEnableIdBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesSetEnableIdResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
