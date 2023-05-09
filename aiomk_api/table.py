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

from dateutil.parser import isoparse
from typing import Optional, TYPE_CHECKING

from .utils import _DictBased, _to_camel

__all__ = (
    "Table",
)

if TYPE_CHECKING:
    from datetime import datetime

    from .types.table import (
        Score as ScorePayload,
        Team as TeamPayload,
        Table as TablePayload,
    )
    from .types.tier import TierType


class Score(_DictBased):

    __slots__ = (
        "score",
        "multiplier",
        "player_id",
        "player_name",
        "player_discord_id",
        "player_country_code",
        "delta",
        "prev_mmr",
        "new_mmr",
    )

    if TYPE_CHECKING:
        score: int
        multiplier: float
        player_id: int
        player_name: str
        player_discord_id: Optional[str]
        player_country_code: Optional[str]
        delta: Optional[int]
        prev_mmr: Optional[int]
        new_mmr: Optional[int]

    def __init__(self, data: ScorePayload) -> None:
        self._update(data)

    def _update(self, data: ScorePayload) -> None:
        self.score = data["score"]
        self.multiplier = data["multiplier"]
        self.player_id = data["playerId"]
        self.player_name = data["playerName"]
        self.player_discord_id = data.get("playerDiscordId")
        self.player_country_code = data.get("playerCountryCode")
        self.delta = data.get("delta")
        self.prev_mmr = data.get("prevMmr")
        self.new_mmr = data.get("newMmr")

    def to_dict(self) -> ScorePayload:
        return {_to_camel(attr): getattr(self, attr) for attr in self.__slots__}


class Team(_DictBased):

    __slots__ = (
        "rank",
        "scores",
    )

    if TYPE_CHECKING:
        rank: int
        scores: list[Score]

    def __init__(self, data: TeamPayload) -> None:
        self._update(data)

    def _update(self, data: TeamPayload) -> None:
        self.rank = data["rank"]
        self.scores = [Score(score) for score in data["scores"]]

    def to_dict(self) -> TeamPayload:
        return {
            "rank" : self.rank,
            "scores" : [score.to_dict() for score in self.scores],
        }


class Table(_DictBased):

    __slots__ = (
        "id",
        "score",
        "created_on",
        "verified_on",
        "deleted_on",
        "num_teams",
        "url",
        "tier",
        "teams",
        "table_message_id",
        "update_message_id",
        "author_id",
    )

    if TYPE_CHECKING:
        id: int
        score: int
        created_on: datetime
        verified_on: Optional[datetime]
        deleted_on: Optional[datetime]
        num_teams: int
        url: str
        tier: TierType
        teams: list[Team]
        table_message_id: Optional[str]
        update_message_id: Optional[str]
        author_id: Optional[str]

    def __init__(self, data: TablePayload) -> None:
        self._update(data)

    def _update(self, data: TablePayload) -> None:
        self.id = data["id"]
        self.score = data["score"]
        self.created_on = isoparse(data["createdOn"])
        self.verified_on = (
            isoparse(data["verifiedOn"]) if data.get("verifiedOn") else None
        )
        self.deleted_on = (
            isoparse(data["deletedOn"]) if data.get("deletedOn") else None
        )
        self.num_teams = data["numTeams"]
        self.url = data["url"]
        self.tier = data["tier"]
        self.teams = [Team(team) for team in data["teams"]]
        self.table_message_id = data.get("tableMessageId")
        self.update_message_id = data.get("updateMessageId")
        self.author_id = data.get("authorId")

    def to_dict(self) -> TablePayload:
        data = {}

        for attr in self.__slots__:
            if attr in ("created_on", "verified_on", "deleted_on"):
                dt: Optional[datetime] = getattr(self, attr)
                data[_to_camel(attr)] = dt.isoformat() if dt is not None else None
            elif attr == "teams":
                data["teams"] = [team.to_dict() for team in self.teams]
            else:
                data[_to_camel(attr)] = getattr(self, attr)

        return data