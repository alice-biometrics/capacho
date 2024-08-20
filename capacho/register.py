from __future__ import annotations

from typing import TypeVar

from capacho.container import Container
from capacho.interface import Interface

T = TypeVar("T")


class Register:
    def __init__(self, aliases: list[str] | None = None):
        self.aliases = aliases

    def __call__(self, cls: T) -> T:
        if issubclass(cls, Interface):
            Container.add_to(cls, aliases=self.aliases)
        else:
            raise TypeError(f"Impossible to register ({cls}). Please try inheriting from Interface")
        return cls


register = Register
