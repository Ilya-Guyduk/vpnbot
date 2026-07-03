from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_hosts_add_body import PostPanelApiHostsAddBody
from ...models.post_panel_api_hosts_add_response_200 import PostPanelApiHostsAddResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiHostsAddBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/hosts/add",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiHostsAddResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiHostsAddResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiHostsAddResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiHostsAddBody,
) -> Response[PostPanelApiHostsAddResponse200]:
    r"""Create a host on an inbound. inboundId and remark are required; security defaults to \"same\"
    (inherit the inbound).

    Args:
        body (PostPanelApiHostsAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiHostsAddResponse200]
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
    body: PostPanelApiHostsAddBody,
) -> PostPanelApiHostsAddResponse200 | None:
    r"""Create a host on an inbound. inboundId and remark are required; security defaults to \"same\"
    (inherit the inbound).

    Args:
        body (PostPanelApiHostsAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiHostsAddResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiHostsAddBody,
) -> Response[PostPanelApiHostsAddResponse200]:
    r"""Create a host on an inbound. inboundId and remark are required; security defaults to \"same\"
    (inherit the inbound).

    Args:
        body (PostPanelApiHostsAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiHostsAddResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiHostsAddBody,
) -> PostPanelApiHostsAddResponse200 | None:
    r"""Create a host on an inbound. inboundId and remark are required; security defaults to \"same\"
    (inherit the inbound).

    Args:
        body (PostPanelApiHostsAddBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiHostsAddResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
