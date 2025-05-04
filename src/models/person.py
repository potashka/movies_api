from typing import List
from pydantic import BaseModel, Field


class PersonFilm(BaseModel):
    uuid: str
    roles: List[str]


class Person(BaseModel):
    uuid: str = Field(alias="id")
    full_name: str
    films: List[PersonFilm] = []
