from __future__ import annotations

import itertools
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, Any

from flywheel import CollectContext, FnCollectEndpoint, FnImplementEntity, FnOverload, SimpleOverload
from flywheel.globals import CALLER_TOKENS, COLLECTING_CONTEXT_VAR
from flywheel.typing import P, R

from .utils import get_var_names, bind_args


@dataclass
class FnCollector(Generic[P, R]):
    base: Callable[P, R]
    overloads: dict[str, tuple[FnOverload, SimpleOverload]] = field(default_factory=dict)
    base_as_default: bool = False
    endpoints: dict[Any, FnCollectEndpoint[..., Callable[P, R]]] = field(init=False)

    def __post_init__(self):
        self.endpoints = {None: FnCollectEndpoint(self._endpoint_target)}
        if not self.overloads:
            # Add empty SimpleOverloads if no FnOverloads found
            empty_overload = SimpleOverload(f'empty@{id(self.base)}')
            self.overloads = {'!': (empty_overload, empty_overload)}

    @classmethod
    def set(cls, *overloads: FnOverload, as_default: bool = False):
        def wrapper(func: Callable[P, R]) -> 'FnCollector[P, R]':
            # func = getattr(func, '__func__', func)
            return cls(
                base=func,
                overloads={
                    # Another SimpleOverload as fallback FnOverload (optional)
                    _.name: (_, SimpleOverload('fallback@' + _.name))
                    for _ in overloads if _.name in get_var_names(func)
                },
                base_as_default=as_default
            )

        return wrapper

    def _endpoint_target(self, *_, **overload_settings):
        # Collect
        for name, fn_overload in self.overloads.items():
            value = overload_settings.get(name, None)
            yield fn_overload[value is None].hold(value)

        # For type checking
        def shape(*args: P.args, **kwargs: P.kwargs) -> R:
            ...

        return shape

    def collect(self,
                __namespace: Any = None,
                __context: CollectContext | None = None,
                **overload_settings):
        if not (endpoint := self.endpoints.get(__namespace, None)):
            # Deepcopy the generator for different namespaces
            self.endpoints[__namespace] = endpoint = FnCollectEndpoint(deepcopy(self._endpoint_target))
        if not __context:
            __context = COLLECTING_CONTEXT_VAR.get()

        def wrapper(func: Callable[P, R]):
            # Check function signature
            if (
                    not isinstance(func, FnImplementEntity)
                    and get_var_names(func) != get_var_names(self.base)
            ):
                raise TypeError(
                    'Signature mismatch: '
                    f'func{get_var_names(func)} != base{get_var_names(self.base)}'
                )
            return __context.collect(endpoint(**overload_settings)(func))

        return wrapper

    def call(self, __namespace, *args: P.args, **kwargs: P.kwargs) -> R:
        # Check input signature
        args_dict = bind_args(self.base, *args, **kwargs)
        # Harvest
        harvest_temp: list[tuple[str, FnOverload, SimpleOverload, Any, set[Callable], set[Callable]]]
        harvest_temp = [(_n, _o[0], _o[1], args_dict.get(_n, None), set(), set())
                        for _n, _o in self.overloads.items()]
        endpoint = self.endpoints.get(__namespace, self.endpoints[None])
        for selection in endpoint.select(False):
            for h_n, h_o, h_o_fb, h_v, r, r_fb in harvest_temp:
                try:
                    r.update(selection.harvest(h_o, h_v))
                except NotImplementedError:
                    ...
                try:
                    # Fallback
                    r_fb.update(selection.harvest(h_o_fb, None))
                except NotImplementedError:
                    ...
        # I think I should write a doc here
        for results in itertools.product(*(_[-2:] for _ in harvest_temp)):
            if not results:
                continue
            # The first result is perfect
            for result in set.intersection(*results):
                # From Selection._wraps()
                tokens = CALLER_TOKENS.get()
                current_index = tokens.get(endpoint, -1)
                _tok = CALLER_TOKENS.set({**tokens, endpoint: current_index + 1})
                try:
                    return result(*args, **kwargs)
                finally:
                    CALLER_TOKENS.reset(_tok)
        if self.base_as_default:
            return self.base(*args, **kwargs)
        raise NotImplementedError('Cannot lookup any implementation with given arguments')

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.call(None, *args, **kwargs)
