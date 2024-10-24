from __future__ import annotations

from dataclasses import dataclass
from functools import wraps

from .collector import FnCollector
from .utils import get_var_names


@dataclass
class FnCollectorContainer:
    def __getattribute__(self, name: str):
        if isinstance(attr := super().__getattribute__(name), FnCollector):
            if 'self' in get_var_names(attr.base):
                @wraps(attr.base)
                def wrapper(*args, **kwargs):
                    return attr(self, *args, **kwargs)

                return wrapper
            return wraps(attr.base)(attr)

        return attr
