from abc import ABC


class Interface(ABC):  # noqa
    @classmethod
    def info(cls) -> dict:
        return {"name": cls.__name__}

    @classmethod
    def description(cls) -> str:
        return f"ERROR: Add a description implementing {cls.__name__}.description() method"
