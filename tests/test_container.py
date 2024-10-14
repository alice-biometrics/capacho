import pytest

from capacho import Container, ImplementationConfig, Interface, TypeImplementationMapping


class MyType(Interface): ...


class MyImpl(MyType): ...


class MyImplConfig(ImplementationConfig): ...


@pytest.mark.unit
class TestContainer:
    def should_check_registered_items_when_empty(self):
        registered_items = Container.get_registered_items()
        assert len(registered_items) == 0

    def should_have_no_available_type(self):
        available = Container.available(MyImpl)
        assert len(available) == 0

    def should_add_an_implementation_with_automatic_inheritance(self):
        Container.add_to(MyImpl)
        assert len(Container.available(MyType)) == 1

    def should_add_an_implementation_passing_inheritance(self):
        Container.add_to(MyImpl, base_class=str)
        assert len(Container.available(MyImpl)) == 0
        assert len(Container.available(str)) == 1

    def should_get_a_class_from_container(self):
        Container.add_to(MyImpl)
        implementation_klass = Container.get(MyType, "MyImpl")
        assert implementation_klass == MyImpl

    def should_build_instance_from_container(self):
        Container.add_to(MyImpl)
        implementation_instance = Container.build(MyType, MyImplConfig(name="MyImpl"))
        assert isinstance(implementation_instance, MyImpl)

    def should_raise_exception_when_get_a_not_available_base_class(self):
        with pytest.raises(TypeError) as excinfo:
            Container.get(MyType, "MyNotRegisteredImpl")
        assert "MyNotRegisteredImpl is not registered in Container for base_class=MyType" in str(excinfo.value)

    def should_raise_exception_when_get_a_not_available_base_class_using_error_handler(self):
        def my_error_handler(impl_class: str, base_class: str) -> None:
            raise TypeError("MyError Handler")

        Container.set_get_error_handler(my_error_handler)
        with pytest.raises(TypeError) as excinfo:
            Container.get(MyType, "MyNotRegisteredImpl")
        assert "MyError Handler" in str(excinfo.value)

    def should_get_type_implementation(self):
        Container.add_to(MyImpl)
        type_implementations = Container.get_type_implementations()
        assert type_implementations["MyType"].get("MyImpl") == "base"

    def should_get_type_implementations_using_alias(self):
        Container.add_to(MyImpl, aliases=["MyAlias"])
        type_implementations = Container.get_type_implementations()
        assert type_implementations["MyType"].get("MyImpl [MyAlias]") == "base"

    @pytest.mark.parametrize(
        "mappings,expected_type_implementation",
        [
            ([TypeImplementationMapping(module_startswith="test", type_implementation="plugin")], "plugin"),
            (
                [
                    TypeImplementationMapping(
                        module_startswith="test.test_module", type_implementation="other", startswith=False
                    )
                ],
                "other",
            ),
            ([TypeImplementationMapping(module_startswith="other_module", type_implementation="plugin")], "base"),
            (
                [TypeImplementationMapping(module_startswith="test", type_implementation="other", startswith=False)],
                "base",
            ),
        ],
    )
    def should_get_type_implementations_using_type_implementation_mapping(
        self, mappings: list[TypeImplementationMapping], expected_type_implementation: str
    ):
        Container.set_type_implementations_mappings(mappings)
        Container.add_to(MyImpl)
        type_implementations = Container.get_type_implementations()
        assert type_implementations["MyType"].get("MyImpl") == expected_type_implementation
