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
    "Bonus",
    "Penalty",
)

if TYPE_CHECKING:
    from datetime import datetime

    from .types.change import (
        _ChangeBase as _ChangeBasePayload,
        Bonus as BonusPayload,
        Penalty as PenaltyPayload,
    )


class _ChangeBase:

    __slots__ = (
        "id",
        "season",
        "awarded_on",
        "prev_mmr",
        "new_mmr",
        "amount",
        "deleted_on",
        "player_id",
        "player_name",
    )

    if TYPE_CHECKING:
        id: int
        season: int
        awarded_on: datetime
        prev_mmr: int
        new_mmr: int
        amount: int
        deleted_on: Optional[datetime]
        player_id: int
        player_name: str

    def __init__(self, data: _ChangeBasePayload) -> None:
        self._update(data)

    def _update(self, data: _ChangeBasePayload) -> None:
        self.id = data["id"]
        self.season = data["season"]
        self.awarded_on = isoparse(data["awardedOn"])
        self.prev_mmr = data["prevMmr"]
        self.new_mmr = data["newMmr"]
        self.amount = data["amount"]
        self.deleted_on = isoparse(data["deletedOn"]) if data["deletedOn"] else None
        self.player_id = data["playerId"]
        self.player_name = data["playerName"]


class Bonus(_ChangeBase):

    def __init__(self, data: BonusPayload) -> None:
        super().__init__(data)


class Penalty(_ChangeBase):

    __slots__ = (
        "id",
        "season",
        "awarded_on",
        "prev_mmr",
        "new_mmr",
        "amount",
        "deleted_on",
        "player_id",
        "player_name",
        "is_strike",
    )

    if TYPE_CHECKING:
        id: int
        season: int
        awarded_on: datetime
        prev_mmr: int
        new_mmr: int
        amount: int
        deleted_on: Optional[datetime]
        player_id: int
        player_name: str
        is_strike: bool

    def __init__(self, data: PenaltyPayload) -> None:
        super().__init__(data)
        self.is_strike = data["is_strike"]