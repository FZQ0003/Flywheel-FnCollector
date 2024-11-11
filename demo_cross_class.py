from dataclasses import dataclass

from flywheel import SimpleOverload

from flywheel_extras import FnCollection, FnCollector


@dataclass
class DemoPerform(FnCollection):
    attr_a: int
    attr_b: str

    @classmethod
    def from_self(cls, self):
        return cls(self.attr_a, self.attr_b)


class DemoCapability(DemoPerform):
    @FnCollector.set(SimpleOverload('name'))
    def func(self, name: str) -> str: ...


class DemoImplementation(DemoPerform):
    @DemoCapability.func.collect(name='abc')
    def impl_abc(self, name: str) -> str:
        return f'impl_abc: {self}, {name}'

    @DemoCapability.func.collect(name='def')
    def impl_def(self, name: str) -> str:
        return f'impl_def: {self}, {name}'


print(DemoCapability(114514, 'senpai').func('abc'))
print(DemoCapability(1919810, 'acceed').func('def'))
# print(DemoCapability(114514, 'senpai').func('ghi'))  # fail
