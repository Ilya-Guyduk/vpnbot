from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_panel_api_nodes_history_id_metric_bucket_response_200 import (
    GetPanelApiNodesHistoryIdMetricBucketResponse200,
)
from ...types import Response


def _get_kwargs(
    id: int,
    metric: str,
    bucket: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/panel/api/nodes/history/{id}/{metric}/{bucket}".format(
            id=quote(str(id), safe=""),
            metric=quote(str(metric), safe=""),
            bucket=quote(str(bucket), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetPanelApiNodesHistoryIdMetricBucketResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPanelApiNodesHistoryIdMetricBucketResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetPanelApiNodesHistoryIdMetricBucketResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiNodesHistoryIdMetricBucketResponse200]:
    """Aggregated metric history for a node — same shape as /server/history, scoped to one node.

    Args:
        id (int):
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiNodesHistoryIdMetricBucketResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        metric=metric,
        bucket=bucket,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiNodesHistoryIdMetricBucketResponse200 | None:
    """Aggregated metric history for a node — same shape as /server/history, scoped to one node.

    Args:
        id (int):
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiNodesHistoryIdMetricBucketResponse200
    """

    return sync_detailed(
        id=id,
        metric=metric,
        bucket=bucket,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetPanelApiNodesHistoryIdMetricBucketResponse200]:
    """Aggregated metric history for a node — same shape as /server/history, scoped to one node.

    Args:
        id (int):
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPanelApiNodesHistoryIdMetricBucketResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        metric=metric,
        bucket=bucket,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    metric: str,
    bucket: int,
    *,
    client: AuthenticatedClient | Client,
) -> GetPanelApiNodesHistoryIdMetricBucketResponse200 | None:
    """Aggregated metric history for a node — same shape as /server/history, scoped to one node.

    Args:
        id (int):
        metric (str):
        bucket (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPanelApiNodesHistoryIdMetricBucketResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            metric=metric,
            bucket=bucket,
            client=client,
        )
    ).parsed
