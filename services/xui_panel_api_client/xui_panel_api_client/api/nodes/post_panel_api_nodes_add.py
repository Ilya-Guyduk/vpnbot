from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_nodes_add_body import PostPanelApiNodesAddBody
from ...models.post_panel_api_nodes_add_response_200 import PostPanelApiNodesAddResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiNodesAddBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/nodes/add",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiNodesAddResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiNodesAddResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiNodesAddResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesAddBody,
) -> Response[PostPanelApiNodesAddResponse200]:
    """Register a new remote node. Provide its URL, apiToken, and optional remark / allowPrivateAddress
    flag.

    Args:
        body (PostPanelApiNodesAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesAddResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesAddBody,
) -> PostPanelApiNodesAddResponse200 | None:
    """Register a new remote node. Provide its URL, apiToken, and optional remark / allowPrivateAddress
    flag.

    Args:
        body (PostPanelApiNodesAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesAddResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesAddBody,
) -> Response[PostPanelApiNodesAddResponse200]:
    """Register a new remote node. Provide its URL, apiToken, and optional remark / allowPrivateAddress
    flag.

    Args:
        body (PostPanelApiNodesAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesAddResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesAddBody,
) -> PostPanelApiNodesAddResponse200 | None:
    """Register a new remote node. Provide its URL, apiToken, and optional remark / allowPrivateAddress
    flag.

    Args:
        body (PostPanelApiNodesAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesAddResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
