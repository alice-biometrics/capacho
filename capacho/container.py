from __future__ import annotations

import json
from collections.abc import Callable
from typing import TypeVar

from capacho.implementation_config import ImplementationConfig
from capacho.interface import Interface
from capacho.singleton import Singleton
from capacho.type_implementation_mapping import TypeImplementationMapping

BaseClass = str
ImplClass = str
RegisteredItems = dict[BaseClass, dict[ImplClass, type[Interface]]]

T = TypeVar("T")


def default_get_index_base_class(klass: type[Interface]) -> int:
    # MyImpl -> MyAbstraction -> Interface -> ABC -> Object
    #   -5          -4            -3        -2       -1
    #                ^----------------------------------------------- index_base_class_interface
    index_base_class_interface = -4
    return index_base_class_interface


class Container(metaclass=Singleton):
    def __init__(self):
        self._clear()

    def _set_type_implementations_mappings(self, mappings: list[TypeImplementationMapping]):
        self.type_implementations_mappings = mappings

    def _set_get_error_handler(self, error_handler: Callable[[str, str], None]):
        self.get_error_handler = error_handler

    def _set_index_base_class_map(self, get_index_base_class: Callable[[type[Interface]], int]):
        self.get_index_base_class = get_index_base_class

    def _add_to(
        self,
        klass: type[Interface],
        base_class: type | None = None,
        aliases: list[str] | None = None,
    ):
        name = klass.__name__
        base_name = base_class.__name__ if base_class else klass.__mro__[self.get_index_base_class(klass)].__name__

        if aliases is None:
            aliases = []

        if base_name not in self.registered_items:
            self.registered_items[base_name] = {}
            self.type_implementations[base_name] = {}

        if name in self.registered_items[base_name]:
            print(f"{name} plugin for {base_name} interface was already registered")

        self.registered_items[base_name][name] = klass

        # logger.debug(f"Adding {klass} to Container ({base_name})")

        for alias in aliases:
            if alias in self.registered_items[base_name]:
                print(f"{alias} plugin for {base_name} interface was already registered")
            self.registered_items[base_name][alias] = klass

        suffix_alias = ""
        if len(aliases) > 0:
            alias_str = ", ".join(aliases)
            suffix_alias = f" [{alias_str}]"

        name_with_alias = name + suffix_alias
        self.type_implementations[base_name][name_with_alias] = self._get_type_implementation(klass)

    def _get_type_implementation(self, klass: type[Interface]):
        module = klass.__module__
        type_implementation = "base"

        for type_implementation_mapping in self.type_implementations_mappings:
            if type_implementation_mapping.match(module):
                type_implementation = type_implementation_mapping.type_implementation
                break

        return type_implementation

    def _available(self, base_class: type[Interface]) -> list[ImplClass]:
        data = self.registered_items.get(base_class.__name__, {})
        return list(data.keys())

    def _get_registered_items(self) -> dict[str, list]:
        return {klass: list(data.keys()) for klass, data in self.registered_items.items()}

    def _get_type_implementations(self) -> dict[str, dict[str, str]]:
        return self.type_implementations

    def _show_registered(self):
        for klass, data in self.registered_items.items():
            print(f"{klass}: {list(data.keys())}")

    def _get(self, base_class: type[Interface], impl_class: ImplClass) -> type[Interface]:
        available_implementations = Container.available(base_class)
        if impl_class not in available_implementations:
            if self.get_error_handler is not None:
                self.get_error_handler(impl_class, base_class.__name__)
            else:
                raise TypeError(
                    f"{impl_class} is not registered in Container for base_class={base_class.__name__}."
                    f"\nPlease, register it, or use available implementations:"
                    f"\n{json.dumps(Container.get_registered_items(), indent=4)}\n"
                )
        return self.registered_items.get(base_class.__name__, {}).get(impl_class)

    def _clear(self):
        self.registered_items: RegisteredItems = {}
        self.type_implementations = {}
        self.type_implementations_mappings = []
        self.get_error_handler = None
        self.get_index_base_class = default_get_index_base_class

    @staticmethod
    def add_to(
        klass: type[Interface],
        base_class: type[Interface] | None = None,
        aliases: list[str] | None = None,
    ):
        Container()._add_to(klass, base_class, aliases)

    @staticmethod
    def set_type_implementations_mappings(mappings: list[TypeImplementationMapping]):
        Container()._set_type_implementations_mappings(mappings)

    @staticmethod
    def set_get_error_handler(error_handler: Callable[[str, str], None]):
        Container()._set_get_error_handler(error_handler)

    @staticmethod
    def set_index_base_class_map(get_index_base_class: Callable[[type[Interface]], int]):
        Container()._set_index_base_class_map(get_index_base_class)

    @staticmethod
    def available(base_class: type[Interface]) -> list[str]:
        return Container()._available(base_class)

    @staticmethod
    def get_registered_items() -> dict[str, list]:
        return Container()._get_registered_items()

    @staticmethod
    def get_type_implementations() -> dict[str, dict[str, str]]:
        return Container()._get_type_implementations()

    @staticmethod
    def show_registered():
        Container()._show_registered()

    @staticmethod
    def clear():
        Container()._clear()

    @staticmethod
    def get(base_class: T, impl_class: ImplClass) -> type[T]:
        return Container()._get(base_class, impl_class)

    @staticmethod
    def build(base_class: T, implementation_config: ImplementationConfig) -> T:
        item_name = implementation_config.name
        args = implementation_config.args
        return Container.get(base_class, item_name)(**args)
