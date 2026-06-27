from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_xray_warp_action_response_200 import PostPanelApiXrayWarpActionResponse200
from ...types import Response


def _get_kwargs(
    action: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/xray/warp/{action}".format(
            action=quote(str(action), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiXrayWarpActionResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiXrayWarpActionResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiXrayWarpActionResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    action: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiXrayWarpActionResponse200]:
    """Manage Cloudflare Warp integration. The action parameter selects the operation.

    Args:
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiXrayWarpActionResponse200]
    """

    kwargs = _get_kwargs(
        action=action,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    action: str,
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiXrayWarpActionResponse200 | None:
    """Manage Cloudflare Warp integration. The action parameter selects the operation.

    Args:
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiXrayWarpActionResponse200
    """

    return sync_detailed(
        action=action,
        client=client,
    ).parsed


async def asyncio_detailed(
    action: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[PostPanelApiXrayWarpActionResponse200]:
    """Manage Cloudflare Warp integration. The action parameter selects the operation.

    Args:
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiXrayWarpActionResponse200]
    """

    kwargs = _get_kwargs(
        action=action,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    action: str,
    *,
    client: AuthenticatedClient | Client,
) -> PostPanelApiXrayWarpActionResponse200 | None:
    """Manage Cloudflare Warp integration. The action parameter selects the operation.

    Args:
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiXrayWarpActionResponse200
    """

    return (
        await asyncio_detailed(
            action=action,
            client=client,
        )
    ).parsed
