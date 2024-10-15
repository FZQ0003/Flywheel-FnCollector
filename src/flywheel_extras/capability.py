from __future__ import annotations

from dataclasses import dataclass
from functools import wraps

from .collector import FnCollector


@dataclass
class Capability:
    # namespace: str = 'default'

    def __getattribute__(self, name: str):
        if isinstance(attr := object.__getattribute__(self, name), FnCollector):
            @wraps(attr.base)
            def wrapper(*args, **kwargs):
                return attr(self, *args, **kwargs)

            return wrapper
        return attr
