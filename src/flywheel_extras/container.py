from __future__ import annotations

from dataclasses import dataclass
from functools import wraps

from .collector import FnCollector


@dataclass
class FnCollectorContainer:
    def __getattribute__(self, name: str):
        if isinstance(attr := super().__getattribute__(name), FnCollector):
            @wraps(attr.base)
            def wrapper(*args, **kwargs):
                return attr(self, *args, **kwargs)

            return wrapper
        return attr
