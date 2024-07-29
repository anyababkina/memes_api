from fastapi import Form
from pydantic import BaseModel, ConfigDict


class MemesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None


class CreateMemSchema(BaseModel):
    description: str | None = None

    @classmethod
    def as_form(cls, description: str | None = Form(default=None)):
        return cls(description=description)