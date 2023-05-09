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

from aiomk_api.types.change import _ChangeBase as _ChangeBasePayload

from .utils import _DictBased, _to_camel

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


class _ChangeBase(_DictBased):

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

    def to_dict(self) -> _ChangeBasePayload:
        """Converts the object to a dict.

        Returns
        -------
        dict
            The object as a dict.
        """

        data = {}

        for attr in (
            "id",
            "season",
            "awarded_on",
            "prev_mmr",
            "new_mmr",
            "amount",
            "deleted_on",
            "player_id",
            "player_name",
        ):
            if attr in ("awarded_on", "deleted_on"):
                dt: Optional[datetime] = getattr(self, attr)
                data[_to_camel(attr)] = dt.isoformat() if dt is not None else None
            else:
                data[_to_camel(attr)] = getattr(self, attr)

        return data


class Bonus(_ChangeBase):

    def __init__(self, data: BonusPayload) -> None:
        super().__init__(data)

    def to_dict(self) -> BonusPayload:
        return super().to_dict()


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
        self.is_strike = data["isStrike"]

    def to_dict(self) -> PenaltyPayload:
        data = super().to_dict()
        data["isStrike"] = self.is_strike
        return data