from __future__ import annotations

from collections.abc import Callable

from capacho.container import Container
from capacho.interface import Interface


def register_callable(
    callable_class: Callable,
    base_class: type[Interface],
    aliases: list[str] | None = None,
    available_base_class: list[type[Interface]] | None = None,
):
    if available_base_class and base_class not in available_base_class:
        raise TypeError(f"register_callable only accepts the following base class: {available_base_class}")

    Container.add_to(callable_class, base_class, aliases)  # noqa
