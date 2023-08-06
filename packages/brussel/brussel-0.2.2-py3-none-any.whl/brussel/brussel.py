"""Asynchronous Python client providing Open Data information of Brussel."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, cast

import async_timeout
from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import ODPBrusselConnectionError, ODPBrusselError
from .models import DisabledParking, Garage


@dataclass
class ODPBrussel:
    """Main class for handling data fetchting from Open Data Platform of Brussel."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Open Data Platform API of Brussel.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (text) with the response from
            the Open Data Platform API of Brussel.

        Raises:
        ------
            ODPBrusselConnectionError: Timeout occurred while
                connecting to the Open Data Platform API.
            ODPBrusselError: If the data is not valid.
        """
        version = metadata.version(__package__)
        url = URL.build(
            scheme="https",
            host="bruxellesdata.opendatasoft.com",
            path="/api/records/1.0/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonODPBrussel/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Open Data Platform API."
            raise ODPBrusselConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with Open Data Platform API."
            raise ODPBrusselConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Open Data Platform API"
            raise ODPBrusselError(
                msg,
                {"Content-Type": content_type, "Response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def disabled_parkings(self, limit: int = 10) -> list[DisabledParking]:
        """Get list of disabled parking.

        Args:
        ----
            limit: Maximum number of disabled parkings to return.

        Returns:
        -------
            A list of DisabledParking objects.
        """
        locations = await self._request(
            "search/",
            params={"dataset": "parking-spaces-for-disabled", "rows": limit},
        )
        return [DisabledParking.from_dict(item) for item in locations["records"]]

    async def garages(self, limit: int = 10) -> list[Garage]:
        """Get list of parking garages.

        Args:
        ----
            limit: Maximum number of garages to return.

        Returns:
        -------
            A list of Garage objects.
        """
        locations = await self._request(
            "search/",
            params={"dataset": "parkings", "rows": limit},
        )
        return [Garage.from_dict(item) for item in locations["records"]]

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> ODPBrussel:
        """Async enter.

        Returns
        -------
            The Open Data Platform Brussel object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
