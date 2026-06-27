from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_panel_api_nodes_mtls_trust_ca_body import PostPanelApiNodesMtlsTrustCABody
from ...models.post_panel_api_nodes_mtls_trust_ca_response_200 import PostPanelApiNodesMtlsTrustCAResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: PostPanelApiNodesMtlsTrustCABody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/panel/api/nodes/mtls/trustCA",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> PostPanelApiNodesMtlsTrustCAResponse200 | None:
    if response.status_code == 200:
        response_200 = PostPanelApiNodesMtlsTrustCAResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[PostPanelApiNodesMtlsTrustCAResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesMtlsTrustCABody,
) -> Response[PostPanelApiNodesMtlsTrustCAResponse200]:
    """Set the CA certificate this panel trusts for incoming node-API client certificates (this panel
    acting as a node). Paste the managing panel's CA (from nodes/mtls/ca). An empty caCert disables it.
    A non-empty value must be a PEM certificate. Applied on the next panel restart.

    Args:
        body (PostPanelApiNodesMtlsTrustCABody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesMtlsTrustCAResponse200]
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
    body: PostPanelApiNodesMtlsTrustCABody,
) -> PostPanelApiNodesMtlsTrustCAResponse200 | None:
    """Set the CA certificate this panel trusts for incoming node-API client certificates (this panel
    acting as a node). Paste the managing panel's CA (from nodes/mtls/ca). An empty caCert disables it.
    A non-empty value must be a PEM certificate. Applied on the next panel restart.

    Args:
        body (PostPanelApiNodesMtlsTrustCABody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesMtlsTrustCAResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesMtlsTrustCABody,
) -> Response[PostPanelApiNodesMtlsTrustCAResponse200]:
    """Set the CA certificate this panel trusts for incoming node-API client certificates (this panel
    acting as a node). Paste the managing panel's CA (from nodes/mtls/ca). An empty caCert disables it.
    A non-empty value must be a PEM certificate. Applied on the next panel restart.

    Args:
        body (PostPanelApiNodesMtlsTrustCABody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPanelApiNodesMtlsTrustCAResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPanelApiNodesMtlsTrustCABody,
) -> PostPanelApiNodesMtlsTrustCAResponse200 | None:
    """Set the CA certificate this panel trusts for incoming node-API client certificates (this panel
    acting as a node). Paste the managing panel's CA (from nodes/mtls/ca). An empty caCert disables it.
    A non-empty value must be a PEM certificate. Applied on the next panel restart.

    Args:
        body (PostPanelApiNodesMtlsTrustCABody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPanelApiNodesMtlsTrustCAResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
