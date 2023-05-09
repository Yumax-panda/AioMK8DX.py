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

from typing import Literal, Optional, TypedDict


ReasonType = Literal[
    "Placement",
    "Table",
    "Penalty",
    "Strike",
    "Bonus",
    "TableDelete",
    "PenaltyDelete",
    "StrikeDelete",
    "BonusDelete",
]


TierType = Literal[
    "X", "S", "A", "AB", "B", "BC", "C", "CD", "D", "DE", "E", "EF", "F", "FG", "G", "SQ"
]


class MmrChange(TypedDict):
    changeId: Optional[int]
    newMmr: int
    mmrDelta: int
    reason: ReasonType
    time: str
    score: Optional[int]
    partnerScores: Optional[list[int]]
    partnerIds: Optional[list[int]]
    tier: Optional[TierType]
    numTeams: Optional[int]


class NameChange(TypedDict):
    name: str
    changedOn: str


class PlayerDetails(TypedDict):
    playerId: int
    name: str
    mkcId: int
    countryCode: Optional[str]
    countryName: Optional[str]
    switchFc: Optional[str]
    isHidden: bool
    season: int
    mmr: Optional[int]
    maxMmr: Optional[int]
    overallRank: Optional[int]
    eventsPlayed: int
    winRate: Optional[float]
    winsLastTen: int
    lossesLastTen: int
    gainLossLastTen: Optional[int]
    largestGain: Optional[int]
    largestGainTableId: Optional[int]
    largestLoss: Optional[int]
    largestLossTableId: Optional[int]
    averageScore: Optional[float]
    averageLastTen: Optional[float]
    partnerAverage: Optional[float]
    mmrChanges: list[MmrChange]
    nameHistory: list[NameChange]
    rank: str