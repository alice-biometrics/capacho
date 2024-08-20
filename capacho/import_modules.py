from __future__ import annotations

import importlib.util
import pkgutil
import sys


def import_modules(path: list[str]) -> list[str]:
    _all = []
    for loader, module_name, _is_pkg in pkgutil.walk_packages(path):
        _all.append(module_name)
        spec = loader.find_spec(module_name)
        _module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_module)
        sys.modules[spec.name] = _module
        globals()[module_name] = _module
    return _all
