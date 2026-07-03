from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_groups_bulk_add_body import PostPanelApiClientsGroupsBulkAddBody
from ...models.post_panel_api_clients_groups_bulk_add_response_200 import PostPanelApiClientsGroupsBulkAddResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsGroupsBulkAddBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/groups/bulkAdd",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsGroupsBulkAddResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsGroupsBulkAddResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsGroupsBulkAddResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkAddBody,
) -> Response[PostPanelApiClientsGroupsBulkAddResponse200]:
    """Add many clients to a group in one call. Updates clients.group_name and patches the matching client
    entry inside every owning inbound's settings JSON in a single transaction. If the group name does
    not yet exist (in client_groups or as a derived label), it is auto-created as a persistent group. To
    clear the group label, use /groups/bulkRemove instead.

    Args:
        body (PostPanelApiClientsGroupsBulkAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsBulkAddResponse200]
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
    body: PostPanelApiClientsGroupsBulkAddBody,
) -> PostPanelApiClientsGroupsBulkAddResponse200 | None:
    """Add many clients to a group in one call. Updates clients.group_name and patches the matching client
    entry inside every owning inbound's settings JSON in a single transaction. If the group name does
    not yet exist (in client_groups or as a derived label), it is auto-created as a persistent group. To
    clear the group label, use /groups/bulkRemove instead.

    Args:
        body (PostPanelApiClientsGroupsBulkAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsBulkAddResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkAddBody,
) -> Response[PostPanelApiClientsGroupsBulkAddResponse200]:
    """Add many clients to a group in one call. Updates clients.group_name and patches the matching client
    entry inside every owning inbound's settings JSON in a single transaction. If the group name does
    not yet exist (in client_groups or as a derived label), it is auto-created as a persistent group. To
    clear the group label, use /groups/bulkRemove instead.

    Args:
        body (PostPanelApiClientsGroupsBulkAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsBulkAddResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsBulkAddBody,
) -> PostPanelApiClientsGroupsBulkAddResponse200 | None:
    """Add many clients to a group in one call. Updates clients.group_name and patches the matching client
    entry inside every owning inbound's settings JSON in a single transaction. If the group name does
    not yet exist (in client_groups or as a derived label), it is auto-created as a persistent group. To
    clear the group label, use /groups/bulkRemove instead.

    Args:
        body (PostPanelApiClientsGroupsBulkAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsBulkAddResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
