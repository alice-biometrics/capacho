from __future__ import annotations

import contextlib


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        with contextlib.suppress(KeyError):
            del Singleton._instances[cls]
