from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_clients_list_paged_response_200 import GetPanelApiClientsListPagedResponse200
from ...types import UNSET, Response


def _get_kwargs(
    *,
    page: int,
    page_size: int,
    search: str,
    filter_: str,
    protocol: str,
    sort: str,
    order: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["pageSize"] = page_size

    params["search"] = search

    params["filter"] = filter_

    params["protocol"] = protocol

    params["sort"] = sort

    params["order"] = order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/clients/list/paged",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiClientsListPagedResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiClientsListPagedResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiClientsListPagedResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int,
    page_size: int,
    search: str,
    filter_: str,
    protocol: str,
    sort: str,
    order: str,
) -> Response[GetPanelApiClientsListPagedResponse200]:
    """Filter, sort, and paginate clients on the server. Each item is a slim row (no
    uuid/password/auth/flow/security/reverse/tgId) so the clients page can ship 25-ish rows in a few KB
    instead of the full table. The response also includes a summary computed across the full DB row set
    so dashboard counters stay stable as the user paginates or filters. Page size capped at 200; fetch
    /get/:email to obtain the full per-client payload for an edit/info modal.

    Args:
        page (int):
        page_size (int):
        search (str):
        filter_ (str):
        protocol (str):
        sort (str):
        order (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsListPagedResponse200]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        search=search,
        filter_=filter_,
        protocol=protocol,
        sort=sort,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    page: int,
    page_size: int,
    search: str,
    filter_: str,
    protocol: str,
    sort: str,
    order: str,
) -> GetPanelApiClientsListPagedResponse200 | None:
    """Filter, sort, and paginate clients on the server. Each item is a slim row (no
    uuid/password/auth/flow/security/reverse/tgId) so the clients page can ship 25-ish rows in a few KB
    instead of the full table. The response also includes a summary computed across the full DB row set
    so dashboard counters stay stable as the user paginates or filters. Page size capped at 200; fetch
    /get/:email to obtain the full per-client payload for an edit/info modal.

    Args:
        page (int):
        page_size (int):
        search (str):
        filter_ (str):
        protocol (str):
        sort (str):
        order (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsListPagedResponse200
    """

    return sync_detailed(
        client=client,
        page=page,
        page_size=page_size,
        search=search,
        filter_=filter_,
        protocol=protocol,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int,
    page_size: int,
    search: str,
    filter_: str,
    protocol: str,
    sort: str,
    order: str,
) -> Response[GetPanelApiClientsListPagedResponse200]:
    """Filter, sort, and paginate clients on the server. Each item is a slim row (no
    uuid/password/auth/flow/security/reverse/tgId) so the clients page can ship 25-ish rows in a few KB
    instead of the full table. The response also includes a summary computed across the full DB row set
    so dashboard counters stay stable as the user paginates or filters. Page size capped at 200; fetch
    /get/:email to obtain the full per-client payload for an edit/info modal.

    Args:
        page (int):
        page_size (int):
        search (str):
        filter_ (str):
        protocol (str):
        sort (str):
        order (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiClientsListPagedResponse200]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        search=search,
        filter_=filter_,
        protocol=protocol,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    page: int,
    page_size: int,
    search: str,
    filter_: str,
    protocol: str,
    sort: str,
    order: str,
) -> GetPanelApiClientsListPagedResponse200 | None:
    """Filter, sort, and paginate clients on the server. Each item is a slim row (no
    uuid/password/auth/flow/security/reverse/tgId) so the clients page can ship 25-ish rows in a few KB
    instead of the full table. The response also includes a summary computed across the full DB row set
    so dashboard counters stay stable as the user paginates or filters. Page size capped at 200; fetch
    /get/:email to obtain the full per-client payload for an edit/info modal.

    Args:
        page (int):
        page_size (int):
        search (str):
        filter_ (str):
        protocol (str):
        sort (str):
        order (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiClientsListPagedResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            page_size=page_size,
            search=search,
            filter_=filter_,
            protocol=protocol,
            sort=sort,
            order=order,
        )
    ).parsed
