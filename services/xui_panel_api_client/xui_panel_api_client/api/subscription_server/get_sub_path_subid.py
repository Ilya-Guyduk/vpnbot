from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_sub_path_subid_response_200 import GetSubPathSubidResponse200
from ...types import Response


def _get_kwargs(
    sub_path: str,
    subid: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/{sub_path}{subid}".format(
            sub_path=quote(str(sub_path), safe=""),
            subid=quote(str(subid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetSubPathSubidResponse200 | None:
    if response.status_code == 200:
        response_200 = GetSubPathSubidResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetSubPathSubidResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sub_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetSubPathSubidResponse200]:
    """Return base64-encoded subscription links for all enabled clients matching the subscription ID. When
    the request has an Accept: text/html header or ?html=1, renders a styled info page instead. Default
    path: /sub/:subid.

    Args:
        sub_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSubPathSubidResponse200]
    """

    kwargs = _get_kwargs(
        sub_path=sub_path,
        subid=subid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sub_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetSubPathSubidResponse200 | None:
    """Return base64-encoded subscription links for all enabled clients matching the subscription ID. When
    the request has an Accept: text/html header or ?html=1, renders a styled info page instead. Default
    path: /sub/:subid.

    Args:
        sub_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSubPathSubidResponse200
    """

    return sync_detailed(
        sub_path=sub_path,
        subid=subid,
        client=client,
    ).parsed


async def asyncio_detailed(
    sub_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetSubPathSubidResponse200]:
    """Return base64-encoded subscription links for all enabled clients matching the subscription ID. When
    the request has an Accept: text/html header or ?html=1, renders a styled info page instead. Default
    path: /sub/:subid.

    Args:
        sub_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetSubPathSubidResponse200]
    """

    kwargs = _get_kwargs(
        sub_path=sub_path,
        subid=subid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sub_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetSubPathSubidResponse200 | None:
    """Return base64-encoded subscription links for all enabled clients matching the subscription ID. When
    the request has an Accept: text/html header or ?html=1, renders a styled info page instead. Default
    path: /sub/:subid.

    Args:
        sub_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetSubPathSubidResponse200
    """

    return (
        await asyncio_detailed(
            sub_path=sub_path,
            subid=subid,
            client=client,
        )
    ).parsed
