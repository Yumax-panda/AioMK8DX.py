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
    Coroutine,
    TYPE_CHECKING,
    TypeVar
)
from typing_extensions import TypeAlias, ParamSpec


__all__ = (
    "Cache",
    "caching_property",
)

if TYPE_CHECKING:
    from .client import AioMKClient

T = TypeVar("T")
P = ParamSpec("P")
Key: TypeAlias = tuple[tuple[Any, ...], frozenset[tuple[str, Any]], str]


class Cache:
    data: dict[Key, Any] = {}

    def put(self, key: Key, value: object) -> Any:
        self.data[key] = value


def caching_property(coro: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
    """A decorator that caches the result of a coroutine.

    Parameters
    ----------
    coro: Callable
        The coroutine to cache.

    Returns
    -------
    Callable
        The coroutine with caching.
    """

    async def wrapper(client: AioMKClient, *args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()), coro.__qualname__)
        if key in client._cache.data:
            return client._cache.data[key]

        result = await coro(client, *args, **kwargs)
        client._cache.put(key, result)
        return result

    return wrapper