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
    Callable,
    Type,
    TypeVar,
    TYPE_CHECKING,
    Iterator,
    Optional,
    SupportsIndex,
    Union,
    overload
)

from .player import LeaderBoardPlayer
from .utils import _DictBased

__all__ = (
    "LeaderBoard",
)

if TYPE_CHECKING:
    from .types.leaderboard import LeaderBoard as LeaderBoardPayload

T = TypeVar("T", bound="LeaderBoard")


class LeaderBoard(_DictBased):
    """Represents a LeaderBoard.

    .. container:: operations

        .. describe:: x == y

            Checks if two LeaderBoards are equal.

        .. describe:: len(x)

            Returns the number of players in the LeaderBoard.

        .. describe:: x[y]

            Returns the player at the specified index.

        .. describe:: contains x

            Checks if a player is in the LeaderBoard.

        .. describe:: bool(x)

            Checks if the LeaderBoard is not empty.

        .. describe:: iter(x)

            Returns an iterator for the LeaderBoard.

    Attributes
    ----------
    total_players: int
        The total number of players in the LeaderBoard.
    data: list[LeaderBoardPlayer]
        The players in the LeaderBoard.
    """

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

    @overload
    def __getitem__(self, __index: SupportsIndex) -> LeaderBoardPlayer:
        ...
    @overload
    def __getitem__(self, __index: slice) -> LeaderBoard:
        ...
    def __getitem__(self, __index: Union[SupportsIndex, slice]) -> Union[LeaderBoardPlayer, LeaderBoard]:

        if isinstance(__index, slice):
            return LeaderBoard._create(self.data[__index])
        else:
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

    @classmethod
    def _create(cls: Type[T], players: list[LeaderBoardPlayer]) -> T:
        """Creates a LeaderBoard object.

        Parameters
        ----------
        cls : Type[T]
            The class to create an instance of.
        players : list[LeaderBoardPlayer]
            The players to create the LeaderBoard with.

        Returns
        -------
        T
            The LeaderBoard object created.
        """

        self = cls.__new__(cls) # bypass __init__

        self.total_players = len(players)
        self.data = [p.copy() for p in players]
        return self


    def find(self, predicate: Callable[[LeaderBoardPlayer], bool]) -> Optional[LeaderBoardPlayer]:
        """Find a player in the LeaderBoard.

        Parameters
        ----------
        predicate: Callable[[LeaderBoardPlayer], bool]
            A function that takes a LeaderBoardPlayer and returns a bool.

        Returns
        -------
        Optional[LeaderBoardPlayer]
            The player found, or None if not found.
        """

        return next((x for x in self.data if predicate(x)), None)

    def find_all(self, predicate: Callable[[LeaderBoardPlayer], bool]) -> LeaderBoardPlayer:
        """Find all players in the LeaderBoard.

        Parameters
        ----------
        predicate: Callable[[LeaderBoardPlayer], bool]
            A function that takes a LeaderBoardPlayer and returns a bool.

        Returns
        -------
        list[LeaderBoardPlayer]
            The players found.
        """

        return LeaderBoard._create([x for x in self.data if predicate(x)])