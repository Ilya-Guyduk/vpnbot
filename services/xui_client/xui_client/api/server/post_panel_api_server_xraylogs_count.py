from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_server_xraylogs_count_body import PostPanelApiServerXraylogsCountBody
from ...models.post_panel_api_server_xraylogs_count_response_200 import PostPanelApiServerXraylogsCountResponse200
from ...types import Response


def _get_kwargs(
    count: int,
    *,
    body: PostPanelApiServerXraylogsCountBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/server/xraylogs/{count}".format(
            count=quote(str(count), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiServerXraylogsCountResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiServerXraylogsCountResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiServerXraylogsCountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    count: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerXraylogsCountBody,
) -> Response[PostPanelApiServerXraylogsCountResponse200]:
    """Return the last N lines of the Xray process log.

    Args:
        count (int):
        body (PostPanelApiServerXraylogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerXraylogsCountResponse200]
    """

    kwargs = _get_kwargs(
        count=count,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    count: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerXraylogsCountBody,
) -> PostPanelApiServerXraylogsCountResponse200 | None:
    """Return the last N lines of the Xray process log.

    Args:
        count (int):
        body (PostPanelApiServerXraylogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerXraylogsCountResponse200
    """

    return sync_detailed(
        count=count,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    count: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerXraylogsCountBody,
) -> Response[PostPanelApiServerXraylogsCountResponse200]:
    """Return the last N lines of the Xray process log.

    Args:
        count (int):
        body (PostPanelApiServerXraylogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerXraylogsCountResponse200]
    """

    kwargs = _get_kwargs(
        count=count,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    count: int,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerXraylogsCountBody,
) -> PostPanelApiServerXraylogsCountResponse200 | None:
    """Return the last N lines of the Xray process log.

    Args:
        count (int):
        body (PostPanelApiServerXraylogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerXraylogsCountResponse200
    """

    return (
        await asyncio_detailed(
            count=count,
            client=client,
            body=body,
        )
    ).parsed
