from pydantic import BaseModel, Field

class Genre(BaseModel):
    uuid: str = Field(alias="id")
    name: str
