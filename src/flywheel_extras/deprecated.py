import warnings
from abc import abstractmethod

from typing_extensions import Self

from .utils import get_common_ancestor


class FnCollectorContainer:
    def __init_subclass__(cls, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings('once')
            warnings.warn('FnCollectorContainer is deprecated, just delete it', DeprecationWarning)


class FnCollection:
    def __init_subclass__(cls, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings('once')
            warnings.warn(
                'FnCollection is deprecated, delete it and replace from_self with __cross__',
                DeprecationWarning
            )

    @classmethod
    def __cross__(cls, other: Self) -> Self:
        ancestor = get_common_ancestor(cls, type(other))
        if issubclass(ancestor, FnCollection) and ancestor is not FnCollection:
            return cls.from_self(other)
        return other

    @classmethod
    @abstractmethod
    def from_self(cls, self: Self) -> Self:
        return self
