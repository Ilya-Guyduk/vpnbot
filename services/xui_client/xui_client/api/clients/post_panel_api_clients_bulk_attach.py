from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_bulk_attach_body import PostPanelApiClientsBulkAttachBody
from ...models.post_panel_api_clients_bulk_attach_response_200 import PostPanelApiClientsBulkAttachResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsBulkAttachBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/bulkAttach",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsBulkAttachResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsBulkAttachResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsBulkAttachResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAttachBody,
) -> Response[PostPanelApiClientsBulkAttachResponse200]:
    """Attach many existing clients to many inbounds in one call. Each client keeps its identity
    (email/UUID/password/subId) and a shared traffic row; all clients are added to a target inbound in a
    single AddInboundClient call. Clients already present on a target are reported under skipped.
    Returns per-email attached/skipped/errors lists and triggers a single Xray restart if any target
    inbound was running.

    Args:
        body (PostPanelApiClientsBulkAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkAttachResponse200]
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
    body: PostPanelApiClientsBulkAttachBody,
) -> PostPanelApiClientsBulkAttachResponse200 | None:
    """Attach many existing clients to many inbounds in one call. Each client keeps its identity
    (email/UUID/password/subId) and a shared traffic row; all clients are added to a target inbound in a
    single AddInboundClient call. Clients already present on a target are reported under skipped.
    Returns per-email attached/skipped/errors lists and triggers a single Xray restart if any target
    inbound was running.

    Args:
        body (PostPanelApiClientsBulkAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkAttachResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAttachBody,
) -> Response[PostPanelApiClientsBulkAttachResponse200]:
    """Attach many existing clients to many inbounds in one call. Each client keeps its identity
    (email/UUID/password/subId) and a shared traffic row; all clients are added to a target inbound in a
    single AddInboundClient call. Clients already present on a target are reported under skipped.
    Returns per-email attached/skipped/errors lists and triggers a single Xray restart if any target
    inbound was running.

    Args:
        body (PostPanelApiClientsBulkAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsBulkAttachResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsBulkAttachBody,
) -> PostPanelApiClientsBulkAttachResponse200 | None:
    """Attach many existing clients to many inbounds in one call. Each client keeps its identity
    (email/UUID/password/subId) and a shared traffic row; all clients are added to a target inbound in a
    single AddInboundClient call. Clients already present on a target are reported under skipped.
    Returns per-email attached/skipped/errors lists and triggers a single Xray restart if any target
    inbound was running.

    Args:
        body (PostPanelApiClientsBulkAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsBulkAttachResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
