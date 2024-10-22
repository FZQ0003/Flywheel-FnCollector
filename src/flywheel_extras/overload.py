from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from flywheel.overloads import SimpleOverload


class MappingOverload(SimpleOverload):
    map_func: Callable[[Any], Any]  # (call_value) -> collect_value

    def __init__(self, name: str, mapping: Callable[[Any], Any] | Mapping[Any, Any]):
        super().__init__(name)
        self.map_func = mapping if isinstance(mapping, Callable) else lambda _: mapping.get(_, None)

    def harvest(self, scope: dict, call_value: Any) -> dict[Callable, None]:
        return super().harvest(scope, self.map_func(call_value))
