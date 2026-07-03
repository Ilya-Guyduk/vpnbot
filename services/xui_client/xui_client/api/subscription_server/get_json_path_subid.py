from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_json_path_subid_response_200 import GetJsonPathSubidResponse200
from ...types import Response


def _get_kwargs(
    json_path: str,
    subid: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/{json_path}{subid}".format(
            json_path=quote(str(json_path), safe=""),
            subid=quote(str(subid), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetJsonPathSubidResponse200 | None:
    if response.status_code == 200:
        response_200 = GetJsonPathSubidResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetJsonPathSubidResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    json_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetJsonPathSubidResponse200]:
    """Return subscription as a JSON array of proxy configs (one per enabled client). Only when JSON
    subscription is enabled in settings. Default path: /json/:subid.

    Args:
        json_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetJsonPathSubidResponse200]
    """

    kwargs = _get_kwargs(
        json_path=json_path,
        subid=subid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    json_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetJsonPathSubidResponse200 | None:
    """Return subscription as a JSON array of proxy configs (one per enabled client). Only when JSON
    subscription is enabled in settings. Default path: /json/:subid.

    Args:
        json_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetJsonPathSubidResponse200
    """

    return sync_detailed(
        json_path=json_path,
        subid=subid,
        client=client,
    ).parsed


async def asyncio_detailed(
    json_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[GetJsonPathSubidResponse200]:
    """Return subscription as a JSON array of proxy configs (one per enabled client). Only when JSON
    subscription is enabled in settings. Default path: /json/:subid.

    Args:
        json_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetJsonPathSubidResponse200]
    """

    kwargs = _get_kwargs(
        json_path=json_path,
        subid=subid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    json_path: str,
    subid: str,
    *,
    client: AuthenticatedClient | Client,
) -> GetJsonPathSubidResponse200 | None:
    """Return subscription as a JSON array of proxy configs (one per enabled client). Only when JSON
    subscription is enabled in settings. Default path: /json/:subid.

    Args:
        json_path (str):
        subid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetJsonPathSubidResponse200
    """

    return (
        await asyncio_detailed(
            json_path=json_path,
            subid=subid,
            client=client,
        )
    ).parsed
