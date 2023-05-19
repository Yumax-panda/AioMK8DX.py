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
    Sequence,
    Union
)
from itertools import zip_longest

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
        """Gets data from the api

        Parameters
        ----------
        endpoint : str
            The endpoint to get from
        params : dict, optional
            Parameters of the request, by default {}

        Returns
        -------
        Optional[Response]
            The data from the api
        """

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
            more info: https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

        Returns
        -------
        list[Optional[T]]
            The data as a class
        """

        tasks = [self._http.get(endpoint, params=param) for param in params]
        results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)

        return [cls(data) if data is not None else None for data in results]


    async def get_player(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        mkc_id: Optional[int] = None,
        discord_id: Optional[int] = None,
        fc: Optional[str] = None,
        season: Optional[int] = None,
    ) -> Optional[Player]:
        """Gets a player from the api

        Parameters
        ----------
        id : Optional[int], optional
            The id of the player, by default None
        name : Optional[str], optional
            The name of the player, by default None
        mkc_id : Optional[int], optional
            The mkc id of the player, by default None
        discord_id : Optional[int], optional
            The discord id of the player, by default None
        fc : Optional[str], optional
            The switch friend code of the player, by default None
        season : Optional[int], optional
            The season to get the player from, by default None

        Returns
        -------
        Optional[Player]
            If successful, the player, else None
        """

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

    async def get_players(
        self,
        ids: Sequence[int] = [],
        names: Sequence[str] = [],
        mkc_ids: Sequence[int] = [],
        discord_ids: Sequence[int] = [],
        fcs: Sequence[str] = [],
        season: int = None,
        return_exceptions: bool = False
    ) -> list[Optional[Player]]:
        """Gets players from the api. This methods is nearly identical to get_player, but can get multiple players at once

        Parameters
        ----------
        ids : Sequence[int], optional
            The ids of the players, by default []
        names : Sequence[str], optional
            The names of the players, by default []
        mkc_ids : Sequence[int], optional
            The mkc ids of the players, by default []
        discord_ids : Sequence[int], optional
            The discord ids of the players, by default []
        fcs : Sequence[str], optional
            The switch friend codes of the players, by default []
        season : int, optional
            The season to get the players from, by default None
        return_exceptions : bool, optional
            whether to return exceptions, by default False
            more info: https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

        Returns
        -------
        list[Optional[Player]]
            If successful, the players, else None
        """

        params_list = []

        for id, name, mkc_id, discord_id, fc in zip_longest(
            ids,
            names,
            mkc_ids,
            discord_ids,
            fcs,
        ):
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

            if season is not None:
                params["season"] = season
            params_list.append(params)
        return await self._fetch_many("player", Player, params_list, return_exceptions=return_exceptions)


    async def get_player_details(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        season: Optional[int] = None,
    ) -> Optional[PlayerDetails]:
        """Gets a player's details from the api

        Parameters
        ----------
        id : Optional[int], optional
            The id of the player, by default None
        name : Optional[str], optional
            The name of the player, by default None
        season : Optional[int], optional
            The season to get the player from, by default None

        Returns
        -------
        Optional[PlayerDetails]
            If successful, the player's details, else None
        """

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


    async def get_player_list(
        self,
        min_mmr: Optional[int] = None,
        max_mmr: Optional[int] = None,
        season: Optional[int] = None,
    ) -> list[PartialPlayer]:
        """Gets a list of players from the api

        Parameters
        ----------
        min_mmr : Optional[int], optional
            The minimum mmr of the players, by default None
        max_mmr : Optional[int], optional
            The maximum mmr of the players, by default None
        season : Optional[int], optional
            The season to get the players from, by default None

        Returns
        -------
        list[PartialPlayer]
            If successful, the players, else empty list
        """

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
        """Gets a leaderboard from the api

        Parameters
        ----------
        season : int
            The season to get the leaderboard from
        skip : int, optional
            If specified, the player with the highest MMR is omitted by that number, by default 0
        page_size : int, optional
            The number of players to get, by default 50
            You should set this from 1 to 100
        search : Union[str, Search, None], optional
            The search query, by default None
            You can use the utils.Search class to make a search query.
            Available search fields: mkc_id, discord_id, switch_friend_code
        country : Optional[str], optional
            The country to get the leaderboard from, by default None
        min_mmr : Optional[int], optional
            The minimum mmr of the players, by default None
        max_mmr : Optional[int], optional
            The maximum mmr of the players, by default None
        min_events_played : Optional[int], optional
            The minimum events played of the players, by default None
        max_events_played : Optional[int], optional
            The maximum events played of the players, by default None

        Returns
        -------
        Optional[LeaderBoard]
            If successful, the leaderboard, else None

        Examples
        --------
        >>> async with AioMKClient() as client:
        >>>    search = Search(switch_fc="1234-5678-1234")
        >>>    leaderboard = await client.get_leaderboard(8, search=search)
        >>>
        >>>    # You can also use a string instead of a Search object
        >>>    search = "switch=1234-5678-1234"
        """

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


    async def get_table(self, table_id: int) -> Optional[Table]:
        """Gets a table from the api

        Parameters
        ----------
        table_id : int
            The id of the table

        Returns
        -------
        Optional[Table]
            If successful, the table, else None
        """
        return await self._fetch("table", Table, {"tableId": table_id})


    async def get_tables(
        self,
        after: Optional[datetime] = None,
        before: Optional[datetime] = None,
        season: Optional[int] = None,
    ) -> list[Table]:
        """Gets a list of tables from the api

        Parameters
        ----------
        after : Optional[datetime], optional
            The date to get the tables after, by default None. Timezone is UTC.
        before : Optional[datetime], optional
            The date to get the tables before, by default None. Timezone is UTC.
        season : Optional[int], optional
            The season to get the tables from, by default None

        Returns
        -------
        list[Table]
            If successful, the tables, else empty list
        """
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


    async def get_table_unverified(self, season: Optional[int] = None) -> list[Table]:
        """Gets a list of unverified tables from the api

        Parameters
        ----------
        season : Optional[int], optional
            The season to get the tables from, by default None

        Returns
        -------
        list[Table]
            If successful, the tables, else empty list
        """

        params = {}

        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("table/unverified", params)) is None:
            return []
        else:
            return [Table(table) for table in data]


    async def get_bonus(self, id: int) -> Optional[Bonus]:
        """Gets a bonus from the api

        Parameters
        ----------
        id : int
            The id of the bonus

        Returns
        -------
        Optional[Bonus]
            If successful, the bonus, else None
        """
        return await self._fetch("bonus", Bonus, {"id": id})


    async def get_bonuses(self, name: str, season: Optional[int] = None) -> list[Bonus]:
        """Gets a list of bonuses from the api

        Parameters
        ----------
        name : str
            The name of the player who got the bonus
        season : Optional[int], optional
            The season to get the bonuses from, by default None

        Returns
        -------
        list[Bonus]
            If successful, the bonuses, else empty list
        """

        params = {"name": name}

        if season is not None:
            params["season"] = season

        if (data:=await self._http.get("bonus/list", params)) is None:
            return []
        else:
            return [Bonus(bonus) for bonus in data]


    async def get_penalty(self, id: int) -> Optional[Penalty]:
        """Gets a penalty from the api

        Parameters
        ----------
        id : int
            The id of the penalty

        Returns
        -------
        Optional[Penalty]
            If successful, the penalty, else None
        """

        return await self._fetch("penalty", Penalty, {"id": id})


    async def get_penalties(
        self,
        name: str,
        is_strike: Optional[bool] = None,
        after: Optional[datetime] = None,
        include_deleted: bool = False,
        season: Optional[int] = None,
    ) -> list[Penalty]:
        """Gets a list of penalties from the api

        Parameters
        ----------
        name : str
            The name of the player who got the penalty
        is_strike : Optional[bool], optional
            If True, only get strikes
        after : Optional[datetime], optional
            The date to get the penalties after, by default None. Timezone is UTC.
        include_deleted : bool, optional
            If True, include deleted penalties, by default False
        season : Optional[int], optional
            The season to get the penalties from, by default None

        Returns
        -------
        list[Penalty]
            If successful, the penalties, else empty list
        """

        params = {
            "name": name,
            "includeDeleted": str(include_deleted),
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