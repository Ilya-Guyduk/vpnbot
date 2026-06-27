from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_server_update_geofile_body import PostPanelApiServerUpdateGeofileBody
from ...models.post_panel_api_server_update_geofile_response_200 import PostPanelApiServerUpdateGeofileResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiServerUpdateGeofileBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/server/updateGeofile",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiServerUpdateGeofileResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiServerUpdateGeofileResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiServerUpdateGeofileResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerUpdateGeofileBody,
) -> Response[PostPanelApiServerUpdateGeofileResponse200]:
    """Refresh the default GeoIP / GeoSite data files. Body can include a fileName, or use the /:fileName
    variant.

    Args:
        body (PostPanelApiServerUpdateGeofileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerUpdateGeofileResponse200]
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
    body: PostPanelApiServerUpdateGeofileBody,
) -> PostPanelApiServerUpdateGeofileResponse200 | None:
    """Refresh the default GeoIP / GeoSite data files. Body can include a fileName, or use the /:fileName
    variant.

    Args:
        body (PostPanelApiServerUpdateGeofileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerUpdateGeofileResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerUpdateGeofileBody,
) -> Response[PostPanelApiServerUpdateGeofileResponse200]:
    """Refresh the default GeoIP / GeoSite data files. Body can include a fileName, or use the /:fileName
    variant.

    Args:
        body (PostPanelApiServerUpdateGeofileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiServerUpdateGeofileResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiServerUpdateGeofileBody,
) -> PostPanelApiServerUpdateGeofileResponse200 | None:
    """Refresh the default GeoIP / GeoSite data files. Body can include a fileName, or use the /:fileName
    variant.

    Args:
        body (PostPanelApiServerUpdateGeofileBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiServerUpdateGeofileResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
