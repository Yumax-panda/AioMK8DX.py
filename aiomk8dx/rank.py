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

from typing import (
    Optional,
    Type,
    TYPE_CHECKING,
    TypeVar
)

from .utils import _DictBased

T = TypeVar("T", bound="Rank")

__all__ = ("Rank",)

if TYPE_CHECKING:
    from .types.rank import Rank as RankPayload, Division


class Rank(_DictBased):

    __slots__ = (
        "division",
        "level",
        "name"
    )

    if TYPE_CHECKING:
        division: Division
        level: Optional[int]
        name: str

    def __init__(self, data: RankPayload) -> None:
        self._update(data)

    def _update(self, data: RankPayload) -> None:
        self.division = data["division"]
        self.level = data.get("level")
        self.name = data["name"]

    def to_dict(self) -> RankPayload:
        return {
            "division": self.division,
            "level": self.level,
            "name": self.name
        }

    @classmethod
    def from_nick(cls: Type[T], nick: str) -> T:
        """Create a rank from a nick."""
        data: RankPayload = {"name": nick}

        if ' ' in nick:
            division, level = nick.split(' ', maxsplit=1)
            data["division"] = division
            data["level"] = int(level)
        else:
            data["division"] = nick
        return cls(data)
