from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_server_logs_count_body import PostPanelApiServerLogsCountBody
from ...models.post_panel_api_server_logs_count_response_200 import PostPanelApiServerLogsCountResponse200
from ...types import Response


def _get_kwargs(
    count: int,
    *,
    body: PostPanelApiServerLogsCountBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/server/logs/{count}".format(
            count=quote(str(count), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiServerLogsCountResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiServerLogsCountResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiServerLogsCountResponse200]:
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
    body: PostPanelApiServerLogsCountBody,
) -> Response[PostPanelApiServerLogsCountResponse200]:
    """Return the last N lines of the panel’s own log.

    Args:
        count (int):
        body (PostPanelApiServerLogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerLogsCountResponse200]
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
    body: PostPanelApiServerLogsCountBody,
) -> PostPanelApiServerLogsCountResponse200 | None:
    """Return the last N lines of the panel’s own log.

    Args:
        count (int):
        body (PostPanelApiServerLogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerLogsCountResponse200
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
    body: PostPanelApiServerLogsCountBody,
) -> Response[PostPanelApiServerLogsCountResponse200]:
    """Return the last N lines of the panel’s own log.

    Args:
        count (int):
        body (PostPanelApiServerLogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerLogsCountResponse200]
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
    body: PostPanelApiServerLogsCountBody,
) -> PostPanelApiServerLogsCountResponse200 | None:
    """Return the last N lines of the panel’s own log.

    Args:
        count (int):
        body (PostPanelApiServerLogsCountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerLogsCountResponse200
    """

    return (
        await asyncio_detailed(
            count=count,
            client=client,
            body=body,
        )
    ).parsed
