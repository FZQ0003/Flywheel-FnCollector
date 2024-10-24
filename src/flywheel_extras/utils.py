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
