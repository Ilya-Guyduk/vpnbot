from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_email_detach_body import PostPanelApiClientsEmailDetachBody
from ...models.post_panel_api_clients_email_detach_response_200 import PostPanelApiClientsEmailDetachResponse200
from ...types import Response


def _get_kwargs(
    email: str,
    *,
    body: PostPanelApiClientsEmailDetachBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/{email}/detach".format(
            email=quote(str(email), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsEmailDetachResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsEmailDetachResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsEmailDetachResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsEmailDetachBody,
) -> Response[PostPanelApiClientsEmailDetachResponse200]:
    """Detach a client from one or more inbounds without deleting the client.

    Args:
        email (str):
        body (PostPanelApiClientsEmailDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsEmailDetachResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsEmailDetachBody,
) -> PostPanelApiClientsEmailDetachResponse200 | None:
    """Detach a client from one or more inbounds without deleting the client.

    Args:
        email (str):
        body (PostPanelApiClientsEmailDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsEmailDetachResponse200
    """

    return sync_detailed(
        email=email,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsEmailDetachBody,
) -> Response[PostPanelApiClientsEmailDetachResponse200]:
    """Detach a client from one or more inbounds without deleting the client.

    Args:
        email (str):
        body (PostPanelApiClientsEmailDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsEmailDetachResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email: str,
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiClientsEmailDetachBody,
) -> PostPanelApiClientsEmailDetachResponse200 | None:
    """Detach a client from one or more inbounds without deleting the client.

    Args:
        email (str):
        body (PostPanelApiClientsEmailDetachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsEmailDetachResponse200
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
            body=body,
        )
    ).parsed
