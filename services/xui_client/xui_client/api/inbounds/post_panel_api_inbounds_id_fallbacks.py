from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_inbounds_id_fallbacks_body import PostPanelApiInboundsIdFallbacksBody
from ...models.post_panel_api_inbounds_id_fallbacks_response_200 import PostPanelApiInboundsIdFallbacksResponse200
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: PostPanelApiInboundsIdFallbacksBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/inbounds/{id}/fallbacks".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiInboundsIdFallbacksResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiInboundsIdFallbacksResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiInboundsIdFallbacksResponse200]:
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
    body: PostPanelApiInboundsIdFallbacksBody,
) -> Response[PostPanelApiInboundsIdFallbacksResponse200]:
    """Replace the entire fallback list for a master inbound. Body is JSON. Triggers an Xray restart.

    Args:
        id (int):
        body (PostPanelApiInboundsIdFallbacksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiInboundsIdFallbacksResponse200]
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
    body: PostPanelApiInboundsIdFallbacksBody,
) -> PostPanelApiInboundsIdFallbacksResponse200 | None:
    """Replace the entire fallback list for a master inbound. Body is JSON. Triggers an Xray restart.

    Args:
        id (int):
        body (PostPanelApiInboundsIdFallbacksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiInboundsIdFallbacksResponse200
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
    body: PostPanelApiInboundsIdFallbacksBody,
) -> Response[PostPanelApiInboundsIdFallbacksResponse200]:
    """Replace the entire fallback list for a master inbound. Body is JSON. Triggers an Xray restart.

    Args:
        id (int):
        body (PostPanelApiInboundsIdFallbacksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiInboundsIdFallbacksResponse200]
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
    body: PostPanelApiInboundsIdFallbacksBody,
) -> PostPanelApiInboundsIdFallbacksResponse200 | None:
    """Replace the entire fallback list for a master inbound. Body is JSON. Triggers an Xray restart.

    Args:
        id (int):
        body (PostPanelApiInboundsIdFallbacksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiInboundsIdFallbacksResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
