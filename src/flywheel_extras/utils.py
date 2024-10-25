from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from flywheel.typing import P, R


def get_var_names(func: Callable) -> tuple[str, ...]:
    return tuple(inspect.signature(func).parameters.keys())


def bind_args(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> dict[str, Any]:
    bound = inspect.signature(func).bind(*args, **kwargs)
    bound.apply_defaults()
    return bound.arguments


def dict_intersection(*dicts: dict[Any, None]) -> dict[Any, None]:
    return {_k: _v for _d in dicts for _k, _v in _d.items()}
