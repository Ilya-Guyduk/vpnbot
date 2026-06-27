from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_setting_api_tokens_create_body import PostPanelApiSettingApiTokensCreateBody
from ...models.post_panel_api_setting_api_tokens_create_response_200 import (
    PostPanelApiSettingApiTokensCreateResponse200,
)
from ...models.post_panel_api_setting_api_tokens_create_response_400 import (
    PostPanelApiSettingApiTokensCreateResponse400,
)
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiSettingApiTokensCreateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/setting/apiTokens/create",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiSettingApiTokensCreateResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = PostPanelApiSettingApiTokensCreateResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiSettingApiTokensCreateBody,
) -> Response[PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400]:
    """Mint a new API token. Name must be unique and 1-64 characters; the token string is server-generated
    and returned only in this response — it is stored hashed and cannot be retrieved later.

    Args:
        body (PostPanelApiSettingApiTokensCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400]
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
    body: PostPanelApiSettingApiTokensCreateBody,
) -> PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400 | None:
    """Mint a new API token. Name must be unique and 1-64 characters; the token string is server-generated
    and returned only in this response — it is stored hashed and cannot be retrieved later.

    Args:
        body (PostPanelApiSettingApiTokensCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiSettingApiTokensCreateBody,
) -> Response[PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400]:
    """Mint a new API token. Name must be unique and 1-64 characters; the token string is server-generated
    and returned only in this response — it is stored hashed and cannot be retrieved later.

    Args:
        body (PostPanelApiSettingApiTokensCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiSettingApiTokensCreateBody,
) -> PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400 | None:
    """Mint a new API token. Name must be unique and 1-64 characters; the token string is server-generated
    and returned only in this response — it is stored hashed and cannot be retrieved later.

    Args:
        body (PostPanelApiSettingApiTokensCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiSettingApiTokensCreateResponse200 | PostPanelApiSettingApiTokensCreateResponse400
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
