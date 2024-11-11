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


def get_method_class(method: Callable) -> type | None:
    if not (module := inspect.getmodule(method)):
        return
    for _, cls in inspect.getmembers(module, inspect.isclass):
        cls_list = method.__qualname__.split('.')
        if cls.__name__ != cls_list[0]:
            continue
        for attr in cls_list[1:-1]:
            if not (cls := getattr(cls, attr, None)):
                break
        # DO NOT USE GETATTR, ENTITY != METHOD
        if hasattr(cls, cls_list[-1]):
            return cls


def get_common_ancestor(*classes: type) -> type:
    common_mro = classes[0].mro()
    for cls in classes[1:]:
        cls_mro = cls.mro()
        common_mro = [ancestor for ancestor in common_mro if ancestor in cls_mro]
    return common_mro[0]
