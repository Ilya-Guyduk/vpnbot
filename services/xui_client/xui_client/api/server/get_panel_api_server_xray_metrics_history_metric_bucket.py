from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_server_xray_metrics_history_metric_bucket_response_200 import (
    GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200,
)
from ...types import Response


def _get_kwargs(
    metric: str,
    bucket: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/server/xrayMetricsHistory/{metric}/{bucket}".format(
            metric=quote(str(metric), safe=""),
            bucket=quote(str(bucket), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200]:
    """Time-series history for one Xray runtime metric over the last ~6 hours. Same {t, v} shape as
    /history/:metric/:bucket.

    Args:
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200]
    """

    kwargs = _get_kwargs(
        metric=metric,
        bucket=bucket,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200 | None:
    """Time-series history for one Xray runtime metric over the last ~6 hours. Same {t, v} shape as
    /history/:metric/:bucket.

    Args:
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200
    """

    return sync_detailed(
        metric=metric,
        bucket=bucket,
        client=client,
    ).parsed


async def asyncio_detailed(
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200]:
    """Time-series history for one Xray runtime metric over the last ~6 hours. Same {t, v} shape as
    /history/:metric/:bucket.

    Args:
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200]
    """

    kwargs = _get_kwargs(
        metric=metric,
        bucket=bucket,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200 | None:
    """Time-series history for one Xray runtime metric over the last ~6 hours. Same {t, v} shape as
    /history/:metric/:bucket.

    Args:
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiServerXrayMetricsHistoryMetricBucketResponse200
    """

    return (
        await asyncio_detailed(
            metric=metric,
            bucket=bucket,
            client=client,
        )
    ).parsed
