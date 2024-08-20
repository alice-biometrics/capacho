from __future__ import annotations

from pydantic import BaseModel, Field


class ImplementationConfig(BaseModel):
    name: str = Field(
        description=(
            "Source name of the implementation model/class. " "It will be used for build the registered object"
        )
    )
    args: dict | None = Field(default={}, description="Necessary arguments of the object class")
