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

from typing import TYPE_CHECKING, Iterator

from .player import LeaderBoardPlayer
from .utils import _DictBased

__all__ = (
    "LeaderBoard",
)

if TYPE_CHECKING:
    from .types.leaderboard import LeaderBoard as LeaderBoardPayload


class LeaderBoard(_DictBased):

    __slots__ = (
        "total_players",
        "data"
    )

    if TYPE_CHECKING:
        total_players: int
        data: list[LeaderBoardPlayer]

    def __init__(self, data: LeaderBoardPayload) -> None:
        self._update(data)

    def _update(self, data: LeaderBoardPayload) -> None:
        self.total_players = data["totalPlayers"]
        self.data = [LeaderBoardPlayer(x) for x in data["data"]]

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item: LeaderBoardPlayer) -> bool:
        return item in self.data

    def __getitem__(self, __index: int) -> LeaderBoardPlayer:
        return self.data[__index]

    def __iter__(self) -> Iterator[LeaderBoardPlayer]:
        return iter(self.data)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, LeaderBoard) and self.data == __value.data

    def __bool__(self) -> bool:
        return len(self.data) > 0

    def to_dict(self) -> LeaderBoardPayload:
        return {
            "totalPlayers": self.total_players,
            "data": [x.to_dict() for x in self.data]
        }