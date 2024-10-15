from __future__ import annotations

from typing import Any, Generic, overload, TypeVar

from flywheel.globals import INSTANCE_CONTEXT_VAR
from typing_extensions import Self

T = TypeVar('T')


class OptionalInstanceOf(Generic[T]):
    target: type[T]
    default: T | None

    def __init__(self, target: type[T], default: T | None = None) -> None:
        self.target = target
        self.default = default

    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...

    @overload
    def __get__(self, instance: Any, owner: type) -> T | None: ...

    def __get__(self, instance: Any, owner: type):
        if instance is None:
            return self

        return INSTANCE_CONTEXT_VAR.get().instances.get(self.target, self.default)
