from __future__ import annotations

from collections.abc import Callable
from typing import Any

from flywheel.overloads import SimpleOverload


class PredicateOverload(SimpleOverload):
    predicate: Callable[[str, Any], Any]  # (arg_name, call_value) -> collect_value

    def __init__(self, name: str, predicate: Callable[[str, Any], Any]):
        super().__init__(name)
        self.predicate = predicate

    def harvest(self, scope: dict, call_value: Any) -> dict[Callable, None]:
        return super().harvest(scope, self.predicate(self.name, call_value))
