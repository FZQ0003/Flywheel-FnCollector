from __future__ import annotations

from flywheel_extras import FnCollector, MappingOverload, PredicateOverload


@FnCollector.set(MappingOverload('raw', lambda raw: raw['type']), as_default=True)
def func_a(raw: dict[str, str]) -> str:
    return f'func_a (default): {raw}'


@func_a.collect(raw='foo.bar')
def impl_a(raw: dict[str, str]) -> str:
    return f'impl_a (foo.bar): {raw}'


print(func_a({'type': 'foo.bar', 'value': '42'}))
print(func_a({'type': 'other', 'key': 'OwO'}))


@FnCollector.set(PredicateOverload('raw', lambda co, ca: type(co) == type(ca)), as_default=True)
def func_b(raw) -> str:
    return f'func_b (default): ({type(raw).__name__}) {raw}'


@func_b.collect(raw='string')
def impl_b_1(raw: str) -> str:
    return f'impl_b (str): ({type(raw).__name__}) {raw}'


@func_b.collect(raw=123)
def impl_b_2(raw: int) -> str:
    return f'impl_b (int): ({type(raw).__name__}) {raw}'


print(func_b('world'))
print(func_b(42))
print(func_b([]))
