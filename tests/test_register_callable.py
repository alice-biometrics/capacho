from abc import abstractmethod

import pytest

from capacho import Container, Interface, register_callable


def callable_func():
    return "external"


class MyAbstraction(Interface):
    @abstractmethod
    def execute(self):
        pass


class MyAllowedAbstraction(Interface):
    @abstractmethod
    def execute(self):
        pass


@pytest.mark.unit
class TestRegisterCallable:
    def should_raise_error_when_register_not_allowed_base_class(self):
        class MyClass:
            pass

        with pytest.raises(TypeError):
            register_callable(
                callable_class=MyClass,
                base_class=MyAbstraction,
                aliases=["MyClass"],
                available_base_class=[MyAllowedAbstraction],
            )

    def should_register_an_external_callable(self):
        register_callable(
            callable_class=callable_func,
            base_class=MyAbstraction,
            aliases=["MyAbstractionCallable"],
        )

        type_implementations = Container.get_type_implementations()

        assert "callable_func" in Container.available(MyAbstraction)
        assert "MyAbstractionCallable" in Container.available(MyAbstraction)
        assert type_implementations["MyAbstraction"]["callable_func [MyAbstractionCallable]"] == "base"
