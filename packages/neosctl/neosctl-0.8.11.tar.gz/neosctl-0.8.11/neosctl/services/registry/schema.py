from pydantic import BaseModel


class RegisterCore(BaseModel):
    name: str


class RemoveCore(BaseModel):
    urn: str
