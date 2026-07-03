from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_import_body import PostPanelApiClientsImportBody
from ...models.post_panel_api_clients_import_response_200 import PostPanelApiClientsImportResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiClientsImportBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/import",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsImportResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsImportResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsImportResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsImportBody,
) -> Response[PostPanelApiClientsImportResponse200]:
    r"""Import clients from a JSON body { \"data\": \"<json>\" }, where data is a string-encoded array
    produced by /export ([{client, inboundIds}]). Items with inboundIds are created and attached to
    those inbounds; items with an empty inboundIds list are restored as unattached client records.
    Existing emails are never overwritten — they are returned in skipped. Triggers a single Xray restart
    at the end if any target inbound was running.

    Args:
        body (PostPanelApiClientsImportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsImportResponse200]
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
    body: PostPanelApiClientsImportBody,
) -> PostPanelApiClientsImportResponse200 | None:
    r"""Import clients from a JSON body { \"data\": \"<json>\" }, where data is a string-encoded array
    produced by /export ([{client, inboundIds}]). Items with inboundIds are created and attached to
    those inbounds; items with an empty inboundIds list are restored as unattached client records.
    Existing emails are never overwritten — they are returned in skipped. Triggers a single Xray restart
    at the end if any target inbound was running.

    Args:
        body (PostPanelApiClientsImportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsImportResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsImportBody,
) -> Response[PostPanelApiClientsImportResponse200]:
    r"""Import clients from a JSON body { \"data\": \"<json>\" }, where data is a string-encoded array
    produced by /export ([{client, inboundIds}]). Items with inboundIds are created and attached to
    those inbounds; items with an empty inboundIds list are restored as unattached client records.
    Existing emails are never overwritten — they are returned in skipped. Triggers a single Xray restart
    at the end if any target inbound was running.

    Args:
        body (PostPanelApiClientsImportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsImportResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsImportBody,
) -> PostPanelApiClientsImportResponse200 | None:
    r"""Import clients from a JSON body { \"data\": \"<json>\" }, where data is a string-encoded array
    produced by /export ([{client, inboundIds}]). Items with inboundIds are created and attached to
    those inbounds; items with an empty inboundIds list are restored as unattached client records.
    Existing emails are never overwritten — they are returned in skipped. Triggers a single Xray restart
    at the end if any target inbound was running.

    Args:
        body (PostPanelApiClientsImportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsImportResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
