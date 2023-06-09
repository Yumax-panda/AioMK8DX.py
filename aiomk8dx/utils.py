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
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    TYPE_CHECKING,
    Union,
    overload
)


__all__ = (
    "_DictBased",
    "Search",
    "_to_camel",
    "cached_slot_property"
)

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class _DictBased:
    """A base class for objects that can be converted to a dictionary."""

    __slots__ = ()

    def to_dict(self) -> dict:
        """Converts this object to a dictionary.

        Returns
        -------
        dict
            The dictionary.
        """

        raise NotImplementedError

    def _update(self, data: dict) -> None:
        """Updates this object with the given data.

        Parameters
        ----------
        data: dict
            The data to update this object with.
        """

        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.to_dict()}>"

    @classmethod
    def copy(cls: Type[T], self: T) -> T:
        """Copies this object.

        Parameters
        ----------
        cls : Type[T]
            The class of the object.
        self : T
            The object to copy.

        Returns
        -------
        T
            The copied object.
        """

        return cls._update(self.to_dict())


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


def _to_camel(string: str) -> str:
    """Converts a string to camel case.

    Parameters
    ----------
    string: str
        The string to convert.

    Returns
    -------
    str
        The converted string.
    """

    return "".join(word.capitalize() for word in string.split("_"))


class CachedSlotProperty(Generic[T, T_co]):

    __slots__ = (
        "name",
        "function",
        "__doc__"
    )

    def __init__(self, name: str, function: Callable[[T], T_co]) -> None:
        self.name = name
        self.function = function
        self.__doc__ = getattr(function, "__doc__")

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> CachedSlotProperty[T, T_co]:
        ...

    @overload
    def __get__(self, instance: T, owner: Type[T]) -> T_co:
        ...

    def __get__(self, instance: Optional[T], owner: Type[T]) -> Any:
        if instance is None:
            return self

        try:
            return getattr(instance, self.name)
        except AttributeError:
            value = self.function(instance)
            setattr(instance, self.name, value)
            return value


def cached_slot_property(name: str) -> Callable[[Callable[[T], T_co]], CachedSlotProperty[T, T_co]]:
    """Creates a cached slot property.

    Parameters
    ----------
    name: str
        The name of the slot.

    Returns
    -------
    Callable[[Callable[[T], T_co]], CachedSlotProperty[T, T_co]]
        The created property.
    """

    def decorator(function: Callable[[T], T_co]) -> CachedSlotProperty[T, T_co]:
        return CachedSlotProperty(name, function)

    return decorator