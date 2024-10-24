from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from flywheel.overloads import SimpleOverload


def _dummy_map_func(call_value):
    return call_value


def _dummy_predicate(collect_value, call_value):
    return collect_value == call_value


class MappingOverload(SimpleOverload):
    map_func: Callable[[Any], Any] = _dummy_map_func  # (call_value) -> collect_value

    def __init__(self, name: str, mapping: Callable[[Any], Any] | Mapping[Any, Any] | None = None):
        super().__init__(name)
        if mapping:
            self.map_func = mapping if isinstance(mapping, Callable) else lambda _: mapping.get(_, None)

    def harvest(self, scope: dict, call_value: Any) -> dict[Callable, None]:
        return super().harvest(scope, self.map_func(call_value))


class PredicateOverload(SimpleOverload):
    predicate: Callable[[Any, Any], bool] = _dummy_predicate  # (collect_value, call_value) -> bool

    def __init__(self, name: str, predicate: Callable[[Any, Any], bool] | None = None):
        super().__init__(name)
        if predicate:
            self.predicate = predicate

    def harvest(self, scope: dict, call_value: Any) -> dict[Callable, None]:
        result = {}
        for collect_value, funcs in scope.items():
            if self.predicate(collect_value, call_value):
                result.update(funcs)
        return result
