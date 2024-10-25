from __future__ import annotations

from flywheel import SimpleOverload, TypeOverload, CollectContext, InstanceOf, InstanceContext

from flywheel_extras import FnCollector, OptionalInstanceOf


class DemoCapability:
    attr_a = InstanceOf(int)
    attr_b = OptionalInstanceOf(str, 'string')

    @FnCollector.set(SimpleOverload('name'))
    def func_a(self, name: str) -> str: ...

    @FnCollector.set(SimpleOverload('name'), TypeOverload('event'))
    def func_b(self, name: str, event: object | None = None) -> str: ...

    # Class methods are not directly supported.
    # Inherit FnCollectorContainer to avoid this.
    @classmethod
    @FnCollector.set(SimpleOverload('name'))
    def func_c(cls, name: str) -> str: ...

    # For properties, use property.fget to get FnCollector.
    # It is not recommended to set no overloads.
    @property
    @FnCollector.set()
    def func_p(self) -> str: ...  # noqa

    # Fully supported
    @staticmethod
    @FnCollector.set(SimpleOverload('name'))
    def func_s(name: str) -> str: ...


demo = DemoCapability()


@DemoCapability.func_a.collect(name='me')
def impl_a_me(self: DemoCapability, name: str) -> str:
    return f'impl_a_me: {self}, {name}'


# print(demo.func_a('him'))  # fail
print(demo.func_a('me'))


@DemoCapability.func_b.collect(name='me', event=int)
@DemoCapability.func_b.collect(name='him', event=int)
@DemoCapability.func_b.collect(name='me', event=str)
def impl_b_1(self: DemoCapability, name: str, event: int | str) -> str:
    return f'impl_b_1: {self}, {name}, ({type(event).__name__}) {event}'


print(demo.func_b('me', 114))
print(demo.func_b('him', 514))
print(demo.func_b('me', '1919'))
print(demo.func_b('him', '810'))  # pass, for impl_b is the same
# print(demo.func_b('me', [42]))  # fail

with CollectContext().scope() as cs:
    @DemoCapability.func_b.collect(name='me', event=int)
    def impl_b_2(self: DemoCapability, name: str, event: int) -> str:
        print(self.func_b(name, event))
        return f'impl_b_2: local'


    print(demo.func_b('me', 42))


@DemoCapability.func_c.collect(name='yeah')
def impl_c(cls: type[DemoCapability], name: str) -> str:
    return f'impl_c: {cls}, {name}'


print(DemoCapability.func_c('yeah'))
print(demo.func_c('yeah'))


@DemoCapability.func_a.collect(name='haha')
def impl_a_haha(self: DemoCapability, name: str) -> str:
    return f'impl_a_haha: {self.attr_a}, {self.attr_b}, {name}'


with InstanceContext().scope() as ins:
    ins.instances[int] = 123
    print(demo.func_a('haha'))


# print(demo.func_a('haha'))  # fail

@DemoCapability.func_b.collect(name='him')
def impl_b_3(self: DemoCapability, name: str, event: object | None = None) -> str:
    return f'impl_b_3: {self}, {name}, ({type(event).__name__}) {event}'


print(demo.func_b('him', [42]))
print(demo.func_b('him'))


@DemoCapability.func_p.fget.collect()  # type: ignore
def impl_p(self: DemoCapability) -> str:
    return f'impl_p: Property func_p called by {self}'


print(demo.func_p)


@DemoCapability.func_s.collect(name='him')
def impl_s(name: str) -> str:
    return f'impl_s: Static method called by {name}'


print(DemoCapability.func_s('him'))
print(demo.func_s('him'))
