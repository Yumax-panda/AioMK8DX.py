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
    TYPE_CHECKING,
    TypeVar,
    Union
)

from .cache import Cache, caching_property

from .change import Bonus, Penalty
from .leaderboard import LeaderBoard
from .player import (
    Player,
    PlayerDetails,
    PartialPlayer
)
from .table import Table
from .utils import Search

if TYPE_CHECKING:
    from datetime import datetime

__all__ = (
    "HttpClient",
    "AioMKClient",
)


API_URL: Final[str] = "https://www.mk8dx-lounge.com/api/"
Response = Union[list, dict[str, Any]]
Param = Union[str, int]
T = TypeVar("T")


class HttpClient:

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        self._session = session or ClientSession()

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    async def get(self, endpoint: str, params: dict = {}) -> Optional[Response]:
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

    async def _fetch(self, endpoint: str, cls: Type[T], params: dict = {}) -> Optional[T]:
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
        Optional[T]
            The data as a class
        """

        if (data:=await self._http.get(endpoint, params=params)) is None:
            return None
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
        id: Optional[int] = None,
        name: Optional[str] = None,
        mkc_id: Optional[int] = None,
        discord_id: Optional[int] = None,
        fc: Optional[str] = None,
        season: Optional[int] = None,
    ) -> Optional[Player]:

        params = {}
        if id is not None:
            params["id"] = id
        elif name is not None:
            params["name"] = name
        elif mkc_id is not None:
            params["mkcId"] = mkc_id
        elif discord_id is not None:
            params["discordId"] = discord_id
        elif fc is not None:
            params["fc"] = fc
        else:
            return None
        if season is not None:
            params["season"] = season

        return await self._fetch("player", Player, params)

    @caching_property
    async def get_player_details(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        season: Optional[int] = None,
    ) -> Optional[PlayerDetails]:
        params = {}
        if id is not None:
            params["id"] = id
        elif name is not None:
            params["name"] = name
        else:
            return None
        if season is not None:
            params["season"] = season

        return await self._fetch("player/details", PlayerDetails, params)

    @caching_property
    async def get_player_list(
        self,
        min_mmr: Optional[int] = None,
        max_mmr: Optional[int] = None,
        season: Optional[int] = None,
    ) -> list[PartialPlayer]:
        params = {}
        if min_mmr is not None:
            params["minMmr"] = min_mmr
        if max_mmr is not None:
            params["maxMmr"] = max_mmr
        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("player/list", params)) is None:
            return []
        else:
            return [PartialPlayer(player) for player in data["players"]]

    @caching_property
    async def get_leaderboard(
        self,
        season: int,
        skip: int = 0,
        page_size: int = 50,
        search: Union[str, Search, None] = None,
        country: Optional[str] = None,
        min_mmr: Optional[int] = None,
        max_mmr: Optional[int] = None,
        min_events_played: Optional[int] = None,
        max_events_played: Optional[int] = None,
    ) -> Optional[LeaderBoard]:

        params = {
            "season": season,
            "skip": skip,
            "pageSize": page_size,
        }

        if search:
            params["search"] = str(search)
        if country is not None:
            params["country"] = country
        if min_mmr is not None:
            params["minMmr"] = min_mmr
        if max_mmr is not None:
            params["maxMmr"] = max_mmr
        if min_events_played is not None:
            params["minEventsPlayed"] = min_events_played
        if max_events_played is not None:
            params["maxEventsPlayed"] = max_events_played

        return await self._fetch("player/leaderboard", LeaderBoard, params)

    @caching_property
    async def get_table(self, table_id: int) -> Optional[Table]:
        return await self._fetch("table", Table, {"tableId": table_id})

    @caching_property
    async def get_tables(
        self,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        season: Optional[int] = None,
    ) -> list[Table]:
        params = {}

        if after is not None:
            params["from"] = after.isoformat()
        if before is not None:
            params["to"] = before.isoformat()
        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("table/list", params)) is None:
            return []
        else:
            return [Table(table) for table in data]

    @caching_property
    async def get_table_unverified(self, season: Optional[int] = None) -> list[Table]:
        params = {}

        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("table/unverified", params)) is None:
            return []
        else:
            return [Table(table) for table in data]

    @caching_property
    async def get_bonus(self, id: int) -> Optional[Bonus]:
        return await self._fetch("bonus", Bonus, {"id": id})

    @caching_property
    async def get_bonuses(self, name: str, season: Optional[int] = None) -> list[Bonus]:
        params = {"name": name}

        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("bonus/list", params)) is None:
            return []
        else:
            return [Bonus(bonus) for bonus in data]

    @caching_property
    async def get_penalty(self, id: int) -> Optional[Penalty]:
        return await self._fetch("penalty", Penalty, {"id": id})

    @caching_property
    async def get_penalties(
        self,
        name: str,
        is_strike: Optional[bool] = None,
        after: Optional[datetime] = None,
        include_deleted: bool = False,
        season: Optional[int] = None,
    ) -> list[Penalty]:
        params = {
            "name": name,
            "includeDeleted": include_deleted,
        }

        if is_strike is not None:
            params["isStrike"] = is_strike
        if after is not None:
            params["from"] = after.isoformat()
        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("penalty/list", params)) is None:
            return []
        else:
            return [Penalty(penalty) for penalty in data]