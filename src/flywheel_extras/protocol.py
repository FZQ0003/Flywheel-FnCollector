from collections.abc import Callable
from typing import Protocol, runtime_checkable

from typing_extensions import Concatenate

from .typing import P, R, T


@runtime_checkable
class SupportsCrossCollection(Protocol[T]):
    @classmethod
    def __cross__(cls, other: T) -> T: ...


@runtime_checkable
class BoundMethod(Protocol[T, P, R]):
    __self__: T
    __func__: Callable[Concatenate[T, P], R]
    __call__: Callable[P, R]
