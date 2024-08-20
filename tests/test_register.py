from abc import abstractmethod

import pytest

from capacho import Container, Interface, register


def assert_list_in_list(inner_list: list, target_list: list) -> bool:
    return all(item in target_list for item in inner_list)


class MyAbstraction(Interface):
    @abstractmethod
    def execute(self):
        pass


class MyDoubleAbstraction(MyAbstraction):
    @abstractmethod
    def execute(self):
        pass


@pytest.mark.unit
class TestRegister:
    def setup_method(self):
        Container.clear()

    def teardown_method(self):
        Container.clear()

    def should_raise_error_when_register_a_function(self):
        with pytest.raises(TypeError):

            @register()
            def func_test1(a):
                return a

    def should_register_an_abstraction(self):
        @register()
        class MyImpl(MyAbstraction):
            def execute(self):
                pass

        assert "MyImpl" in Container.available(MyAbstraction)
        assert issubclass(Container.get(MyAbstraction, "MyImpl"), MyImpl)

    @pytest.mark.parametrize(
        "aliases",
        [
            ["my_alias"],
            ["my_alias", "my_processor"],
            ["my_alias", "my_processor", "MyProcessor"],
        ],
    )
    def should_register_an_abstraction_with_aliases(self, aliases):
        @register(aliases=aliases)
        class MyImpl(MyAbstraction):
            def execute(self):
                pass

        assert_list_in_list(
            list(set(["MyImpl"] + aliases)),
            Container.available(MyAbstraction),
        )
        assert issubclass(Container.get(MyAbstraction, "MyImpl"), MyImpl)

    def should_register_an_double_abstraction(self):
        @register()
        class MyImpl(MyDoubleAbstraction):
            def execute(self):
                pass

        assert "MyImpl" in Container.available(MyAbstraction)
        assert issubclass(Container.get(MyAbstraction, "MyImpl"), MyImpl)
