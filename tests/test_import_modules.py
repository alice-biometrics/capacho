import os

import pytest

from capacho import import_modules


@pytest.mark.unit
class TestImportModules:
    path: list[str]

    def setup_method(self):
        self.path = [f"{os.path.dirname(os.path.realpath(__file__))}/test_module"]

    def should_import_modules(self):
        modules = import_modules(self.path)
        assert modules == [
            "module_1",
            "module_1.my_class",
            "module_1.submodule_1",
            "module_1.submodule_1.my_submodule_func",
            "module_2",
            "module_2.my_func",
        ]
