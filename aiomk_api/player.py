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

__all__ = (
    "MinimalPlayer",
    "PartialPlayer",
    "Player",
    "PlayerDetails",
    "LeaderBoardPlayer",
)

if TYPE_CHECKING:
    from datetime import datetime

    from .types.player import (
        ReasonType,
        MmrChange as MmrChangePayload,
        NameChange as NameChangePayload,
        _MinimalPlayer as MinimalPlayerPayload,
        Player as PlayerPayload,
        PlayerDetails as PlayerDetailsPayload,
        PartialPlayer as PartialPlayerPayload,
        LeaderBoardPlayer as LeaderBoardPlayerPayload
    )
    from types.tier import TierType


class MmrChange:

    __slots__ = (
        "change_id",
        "new_mmr",
        "mmr_delta",
        "reason",
        "time",
        "score",
        "partner_scores",
        "partner_ids",
        "tier",
        "numTeams"
    )

    if TYPE_CHECKING:
        change_id: Optional[int]
        new_mmr: int
        mmr_delta: int
        reason: ReasonType
        time: datetime
        score: Optional[int]
        partner_scores: list[int]
        partner_ids: list[int]
        tier: TierType
        numTeams: Optional[int]

    def __init__(self, data: MmrChangePayload) -> None:
        self._update(data)

    def _update(self, data: MmrChangePayload) -> None:
        self.change_id = data.get("changeId")
        self.new_mmr = data["newMmr"]
        self.mmr_delta = data["mmrDelta"]
        self.reason = data["reason"]
        self.time = isoparse(data["time"])
        self.score = data.get("score")
        self.partner_scores = data.get("partnerScores", [])
        self.partner_ids = data.get("partnerIds", [])
        self.tier = data.get("tier")
        self.numTeams = data.get("numTeams")


class NameChange:

    __slots__ = (
        "name",
        "changed_on"
    )

    if TYPE_CHECKING:
        name: str
        changed_on: datetime

    def __init__(self, data: NameChangePayload) -> None:
        self._update(data)

    def _update(self, data: NameChangePayload) -> None:
        self.name = data["name"]
        self.changed_on = isoparse(data["changedOn"])


class _MinimalPlayer:

    __slots__ = (
        "name",
        "mmr",
    )

    if TYPE_CHECKING:
        name: str
        mmr: Optional[int]

    def _update(self, data: MinimalPlayerPayload) -> None:
        self.name = data["name"]
        self.mmr = data.get("mmr")


class Player(_MinimalPlayer):

    __slots__ = (
        "name",
        "mmr",
        "id",
        "mkc_id",
        "discord_id",
        "country_code",
        "switch_fc",
        "is_hidden",
        "max_mmr"
    )

    if TYPE_CHECKING:
        name: str
        mmr: Optional[int]
        id: int
        mkc_id: int
        discord_id: Optional[str]
        country_code: Optional[str]
        switch_fc: Optional[str]
        is_hidden: bool
        max_mmr: Optional[int]

    def __init__(self, data: PlayerPayload) -> None:
        self._update(data)

    def _update(self, data: PlayerPayload) -> None:
        super()._update(data)
        self.id = data["id"]
        self.mkc_id = data["mkcId"]
        self.discord_id = data.get("discordId")
        self.country_code = data.get("countryCode")
        self.switch_fc = data.get("switchFc")
        self.is_hidden = data["isHidden"]
        self.max_mmr = data.get("maxMmr")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Player) and __value.id == self.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return self.id >> 22


class PartialPlayer(_MinimalPlayer):

    __slots__ = (
        "name",
        "mmr",
        "mkc_id",
        "events_played",
        "discord_id"
    )

    if TYPE_CHECKING:
        name: str
        mmr: Optional[int]
        mkc_id: int
        events_played: int
        discord_id: Optional[str]

    def __init__(self, data: PartialPlayerPayload) -> None:
        self._update(data)

    def _update(self, data: PartialPlayerPayload) -> None:
        super()._update(data)
        self.mkc_id = data["mkcId"]
        self.events_played = data["eventsPlayed"]
        self.discord_id = data.get("discordId")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PartialPlayer) and __value.mkc_id == self.mkc_id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return self.mkc_id >> 22


class PlayerDetails(_MinimalPlayer):

    __slots__ = (
        "name",
        "mmr",
        "player_id",
        "mkc_id",
        "country_code",
        "country_name",
        "switch_fc",
        "is_hidden",
        "season",
        "max_mmr",
        "overall_rank",
        "events_played",
        "win_rate",
        "wins_last_ten",
        "losses_last_ten",
        "gain_loss_last_ten",
        "largest_gain",
        "largest_gain_table_id",
        "largest_loss",
        "largest_loss_table_id",
        "average_score",
        "average_last_ten",
        "partner_average",
        "mmr_changes",
        "name_history",
        "rank"
    )

    if TYPE_CHECKING:
        name: str
        mmr: Optional[int]
        player_id: int
        mkc_id: int
        country_code: Optional[str]
        country_name: Optional[str]
        switch_fc: Optional[str]
        is_hidden: bool
        season: int
        max_mmr: Optional[int]
        overall_rank: Optional[int]
        events_played: int
        win_rate: Optional[float]
        wins_last_ten: int
        losses_last_ten: int
        gain_loss_last_ten: Optional[int]
        largest_gain: Optional[int]
        largest_gain_table_id: Optional[int]
        largest_loss: Optional[int]
        largest_loss_table_id: Optional[int]
        average_score: Optional[float]
        average_last_ten: Optional[float]
        partner_average: Optional[float]
        mmr_changes: list[MmrChange]
        name_history: list[NameChange]
        rank: str

    def __init__(self, data: PlayerDetailsPayload) -> None:
        self._update(data)

    def _update(self, data: _MinimalPlayer) -> None:
        super()._update(data)
        self.player_id = data["playerId"]
        self.mkc_id = data["mkcId"]
        self.country_code = data.get("countryCode")
        self.country_name = data.get("countryName")
        self.switch_fc = data.get("switchFc")
        self.is_hidden = data["isHidden"]
        self.season = data["season"]
        self.max_mmr = data.get("maxMmr")
        self.overall_rank = data.get("overallRank")
        self.events_played = data["eventsPlayed"]
        self.win_rate = data.get("winRate")
        self.wins_last_ten = data["winsLastTen"]
        self.losses_last_ten = data["lossesLastTen"]
        self.gain_loss_last_ten = data.get("gainLossLastTen")
        self.largest_gain = data.get("largestGain")
        self.largest_gain_table_id = data.get("largestGainTableId")
        self.largest_loss = data.get("largestLoss")
        self.largest_loss_table_id = data.get("largestLossTableId")
        self.average_score = data.get("averageScore")
        self.average_last_ten = data.get("averageLastTen")
        self.partner_average = data.get("partnerAverage")
        self.mmr_changes = [MmrChange(x) for x in data.get("mmrChanges", [])]
        self.name_history = [NameChange(x) for x in data.get("nameHistory", [])]
        self.rank = data["rank"]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, PlayerDetails) and __value.player_id == self.player_id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return self.player_id >> 22


class LeaderBoardPlayer(_MinimalPlayer):

    __slots__ = (
        "name",
        "mmr",
        "id",
        "wins_last_ten",
        "losses_last_ten",
        "events_played",
        "overall_rank",
        "country_code",
        "max_mmr",
        "win_rate",
        "gain_loss_last_ten",
        "largest_gain",
        "largest_loss",
        "max_rank",
        "max_mmr_rank"
    )

    if TYPE_CHECKING:
        name: str
        mmr: Optional[int]
        id: int
        wins_last_ten: int
        losses_last_ten: int
        events_played: int
        overall_rank: Optional[int]
        country_code: Optional[str]
        max_mmr: Optional[int]
        win_rate: Optional[float]
        gain_loss_last_ten: Optional[int]
        largest_gain: Optional[int]
        largest_loss: Optional[int]
        max_rank: Optional[str]
        max_mmr_rank: Optional[str]

    def __init__(self, data: LeaderBoardPlayerPayload) -> None:
        self._update(data)

    def _update(self, data: LeaderBoardPlayerPayload) -> None:
        super()._update(data)
        self.id = data["id"]
        self.wins_last_ten = data["winsLastTen"]
        self.losses_last_ten = data["lossesLastTen"]
        self.events_played = data["eventsPlayed"]
        self.overall_rank = data.get("overallRank")
        self.country_code = data.get("countryCode")
        self.max_mmr = data.get("maxMmr")
        self.win_rate = data.get("winRate")
        self.gain_loss_last_ten = data.get("gainLossLastTen")
        self.largest_gain = data.get("largestGain")
        self.largest_loss = data.get("largestLoss")
        self.max_rank = data.get("maxRank")
        self.max_mmr_rank = data.get("maxMmrRank")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, LeaderBoardPlayer) and __value.id == self.id

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return self.id >> 22