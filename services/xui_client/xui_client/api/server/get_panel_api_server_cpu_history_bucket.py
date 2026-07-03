from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_server_cpu_history_bucket_response_200 import GetPanelApiServerCpuHistoryBucketResponse200
from ...types import Response


def _get_kwargs(
    bucket: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/server/cpuHistory/{bucket}".format(
            bucket=quote(str(bucket), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiServerCpuHistoryBucketResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiServerCpuHistoryBucketResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiServerCpuHistoryBucketResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerCpuHistoryBucketResponse200]:
    """Legacy: aggregated CPU history. Use /history/cpu/:bucket instead — same data with a uniform {t, v}
    shape.

    Args:
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerCpuHistoryBucketResponse200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerCpuHistoryBucketResponse200 | None:
    """Legacy: aggregated CPU history. Use /history/cpu/:bucket instead — same data with a uniform {t, v}
    shape.

    Args:
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerCpuHistoryBucketResponse200
    """

    return sync_detailed(
        bucket=bucket,
        client=client,
    ).parsed


async def asyncio_detailed(
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerCpuHistoryBucketResponse200]:
    """Legacy: aggregated CPU history. Use /history/cpu/:bucket instead — same data with a uniform {t, v}
    shape.

    Args:
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerCpuHistoryBucketResponse200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerCpuHistoryBucketResponse200 | None:
    """Legacy: aggregated CPU history. Use /history/cpu/:bucket instead — same data with a uniform {t, v}
    shape.

    Args:
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerCpuHistoryBucketResponse200
    """

    return (
        await asyncio_detailed(
            bucket=bucket,
            client=client,
        )
    ).parsed
