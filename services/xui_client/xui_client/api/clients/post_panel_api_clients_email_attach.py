from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_clients_email_attach_body import PostPanelApiClientsEmailAttachBody
from ...models.post_panel_api_clients_email_attach_response_200 import PostPanelApiClientsEmailAttachResponse200
from ...types import Response


def _get_kwargs(
    email: str,
    *,
    body: PostPanelApiClientsEmailAttachBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/clients/{email}/attach".format(
            email=quote(str(email), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiClientsEmailAttachResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiClientsEmailAttachResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiClientsEmailAttachResponse200]:
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
    body: PostPanelApiClientsEmailAttachBody,
) -> Response[PostPanelApiClientsEmailAttachResponse200]:
    """Attach an existing client to one or more additional inbounds. Body is JSON.

    Args:
        email (str):
        body (PostPanelApiClientsEmailAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsEmailAttachResponse200]
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
    body: PostPanelApiClientsEmailAttachBody,
) -> PostPanelApiClientsEmailAttachResponse200 | None:
    """Attach an existing client to one or more additional inbounds. Body is JSON.

    Args:
        email (str):
        body (PostPanelApiClientsEmailAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsEmailAttachResponse200
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
    body: PostPanelApiClientsEmailAttachBody,
) -> Response[PostPanelApiClientsEmailAttachResponse200]:
    """Attach an existing client to one or more additional inbounds. Body is JSON.

    Args:
        email (str):
        body (PostPanelApiClientsEmailAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiClientsEmailAttachResponse200]
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
    body: PostPanelApiClientsEmailAttachBody,
) -> PostPanelApiClientsEmailAttachResponse200 | None:
    """Attach an existing client to one or more additional inbounds. Body is JSON.

    Args:
        email (str):
        body (PostPanelApiClientsEmailAttachBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiClientsEmailAttachResponse200
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
            body=body,
        )
    ).parsed
