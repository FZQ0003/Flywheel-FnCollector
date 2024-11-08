from abc import abstractmethod

from typing_extensions import Self


class FnCollection:
    @classmethod
    @abstractmethod
    def from_self(cls, self: Self) -> Self:
        return self
