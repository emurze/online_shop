from pydantic import BaseModel, ConfigDict, condecimal


class Schema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
    )


class ErrorSchema(Schema):
    error: str


PydanticMoney = condecimal(max_digits=10, decimal_places=2)
