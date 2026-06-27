from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_groups_delete_body import PostPanelApiClientsGroupsDeleteBody
from ...models.post_panel_api_clients_groups_delete_response_200 import PostPanelApiClientsGroupsDeleteResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsGroupsDeleteBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/groups/delete",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsGroupsDeleteResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsGroupsDeleteResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsGroupsDeleteResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsDeleteBody,
) -> Response[PostPanelApiClientsGroupsDeleteResponse200]:
    """Remove a group. Deletes the client_groups row and clears the group label from every matching client
    (both clients.group_name and the inbound settings JSON). The clients themselves are NOT deleted —
    use /bulkDel after filtering by group for that. Returns the count of clients whose label was
    cleared.

    Args:
        body (PostPanelApiClientsGroupsDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsDeleteResponse200]
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
    body: PostPanelApiClientsGroupsDeleteBody,
) -> PostPanelApiClientsGroupsDeleteResponse200 | None:
    """Remove a group. Deletes the client_groups row and clears the group label from every matching client
    (both clients.group_name and the inbound settings JSON). The clients themselves are NOT deleted —
    use /bulkDel after filtering by group for that. Returns the count of clients whose label was
    cleared.

    Args:
        body (PostPanelApiClientsGroupsDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsDeleteResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsDeleteBody,
) -> Response[PostPanelApiClientsGroupsDeleteResponse200]:
    """Remove a group. Deletes the client_groups row and clears the group label from every matching client
    (both clients.group_name and the inbound settings JSON). The clients themselves are NOT deleted —
    use /bulkDel after filtering by group for that. Returns the count of clients whose label was
    cleared.

    Args:
        body (PostPanelApiClientsGroupsDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsGroupsDeleteResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsGroupsDeleteBody,
) -> PostPanelApiClientsGroupsDeleteResponse200 | None:
    """Remove a group. Deletes the client_groups row and clears the group label from every matching client
    (both clients.group_name and the inbound settings JSON). The clients themselves are NOT deleted —
    use /bulkDel after filtering by group for that. Returns the count of clients whose label was
    cleared.

    Args:
        body (PostPanelApiClientsGroupsDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsGroupsDeleteResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
