from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_login_body import PostLoginBody
from ...models.post_login_response_200 import PostLoginResponse200
from ...models.post_login_response_400 import PostLoginResponse400
from ...types import Response


def _get_kwargs(
    *,
    body: PostLoginBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/login",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostLoginResponse200 | PostLoginResponse400 | None:
    if response.status_code == 200:
        response_200 = PostLoginResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = PostLoginResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostLoginResponse200 | PostLoginResponse400]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostLoginBody,
) -> Response[PostLoginResponse200 | PostLoginResponse400]:
    """Authenticate with username + password and receive a session cookie. Required before any cookie-based
    API call.

    Args:
        body (PostLoginBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostLoginResponse200 | PostLoginResponse400]
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
    body: PostLoginBody,
) -> PostLoginResponse200 | PostLoginResponse400 | None:
    """Authenticate with username + password and receive a session cookie. Required before any cookie-based
    API call.

    Args:
        body (PostLoginBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostLoginResponse200 | PostLoginResponse400
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostLoginBody,
) -> Response[PostLoginResponse200 | PostLoginResponse400]:
    """Authenticate with username + password and receive a session cookie. Required before any cookie-based
    API call.

    Args:
        body (PostLoginBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostLoginResponse200 | PostLoginResponse400]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostLoginBody,
) -> PostLoginResponse200 | PostLoginResponse400 | None:
    """Authenticate with username + password and receive a session cookie. Required before any cookie-based
    API call.

    Args:
        body (PostLoginBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostLoginResponse200 | PostLoginResponse400
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
