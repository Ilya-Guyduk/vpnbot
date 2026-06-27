from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_groups_bulk_remove_body import PostPanelApiClientsGroupsBulkRemoveBody
from ...models.post_panel_api_clients_groups_bulk_remove_response_200 import (
    PostPanelApiClientsGroupsBulkRemoveResponse200,
)
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsGroupsBulkRemoveBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/groups/bulkRemove",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsGroupsBulkRemoveResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsGroupsBulkRemoveResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsGroupsBulkRemoveResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkRemoveBody,
) -> Response[PostPanelApiClientsGroupsBulkRemoveResponse200]:
    """Clear the group label on many clients in one call. Inverse of /groups/bulkAdd. Clients themselves
    are kept — only the group label is cleared from clients.group_name and from each owning inbound's
    settings JSON. Groups become empty if all their members are removed.

    Args:
        body (PostPanelApiClientsGroupsBulkRemoveBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsBulkRemoveResponse200]
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
    body: PostPanelApiClientsGroupsBulkRemoveBody,
) -> PostPanelApiClientsGroupsBulkRemoveResponse200 | None:
    """Clear the group label on many clients in one call. Inverse of /groups/bulkAdd. Clients themselves
    are kept — only the group label is cleared from clients.group_name and from each owning inbound's
    settings JSON. Groups become empty if all their members are removed.

    Args:
        body (PostPanelApiClientsGroupsBulkRemoveBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsBulkRemoveResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkRemoveBody,
) -> Response[PostPanelApiClientsGroupsBulkRemoveResponse200]:
    """Clear the group label on many clients in one call. Inverse of /groups/bulkAdd. Clients themselves
    are kept — only the group label is cleared from clients.group_name and from each owning inbound's
    settings JSON. Groups become empty if all their members are removed.

    Args:
        body (PostPanelApiClientsGroupsBulkRemoveBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsBulkRemoveResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkRemoveBody,
) -> PostPanelApiClientsGroupsBulkRemoveResponse200 | None:
    """Clear the group label on many clients in one call. Inverse of /groups/bulkAdd. Clients themselves
    are kept — only the group label is cleared from clients.group_name and from each owning inbound's
    settings JSON. Groups become empty if all their members are removed.

    Args:
        body (PostPanelApiClientsGroupsBulkRemoveBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsBulkRemoveResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
