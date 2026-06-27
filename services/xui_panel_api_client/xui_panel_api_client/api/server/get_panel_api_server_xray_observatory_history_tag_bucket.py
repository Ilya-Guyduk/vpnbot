from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_server_xray_observatory_history_tag_bucket_response_200 import (
    GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200,
)
from ...types import Response


def _get_kwargs(
    tag: str,
    bucket: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/server/xrayObservatoryHistory/{tag}/{bucket}".format(
            tag=quote(str(tag), safe=""),
            bucket=quote(str(bucket), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200]:
    """Time-series of observatory probe results for one outbound tag. Same {t, v} shape as the other
    history endpoints.

    Args:
        tag (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200]
    """

    kwargs = _get_kwargs(
        tag=tag,
        bucket=bucket,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200 | None:
    """Time-series of observatory probe results for one outbound tag. Same {t, v} shape as the other
    history endpoints.

    Args:
        tag (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200
    """

    return sync_detailed(
        tag=tag,
        bucket=bucket,
        client=client,
    ).parsed


async def asyncio_detailed(
    tag: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200]:
    """Time-series of observatory probe results for one outbound tag. Same {t, v} shape as the other
    history endpoints.

    Args:
        tag (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200]
    """

    kwargs = _get_kwargs(
        tag=tag,
        bucket=bucket,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200 | None:
    """Time-series of observatory probe results for one outbound tag. Same {t, v} shape as the other
    history endpoints.

    Args:
        tag (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerXrayObservatoryHistoryTagBucketResponse200
    """

    return (
        await asyncio_detailed(
            tag=tag,
            bucket=bucket,
            client=client,
        )
    ).parsed
