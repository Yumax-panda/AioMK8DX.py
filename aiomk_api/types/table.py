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

from typing import Optional, TypedDict

from .tier import TierType


class Score(TypedDict):
    score: int
    multiplier: float
    playerId: int
    playerName: str
    playerDiscordId: Optional[str]
    playerCountryCode: Optional[str]
    delta: Optional[int]
    prevMmr: Optional[int]
    newMmr: Optional[int]


class Team(TypedDict):
    rank: int
    scores: list[Score]


class Table(TypedDict):
    id: int
    score: int
    createdOn: str
    verifiedOn: Optional[str]
    deletedOn: Optional[str]
    numTeams: int
    url: str
    tier: TierType
    teams: list[Team]
    tableMessageId: Optional[str]
    updateMessageId: Optional[str]
    authorId: Optional[str]