from typing import Protocol, runtime_checkable

from .typing import T


@runtime_checkable
class SupportsCrossCollection(Protocol[T]):
    @classmethod
    def __cross__(cls, other: T) -> T: ...
