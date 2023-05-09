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

from typing import Optional, TYPE_CHECKING, Union


class Search:

    __slots__ = (
        "mkc_id",
        "discord_id",
        "switch_fc"
    )

    if TYPE_CHECKING:
        mkc_id: Union[int, str, None]
        discord_id: Union[int, str, None]
        switch_fc: Optional[str]

    def __init__(
        self,
        mkc_id: Union[int, str, None] = None,
        discord_id: Union[int, str, None] = None,
        switch_fc: Optional[str] = None
    ) -> None:
        self.mkc_id = mkc_id
        self.discord_id = discord_id
        self.switch_fc = switch_fc

    def __bool__(self) -> bool:
        return any((self.mkc_id, self.discord_id, self.switch_fc))

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Search)
            and self.mkc_id == __value.mkc_id
            and self.discord_id == __value.discord_id
            and self.switch_fc == __value.switch_fc
        )

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return hash((self.mkc_id, self.discord_id, self.switch_fc))

    @property
    def query(self) -> str:
        """Generates a query string for the search.

        Returns
        -------
        str
            The query string.
        """

        if self.mkc_id:
            return f"mkc={self.mkc_id}"
        elif self.discord_id:
            return f"discord={self.discord_id}"
        else:
            return f"switch={self.switch_fc}"

    def __str__(self) -> str:
        return self.query

    def __repr__(self) -> str:
        return f"<Search {self.query}>"