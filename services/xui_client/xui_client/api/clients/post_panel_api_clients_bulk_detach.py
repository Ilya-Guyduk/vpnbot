from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_bulk_detach_body import PostPanelApiClientsBulkDetachBody
from ...models.post_panel_api_clients_bulk_detach_response_200 import PostPanelApiClientsBulkDetachResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsBulkDetachBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/bulkDetach",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsBulkDetachResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsBulkDetachResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsBulkDetachResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkDetachBody,
) -> Response[PostPanelApiClientsBulkDetachResponse200]:
    """Mirror of bulkAttach: detach many existing clients from many inbounds in one call. For each email,
    intersects the client's current inbounds with the requested set and detaches from those only;
    (email, inbound) pairs where the client is not currently attached are silently no-ops. Emails not
    attached to any of the requested inbounds are reported under skipped. Client records are kept even
    if they become orphaned — use bulkDel for full removal. Returns per-email detached/skipped/errors
    lists and triggers a single Xray restart if any target inbound was running.

    Args:
        body (PostPanelApiClientsBulkDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkDetachResponse200]
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
    body: PostPanelApiClientsBulkDetachBody,
) -> PostPanelApiClientsBulkDetachResponse200 | None:
    """Mirror of bulkAttach: detach many existing clients from many inbounds in one call. For each email,
    intersects the client's current inbounds with the requested set and detaches from those only;
    (email, inbound) pairs where the client is not currently attached are silently no-ops. Emails not
    attached to any of the requested inbounds are reported under skipped. Client records are kept even
    if they become orphaned — use bulkDel for full removal. Returns per-email detached/skipped/errors
    lists and triggers a single Xray restart if any target inbound was running.

    Args:
        body (PostPanelApiClientsBulkDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkDetachResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkDetachBody,
) -> Response[PostPanelApiClientsBulkDetachResponse200]:
    """Mirror of bulkAttach: detach many existing clients from many inbounds in one call. For each email,
    intersects the client's current inbounds with the requested set and detaches from those only;
    (email, inbound) pairs where the client is not currently attached are silently no-ops. Emails not
    attached to any of the requested inbounds are reported under skipped. Client records are kept even
    if they become orphaned — use bulkDel for full removal. Returns per-email detached/skipped/errors
    lists and triggers a single Xray restart if any target inbound was running.

    Args:
        body (PostPanelApiClientsBulkDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkDetachResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkDetachBody,
) -> PostPanelApiClientsBulkDetachResponse200 | None:
    """Mirror of bulkAttach: detach many existing clients from many inbounds in one call. For each email,
    intersects the client's current inbounds with the requested set and detaches from those only;
    (email, inbound) pairs where the client is not currently attached are silently no-ops. Emails not
    attached to any of the requested inbounds are reported under skipped. Client records are kept even
    if they become orphaned — use bulkDel for full removal. Returns per-email detached/skipped/errors
    lists and triggers a single Xray restart if any target inbound was running.

    Args:
        body (PostPanelApiClientsBulkDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkDetachResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
