from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_xray_reset_outbounds_traffic_body import PostPanelApiXrayResetOutboundsTrafficBody
from ...models.post_panel_api_xray_reset_outbounds_traffic_response_200 import (
    PostPanelApiXrayResetOutboundsTrafficResponse200,
)
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiXrayResetOutboundsTrafficBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/xray/resetOutboundsTraffic",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiXrayResetOutboundsTrafficResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiXrayResetOutboundsTrafficResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiXrayResetOutboundsTrafficResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiXrayResetOutboundsTrafficBody,
) -> Response[PostPanelApiXrayResetOutboundsTrafficResponse200]:
    """Reset traffic counters for a specific outbound by tag.

    Args:
        body (PostPanelApiXrayResetOutboundsTrafficBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiXrayResetOutboundsTrafficResponse200]
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
    body: PostPanelApiXrayResetOutboundsTrafficBody,
) -> PostPanelApiXrayResetOutboundsTrafficResponse200 | None:
    """Reset traffic counters for a specific outbound by tag.

    Args:
        body (PostPanelApiXrayResetOutboundsTrafficBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiXrayResetOutboundsTrafficResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiXrayResetOutboundsTrafficBody,
) -> Response[PostPanelApiXrayResetOutboundsTrafficResponse200]:
    """Reset traffic counters for a specific outbound by tag.

    Args:
        body (PostPanelApiXrayResetOutboundsTrafficBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiXrayResetOutboundsTrafficResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiXrayResetOutboundsTrafficBody,
) -> PostPanelApiXrayResetOutboundsTrafficResponse200 | None:
    """Reset traffic counters for a specific outbound by tag.

    Args:
        body (PostPanelApiXrayResetOutboundsTrafficBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiXrayResetOutboundsTrafficResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
