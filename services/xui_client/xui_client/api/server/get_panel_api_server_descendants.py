from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_server_descendants_response_200 import GetPanelApiServerDescendantsResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/server/descendants",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiServerDescendantsResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiServerDescendantsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiServerDescendantsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerDescendantsResponse200]:
    """Read-only summaries (guid, parentGuid, name, address, status, versions) of the nodes this panel
    manages. A parent panel calls it on a node (via the node API token) to surface transitive sub-nodes
    in a chained topology. Counts are computed by the parent, not returned here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerDescendantsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerDescendantsResponse200 | None:
    """Read-only summaries (guid, parentGuid, name, address, status, versions) of the nodes this panel
    manages. A parent panel calls it on a node (via the node API token) to surface transitive sub-nodes
    in a chained topology. Counts are computed by the parent, not returned here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerDescendantsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerDescendantsResponse200]:
    """Read-only summaries (guid, parentGuid, name, address, status, versions) of the nodes this panel
    manages. A parent panel calls it on a node (via the node API token) to surface transitive sub-nodes
    in a chained topology. Counts are computed by the parent, not returned here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerDescendantsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerDescendantsResponse200 | None:
    """Read-only summaries (guid, parentGuid, name, address, status, versions) of the nodes this panel
    manages. A parent panel calls it on a node (via the node API token) to surface transitive sub-nodes
    in a chained topology. Counts are computed by the parent, not returned here.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerDescendantsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
