from pydantic import BaseModel, Field


class TypeImplementationMapping(BaseModel):
    module_startswith: str = Field(description="Pattern to match implementation module")
    type_implementation: str = Field(
        description="Type of implementation to save references and order similar implementations"
    )
    startwith: bool = Field(
        default=True,
        description="You can select if startwith or not with given module_startwith",
    )

    def match(self, module_name: str) -> bool:
        condition = False
        if (self.startwith and module_name.startswith(self.module_startswith)) or (
            not self.startwith and not module_name.startswith(self.module_startswith)
        ):
            condition = True
        return condition
