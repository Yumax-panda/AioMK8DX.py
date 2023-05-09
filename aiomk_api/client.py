"""
The MIT License (MIT)

Copyright (c) 2023-present Yumax-panda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import asyncio
from aiohttp import ClientSession
from typing import (
    Any,
    Final,
    Optional,
    Type,
    TypeVar,
    Union
)

from .cache import Cache, caching_property

from .change import Bonus, Penalty
from .leaderboard import LeaderBoard
from .player import Player, PlayerDetails
from .table import Table


API_URL: Final[str] = "https://www.mk8dx-lounge.com/api/"
JsonResponse = dict[str, Any]
Param = Union[str, int]
T = TypeVar("T")


class HttpClient:

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        self._session = session or ClientSession()

    async def close(self) -> None:
        await self._session.close()

    async def get(self, endpoint: str, params: dict = {}) -> Optional[JsonResponse]:
        async with self._session.get(API_URL + endpoint, params=params) as response:
            if response.status != 200:
                return None
            else:
                return await response.json()


class AioMKClient:

    _http: HttpClient
    _cache: Cache

    def __init__(self, *, http: Optional[HttpClient] = None) -> None:
        self._http = http or HttpClient()
        self._cache = Cache()

    async def __aenter__(self) -> AioMKClient:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        await self._http.close()

    async def _fetch(self, endpoint: str, cls: Type[T], params: dict = {}) -> Union[T, list[T], None]:
        """fetches data from the api and changes it into a class

        Parameters
        ----------
        endpoint : str
            The endpoint to fetch from
        cls : Type[T]
            The class to change the data into
        params : dict, optional
            query, by default {}

        Returns
        -------
        Union[T, list[T], None]
            The data as a class
        """

        if (data:=await self._http.get(endpoint, params=params)) is None:
            return None
        else:
            if isinstance(data, list):
                return [cls(d) for d in data]
            else:
                return cls(data)

    async def _fetch_many(
        self,
        endpoint: str,
        cls: Type[T],
        params: list[dict] = [],
        return_exceptions: bool = False
    ) -> list[Optional[T]]:
        """fetches data from the api and changes it into a class

        Parameters
        ----------
        endpoint : str
            The endpoint to fetch from
        cls : Type[T]
            The class to change the data into
        params : list[dict], optional
            query, by default {}
        return_exceptions : bool, optional
            whether to return exceptions, by default False

        Returns
        -------
        list[Optional[T]]
            The data as a class
        """

        tasks = [self._http.get(endpoint, params=param) for param in params]
        results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)

        return [cls(data) if data is not None else None for data in results]

    @caching_property
    async def get_player(
        self,
        id: Optional[Param] = None,
        name: Optional[str] = None,
        mkc_id: Optional[Param] = None,
        discord_id: Optional[Param] = None,
        fc: Optional[str] = None,
        season: Optional[Param] = None,
    ) -> Optional[Player]:

        params = {}
        if id is not None:
            params['id'] = id
        elif name is not None:
            params['name'] = name
        elif mkc_id is not None:
            params['mkcId'] = mkc_id
        elif discord_id is not None:
            params['discordId'] = discord_id
        elif fc is not None:
            params['fc'] = fc
        else:
            return None
        if season is not None:
            params['season'] = season

        return await self._fetch("player", Player, params)

    @caching_property
    async def get_player_details(
        self,
        id: Optional[Param] = None,
        name: Optional[str] = None,
        season: Optional[Param] = None,
    ) -> Optional[PlayerDetails]:
        params = {}
        if id is not None:
            params['id'] = id
        elif name is not None:
            params['name'] = name
        else:
            return None
        if season is not None:
            params['season'] = season

        return await self._fetch("player/details", PlayerDetails, params)